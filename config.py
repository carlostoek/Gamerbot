import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
DATABASE_URL = "sqlite+aiosqlite:///./database/gamification.db"


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN no está definido en el archivo .env")
if ADMIN_ID is None:
    raise ValueError("ADMIN_ID no está definido en el archivo .env")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definido en el archivo .env")
