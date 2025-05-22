# tests/crud/test_manufacturer.py
# pytest tests/crud/test_manufacturer.py -v
# alembic -x db=test upgrade head

from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from app.crud.manufacturer import ManufacturerDAO
from app.schemas.manufacturer import SManufacturerAdd


@pytest.mark.asyncio
async def test_create_manufacturer(db_session):
    # Подготавливаем данные
    data = SManufacturerAdd(manufacturer_name="Apple", is_valid=True)

    # Вызываем DAO через экземпляр класса
    manufacturer = await ManufacturerDAO().add(session=db_session, **data.model_dump())

    # Проверяем результат
    assert manufacturer.id is not None
    assert manufacturer.manufacturer_name == "Apple"
    assert manufacturer.is_valid is True

