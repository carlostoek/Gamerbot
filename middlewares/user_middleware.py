from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select
from database import models
import config

engine = create_async_engine(config.DATABASE_URL)

async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user: User = event.from_user
        async for db in get_session():
            result = await db.execute(select(models.Usuario).where(models.Usuario.user_id == user.id))
            user_exists = result.scalar_one_or_none()
            if not user_exists:
                new_user = models.Usuario(user_id=user.id, username=user.username)
                db.add(new_user)
                await db.commit()
                print(f"Nuevo usuario registrado: {user.id} - {user.username} (desde middleware)")
            data["db"] = db
            result = await handler(event, data)
            return result
