import pytest
from typing import TypeVar, Generic, Type, Any
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.crud.base import BaseDAO
from sqlalchemy import update


ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=BaseModel)

class BaseDAOTestCase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, FilterSchemaType]):
    dao: Type[BaseDAO[ModelType, CreateSchemaType, UpdateSchemaType, FilterSchemaType]]
    create_data: dict
    update_data: dict
    filter_data: dict

    @classmethod
    def setup_class(cls, dao: Type[BaseDAO], create_data: dict, update_data: dict, filter_data: dict):
        cls.dao = dao
        cls.create_data = create_data
        cls.update_data = update_data
        cls.filter_data = filter_data

    @pytest.mark.asyncio
    async def test_create(self, db_session: AsyncSession):
        data = self.dao.create_schema(**self.create_data)
        instance = await self.dao.add(session=db_session, **data.model_dump())
        assert instance.id is not None
        for key, value in data.model_dump().items():
            assert getattr(instance, key) == value
        return instance

    @pytest.mark.asyncio
    async def test_find_one_or_none_by_id(self, db_session: AsyncSession):
        created = await self.test_create(db_session)
        instance = await self.dao.find_one_or_none_by_id(created.id, db_session)
        assert instance is not None
        assert instance.id == created.id

    @pytest.mark.asyncio
    async def test_find_all(self, db_session: AsyncSession):
        # Создаем несколько записей с уникальными именами
        for i in range(3):
            data = self.dao.create_schema(**{
                **self.create_data,
                "manufacturer_name": f"{self.create_data['manufacturer_name']}-{i}"
            })
            print('data ===== ',data)
            await self.dao.add(session=db_session, **data.model_dump())

        filters = self.dao.filter_schema(**self.filter_data) if self.filter_data else None
        instances = await self.dao.find_all(db_session, filters=filters)
        assert len(instances) >= 1

    @pytest.mark.asyncio
    async def test_update_one_by_id(self, db_session: AsyncSession):
        created = await self.test_create(db_session)
        update_values = self.dao.update_schema(**self.update_data)
        updated = await self.dao.update_one_by_id(db_session, created.id, update_values)
        assert updated is not None
        for key, value in update_values.model_dump(exclude_unset=True).items():
            assert getattr(updated, key) == value

    @pytest.mark.asyncio
    async def test_delete(self, db_session: AsyncSession):
        created = await self.test_create(db_session)
        result = await self.dao.delete(db_session, created.id)
        assert "message" in result

        # Проверяем, что объект действительно удален (или помечен как удаленный)
        deleted = await self.dao.find_one_or_none_by_id(created.id, db_session)
        assert deleted is None or getattr(deleted, "deleted_at", None) is not None

    @pytest.mark.asyncio
    async def test_soft_delete(self, db_session: AsyncSession):
        if not hasattr(self.dao.model, "deleted_at"):
            pytest.skip("Soft-delete не поддерживается этой моделью")

        created = await self.test_create(db_session)
        await self.dao.delete(db_session, created.id)

        # Проверка, что find_one_or_none_by_id больше не находит запись
        assert await self.dao.find_one_or_none_by_id(created.id, db_session) is None

