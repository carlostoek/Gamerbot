from aiogram import Router, types
from sqlalchemy.orm import Session

router = Router()

from aiogram.filters import Command

@router.message(Command(commands=["admin"]))
async def admin_panel(message: types.Message):
    # Aquí la lógica del panel de administración
    await message.answer("Panel de administración (en desarrollo)")

@router.message(Command(commands=["sumarpuntos"]))
async def add_points(message: types.Message, db: Session):
    # Aquí la lógica para sumar puntos manualmente
    if message.from_user.id == config.ADMIN_ID:
        try:
            parts = message.text.split()
            if len(parts) == 3:
                user_id = int(parts[1])
                points = int(parts[2])
                user = db.query(models.Usuario).filter(models.Usuario.user_id == user_id).first()
                if user:
                    user.puntos += points
                    db.commit()
                    await message.answer(f"Se sumaron {points} puntos al usuario {user_id}.")
                else:
                    await message.answer(f"No se encontró al usuario con ID {user_id}.")
            else:
                await message.answer("Uso correcto: /sumarpuntos <user_id> <puntos>")
        except ValueError:
            await message.answer("Los argumentos deben ser números.")
    else:
        await message.answer("No tienes permiso para usar este comando.")

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
  
