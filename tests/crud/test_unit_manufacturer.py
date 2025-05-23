#test_unit_manufacturer.py
# pytest test_unit_manufacturer.py -v


from unittest.mock import AsyncMock
import pytest
from app.crud.manufacturer import ManufacturerDAO
from app.schemas.manufacturer import SManufacturerAdd
from app.models.manufacturer import Manufacturer


async def test_create_manufacturer_unit(db_session):
    dao = ManufacturerDAO()
    data = SManufacturerAdd(manufacturer_name="Apple", is_valid=True)

    # Мокаем метод .add(), чтобы не работать с БД
    dao.add = AsyncMock(return_value=Manufacturer(id=1, manufacturer_name="Apple", is_valid=True))

    manufacturer = await dao.add(session=db_session, **data.model_dump())

    assert manufacturer.id == 1
    dao.add.assert_awaited_once_with(session=db_session, **data.model_dump())


