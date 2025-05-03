import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # Asegúrate de tener esto aquí también
from sqlalchemy.ext.declarative import declarative_base

import config
from database.database import init_db, get_db, Base, engine  # Importamos Base y engine
from handlers import user_handlers, admin_handlers, common_handlers
from middlewares.user_middleware import UserMiddleware
from schedulers import tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # Inicializar la base de datos de forma explícita y asíncrona
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Base de datos inicializada (explícitamente y asíncrona).")

    # Configurar comandos del bot (se mostrarán en el menú de Telegram)
    commands = [
        BotCommand(command="/start", description="Inicia el bot y muestra el menú"),
        BotCommand(command="/perfil", description="Muestra tu perfil"),
        BotCommand(command="/ranking", description="Top 10 de usuarios"),
        BotCommand(command="/admin", description="Panel de administración (solo para admins)"),
    ]
    await bot.set_my_commands(commands)

    # Registrar middlewares
    dp.message.middleware(UserMiddleware())

    # Registrar handlers
    user_handlers.register_handlers(dp)
    admin_handlers.register_handlers(dp)
    common_handlers.register_handlers(dp)

    # Configurar tareas programadas
    scheduler = AsyncIOScheduler()
    tasks.setup_scheduled_tasks(scheduler, bot, get_db)
    scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
