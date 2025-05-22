import pytest
from app.dependencies.get_db import get_db
from asyncio import AbstractEventLoop, get_event_loop
from sqlalchemy.ext.asyncio import create_async_engine
from app.dependencies.get_db import set_test_engine, get_db



# @pytest.fixture(scope="function")
# def event_loop() -> AbstractEventLoop:
#     loop = get_event_loop()
#     yield loop
#     loop.close()


# @pytest.fixture(scope="function")
# async def db_session():
#     async for session in get_db(testing=True):
#         yield session

@pytest.fixture(scope="function")
async def db_session():
    # Создаем отдельный движок для тестов
    test_engine = create_async_engine("postgresql+asyncpg://admin:admin@localhost:5435/fast_api_test")
    set_test_engine(test_engine)

    # Опционально: создаём таблицы перед каждым тестом
    from app.models import Base
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for session in get_db():
        yield session

    # Очистка после теста
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)