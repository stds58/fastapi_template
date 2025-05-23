import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime
from typing import Annotated, Optional, Callable, Any, AsyncGenerator
from sqlalchemy import func, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import String, Boolean, ForeignKey
from fastapi import HTTPException
from app.core.config import get_db_url
from contextlib import asynccontextmanager
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App settings
    APP_NAME: str
    DEBUG: bool
    ENV: str
    SECRET_KEY: str
    ALGORITHM: str
    SESSION_MIDDLEWARE_SECRET_KEY: str

    # Database settings
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DATABASE_URL: str

    # Keycloak settings
    KEYCLOAK_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str
    KEYCLOAK_POSTGRES_USER: str
    KEYCLOAK_POSTGRES_PASSWORD: str
    KEYCLOAK_POSTGRES_DB: str
    KEYCLOAK_DB_PORT: str
    KEYCLOAK_ADMIN: str
    KEYCLOAK_ADMIN_PASSWORD: str
    KEYCLOAK_PORT: str
    FRONT_URL: str
    SSO_SESSION_MAX_LIFESPAN: int
    SSO_SESSION_IDLE_TIMEOUT: int

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

settings = Settings()

def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}

########################################################################################################################
# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
access_id = Annotated[int, mapped_column(nullable=True, info={"verbose_name": "id в аксесе Блага"})]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=func.now())]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]
str_255 = Annotated[str, mapped_column(String(255), nullable=True)]
bool_null_false = Annotated[bool, mapped_column(default=False, server_default=text("'false'"), nullable=False)]

def fk_protect_nullable(table_name: str):
    return Annotated[
        Optional[int],
        mapped_column(
            ForeignKey(f"{table_name}.id", ondelete="PROTECT"),
            nullable=True
        )
    ]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True  # Класс абстрактный, чтобы не создавать отдельную таблицу для него

    # id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    access_id: Mapped[access_id]

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

########################################################################################################################






########################################################################################################################





########################################################################################################################





########################################################################################################################





########################################################################################################################





########################################################################################################################





########################################################################################################################





########################################################################################################################

