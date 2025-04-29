from aiogram import Bot
from sqlalchemy.orm import Session
from database import models
from datetime import timedelta

async def otorgar_puntos_por_permanencia(bot: Bot, db: Session):
    users = db.query(models.Usuario).all()
    for user in users:
        user.puntos += 50
        print(f"Se otorgaron 50 puntos por permanencia a {user.user_id} - {user.username}")
    db.commit()

def setup_scheduled_tasks(scheduler, bot: Bot, get_db_func):
    async def scoped_otorgar_puntos():
        async with next(get_db_func()) as db:
            await otorgar_puntos_por_permanencia(bot, db)

    scheduler.add_job(scoped_otorgar_puntos, trigger="interval", weeks=1)
  
