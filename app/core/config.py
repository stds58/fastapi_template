import os
from pydantic import BaseModel
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

class AppSettings(BaseModel):
    APP_NAME: str
    DEBUG: bool
    ENV: str
    SECRET_KEY: str
    ALGORITHM: str
    SESSION_MIDDLEWARE_SECRET_KEY: str


class DBSettings(BaseModel):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DATABASE_URL: str

class TestDBSettings(BaseModel):
    TEST_TESTING: bool
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DATABASE_URL: str

class KeycloakSettings(BaseModel):
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

current_dir = os.path.dirname(os.path.abspath(__file__))  # app/core/
parent_dir = os.path.dirname(current_dir)                 # app/
project_dir = os.path.dirname(parent_dir)                 # fastapi_template/
env_path = os.path.join(project_dir, ".env")
# print(f"пути в проекте\n"
#       f"current_dir {current_dir}\n"
#       f"parent_dir {parent_dir}\n"
#       f"project_dir {project_dir}\n"
#       f"env_path {env_path}")

class Settings(BaseSettings):
    app: AppSettings
    db: DBSettings
    test: TestDBSettings
    keycloak: KeycloakSettings

    model_config = SettingsConfigDict(
        #env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        env_file=env_path,
        env_nested_delimiter="__",
    )

settings = Settings()

#print(settings.model_dump())

def get_db_url(testing: bool = False):
    if testing:
        return (f"postgresql+asyncpg://{settings.test.TEST_DB_USER}:{settings.test.TEST_DB_PASSWORD}@"
                f"{settings.test.TEST_DB_HOST}:{settings.test.TEST_DB_PORT}/{settings.test.TEST_DB_NAME}")
    else:
        return (f"postgresql+asyncpg://{settings.db.DB_USER}:{settings.db.DB_PASSWORD}@"
                f"{settings.db.DB_HOST}:{settings.db.DB_PORT}/{settings.db.DB_NAME}")

def get_auth_data():
    return {"secret_key": settings.db.SECRET_KEY, "algorithm": settings.db.ALGORITHM}


