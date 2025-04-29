from aiogram import Router, types
from sqlalchemy.orm import Session
from database import models

router = Router()

@router.message(commands=["start"])
async def start_handler(message: types.Message, db: Session):
    user = db.query(models.Usuario).filter(models.Usuario.user_id == message.from_user.id).first()
    if user:
        await message.answer(f"¡Bienvenido de nuevo, {user.username}!")
        # Aquí podrías mostrar el menú principal con botones inline
    else:
        await message.answer("¡Bienvenido al sistema de gamificación!")
        # El middleware ya registró al usuario

@router.message(commands=["perfil"])
async def profile_handler(message: types.Message, db: Session):
    user = db.query(models.Usuario).filter(models.Usuario.user_id == message.from_user.id).first()
    if user:
        await message.answer(
            f"Tu perfil:\n"
            f"ID: {user.user_id}\n"
            f"Nombre de usuario: {user.username}\n"
            f"Puntos: {user.puntos}\n"
            f"Nivel: {user.nivel}\n"
            f"Fecha de ingreso: {user.fecha_ingreso.strftime('%Y-%m-%d')}"
        )
    else:
        await message.answer("Tu perfil no se encontró.")

@router.message(commands=["ranking"])
async def ranking_handler(message: types.Message, db: Session):
    top_users = db.query(models.Usuario).order_by(models.Usuario.puntos.desc()).limit(10).all()
    if top_users:
        ranking_text = "🏆 **Ranking de Usuarios** 🏆\n"
        for i, user in enumerate(top_users, 1):
            ranking_text += f"{i}. {user.username} - {user.puntos} puntos\n"
        await message.answer(ranking_text)
    else:
        await message.answer("Aún no hay usuarios en el ranking.")

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
  
