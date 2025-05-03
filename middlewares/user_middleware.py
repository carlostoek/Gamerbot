from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
        async for db in get_db():
            result = await db.execute(select(models.Usuario).where(models.Usuario.user_id == user.id))
            user_exists = result.scalar_one_or_none()
            if not user_exists:
                new_user = models.Usuario(user_id=user.id, username=user.username)
                db.add(new_user)
                await db.commit()
                print(f"Nuevo usuario registrado: {user.id} - {user.username}")
            data["db"] = db
            result = await handler(event, data)
            return result
