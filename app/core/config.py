import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

# прочитать .env из соседнего репозитория
# current_dir = os.getcwd()
# # Поднимаемся на уровень выше 2 раза
# project_root = os.path.dirname(os.path.dirname(current_dir))
# dotenv_path = f"{project_root}/devops/.env"
#
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
# else:
#     load_dotenv()
#     #raise FileNotFoundError(f".env file not found at {dotenv_path}")


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

    # Это стиль Pydantic v1 или старые версии Pydantic v2 , совместимый с предыдущими версиями
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"


settings = Settings()

#print(settings.model_dump())

def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


