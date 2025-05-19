from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()
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

    # Database settings
    DB_LOGIN: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DATABASE_URL: str


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()