# tests/crud/test_product.py
# pytest tests/crud/test_product.py -v

import pytest
from app.crud.product import ProductDAO
from app.schemas.product import SProductAdd, SProductUpdate
from app.models.product import Product
from app.models.manufacturer import Manufacturer
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_product(db_session: AsyncSession):
    # Arrange
    manufacturer = await db_session.execute(
        Manufacturer.__table__.insert().values(manufacturer_name="Test Manufacturer", is_valid=True).returning(Manufacturer)
    )
    manufacturer_id = manufacturer.scalar().id

    dao = ProductDAO()
    new_product = SProductAdd(
        product_name="Test Product",
        manufacturer_id=manufacturer_id,
        artikul="123456",
        is_moderated=False,
        name_full="Full Test Product Name"
    )

    # Act
    created = await dao.add(session=db_session, **new_product.model_dump())

    # Assert
    assert created.id is not None
    assert created.product_name == "Test Product"
    assert created.manufacturer_id == manufacturer_id

@pytest.mark.asyncio
async def test_get_product_by_id(db_session: AsyncSession):
    # Arrange
    manufacturer = await db_session.execute(
        Manufacturer.__table__.insert().values(manufacturer_name="Another Manufacturer", is_valid=True).returning(Manufacturer)
    )
    manufacturer_id = manufacturer.scalar().id

    product = await db_session.execute(
        Product.__table__.insert().values(
            product_name="GetById Product",
            manufacturer_id=manufacturer_id,
            artikul="789012",
            is_moderated=False,
            name_full="Full GetById Product"
        ).returning(Product)
    )
    product_id = product.scalar().id

    # Act
    result = await ProductDAO().find_one_or_none_by_id(data_id=product_id, session=db_session)

    # Assert
    assert result is not None
    assert result.product_name == "GetById Product"

@pytest.mark.asyncio
async def test_update_product(db_session: AsyncSession):
    # Arrange
    manufacturer = await db_session.execute(
        Manufacturer.__table__.insert().values(manufacturer_name="Update Manufacturer", is_valid=True).returning(Manufacturer)
    )
    manufacturer_id = manufacturer.scalar().id

    product = await db_session.execute(
        Product.__table__.insert().values(
            product_name="Old Product Name",
            manufacturer_id=manufacturer_id,
            artikul="OLD123",
            is_moderated=False,
            name_full="Old Full Name"
        ).returning(Product)
    )
    product_id = product.scalar().id

    # Act
    update_data = SProductUpdate(product_name="New Product Name", artikul="NEW456")
    updated = await ProductDAO().update_one_by_id(session=db_session, data_id=product_id, values=update_data)

    # Assert
    assert updated.product_name == "New Product Name"
    assert updated.artikul == "NEW456"