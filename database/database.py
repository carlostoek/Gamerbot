from sqlalchemy import create_engine  # <--- Cambiar a create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from . import models  # Importa las definiciones de las tablas
import config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # Importar create_async_engine y AsyncSession

Base = declarative_base()
engine = create_async_engine(config.DATABASE_URL)  # <--- Usar create_async_engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)  # Usar AsyncSession

async def get_db():
    async with SessionLocal() as db:
        yield db

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    async def main():
        await init_db()
        print("Base de datos inicializada (asíncronamente).")
    asyncio.run(main())
