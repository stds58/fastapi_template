import os
from app.core.config import get_db_url
from contextlib import asynccontextmanager
from functools import wraps
from typing import Optional, Callable, Any, AsyncGenerator
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import HTTPException
from app.db.session import async_session_maker, get_session_with_isolation
import logging


logger = logging.getLogger(__name__)



#def connection = def get_db

# def connection2(isolation_level: Optional[str] = None, commit: bool = True):
#     """
#     Декоратор для управления сессией с возможностью настройки уровня изоляции и коммита.
#     Декоратор не должен быть асинхронным , он просто создаёт обёртку вокруг асинхронной функции.
#     Для декорирования функций с логикой коммита / отката
#     """
#     def decorator(method: Callable[..., Any]):
#         print('111111111111')
#         @wraps(method)
#         async def wrapper(*args, **kwargs):
#             print('222222222222')
#             async with get_session_with_isolation(async_session_maker, isolation_level) as session:
#                 try:
#                     print('33333333333')
#                     result = await method(*args, session=session, **kwargs)
#                     if commit and session.in_transaction():
#                         await session.commit()
#                     return result
#                 except IntegrityError as e:
#                     print('444444444')
#                     logger.error(f"Ошибка целостности данных: {e.orig}")
#                     raise HTTPException(status_code=400, detail=f"Ошибка целостности данных: {e.orig}")
#                 except SQLAlchemyError as e:
#                     print('55555555555')
#                     logger.error(f"Ошибка при работе с базой данных: {e}")
#                     raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
#                 except Exception as e:
#                     print('6666666666')
#                     if session.in_transaction():
#                         await session.rollback()
#                     raise
#
#         print('7777777777')
#         return wrapper
#     return decorator


def connection(isolation_level: Optional[str] = None, commit: bool = True):
    """
    Фабрика зависимости для FastAPI, создающая асинхронную сессию с заданным уровнем изоляции.
    """

    async def dependency() -> AsyncGenerator[AsyncSession, None]:
        async with get_session_with_isolation(async_session_maker, isolation_level) as session:
            try:
                yield session
                if commit and session.in_transaction():
                    await session.commit()
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(status_code=400, detail=f"Ошибка целостности данных: {e.orig}")
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=500, detail=f"Ошибка БД: {e}")
            except Exception:
                await session.rollback()
                raise

    return dependency


_custom_engine = None

def set_test_engine(engine):
    global _custom_engine
    _custom_engine = engine

async def get_db():
    global _custom_engine
    engine = _custom_engine or create_async_engine(get_db_url())
    async_session = async_sessionmaker(engine)
    async with async_session() as session:
        yield session

# async def get_db():
#     """	Для интеграции с FastAPI как зависимость"""
#     async with async_session_maker() as session:
#         yield session


def connection2(isolation_level: Optional[str] = None, commit: bool = True):
    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                try:
                    if isolation_level:
                        await session.execute(text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}"))
                        # Проверяем уровень изоляции
                        result = await session.execute(text("SHOW TRANSACTION ISOLATION LEVEL;"))
                        current_isolation_level = result.scalar()
                        print(f"Текущий уровень изоляции: {current_isolation_level}")
                    result = await method(*args, session=session, **kwargs)
                    if commit:
                        await session.commit()
                    return result
                except IntegrityError as e:
                    logger.error(f"Ошибка целостности данных: {e.orig}")
                    raise HTTPException(status_code=400, detail=f"Ошибка целостности данных: {e.orig}")
                except SQLAlchemyError as e:
                    logger.error(f"Ошибка при работе с базой данных: {e}")
                    raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
                except Exception as e:
                    await session.rollback()
                    raise
                finally:
                    await session.close()
        return wrapper
    return decorator



# """
#     Декоратор для управления сессией с возможностью настройки уровня изоляции и коммита.
#     Параметры:
#     - `isolation_level`: уровень изоляции для транзакции (например, "SERIALIZABLE").
#     - `commit`: если `True`, выполняется коммит после вызова метода.
#     READ COMMITTED — для обычных запросов (по умолчанию в PostgreSQL).
#     SERIALIZABLE — для финансовых операций, требующих максимальной надежности.
#     REPEATABLE READ — для отчетов и аналитики.
#
#     # Чтение данных
#     @connection(isolation_level="READ COMMITTED")
#     async def get_user(self, session, user_id: int):
#         ...
#     # Финансовая операция
#     @connection(isolation_level="SERIALIZABLE", commit=False)
#     async def transfer_money(self, session, from_id: int, to_id: int):
#         ...
#     """