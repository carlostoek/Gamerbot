import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

import config
from database.database import init_db, Base, engine  # <-- Eliminamos get_db
from handlers import user_handlers, admin_handlers, common_handlers
from middlewares.user_middleware import UserMiddleware
from schedulers import tasks  # <-- Comentar o eliminar por ahora
from apscheduler.schedulers.asyncio import AsyncIOScheduler # <-- Comentar o eliminar por ahora

# Inicializar la base de datos de forma síncrona al importar (intento)
async def sync_init_db():
    await init_db()
    print("Base de datos inicializada (síncronamente al importar) en bot.py.")

asyncio.run(sync_init_db())

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

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

    # # Configurar tareas programadas - Comentado por ahora
    # scheduler = AsyncIOScheduler()
    # tasks.setup_scheduled_tasks(scheduler, bot, get_session) # <-- Usar get_session si se reactiva
    # scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
    
