from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.orm import Session
from database import models
from database.database import get_db

class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user: User = event.from_user
        db: Session = next(get_db())
        user_exists = db.query(models.Usuario).filter(models.Usuario.user_id == user.id).first()
        if not user_exists:
            new_user = models.Usuario(user_id=user.id, username=user.username)
            db.add(new_user)
            db.commit()
            print(f"Nuevo usuario registrado: {user.id} - {user.username}")
        data["db"] = db  # Pasar la sesión de la base de datos a los handlers
        result = await handler(event, data)
        return result
      
