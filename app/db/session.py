import os
from app.core.config import get_db_url
from contextlib import asynccontextmanager
from functools import wraps
from typing import Optional, Callable, Any, AsyncGenerator
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()
import logging



logger = logging.getLogger(__name__)
# create_async_engine: создаёт асинхронное подключение к базе данных PostgreSQL, используя драйвер asyncpg.
# async_session_maker: создаёт фабрику асинхронных сессий, используя созданный движок.
# Сессии используются для выполнения транзакций в базе данных.
# Base: абстрактный класс, от которого наследуются все модели.
# Он используется для миграций и аккумулирует информацию обо всех моделях,
# чтобы Alembic мог создавать миграции для синхронизации структуры базы данных с моделями на бэкенде.·
# @declared_attr.directive: определяет имя таблицы для модели на основе имени класса,
# преобразуя его в нижний регистр и добавляя букву 's' в конце (например, класс User будет иметь таблицу users).

DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def get_session_with_isolation(session_factory, isolation_level: Optional[str] = None) -> AsyncGenerator[AsyncSession, None]:
    """
    Контекстный менеджер для создания сессии с опциональным уровнем изоляции.Для гибкого управления уровнем изоляции
    """
    async with session_factory() as session:
        if isolation_level:
            await session.connection(execution_options={"isolation_level": isolation_level})
            # Проверяем уровень изоляции
            result = await session.execute(text("SHOW TRANSACTION ISOLATION LEVEL;"))
            current_isolation_level = result.scalar()
            #print(f"Текущий уровень изоляции: {current_isolation_level}")
        yield session

