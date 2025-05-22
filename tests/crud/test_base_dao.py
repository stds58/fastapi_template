# pytest tests/crud/test_base_dao.py -v


import pytest
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models.product import Product
from app.models.manufacturer import Manufacturer
from app.schemas.product import SProductAdd, SProductUpdate, SProductFilter
from app.crud.base import BaseDAO
from conftest import TestingSessionLocal

#
# class TestDAO(BaseDAO[Product, SProductAdd, SProductUpdate, SProductFilter]):
#     model = Product
#     create_schema = SProductAdd
#     update_schema = SProductUpdate
#     filter_schema = SProductFilter
#
#
# @pytest.mark.asyncio
# async def test_add(setup_database):
#     async with TestingSessionLocal() as session:
#         async with session.begin():
#             data = SProductAdd(
#                 product_name="Test Product",
#                 manufacturer_id=1,
#                 artikul="ART12345",
#                 is_moderated=False
#             )
#             result = await TestDAO.add(session=session, **data.model_dump())
#             assert result.product_name == data.product_name
#             assert result.manufacturer_id == data.manufacturer_id
#
#
# @pytest.mark.asyncio
# async def test_find_one_or_none(setup_database):
#     async with TestingSessionLocal() as session:
#         async with session.begin():
#             # Добавляем через DAO
#             added = await TestDAO.add(session=session, product_name="Find Me", manufacturer_id=1, is_moderated=False)
#             filters = SProductFilter(product_name="Find Me")
#             result = await TestDAO.find_one_or_none(session=session, filters=filters)
#             assert result is not None
#             assert result.id == added.id
#
#
# @pytest.mark.asyncio
# async def test_find_all(setup_database):
#     async with TestingSessionLocal() as session:
#         async with session.begin():
#             names = ["Item 1", "Item 2", "Item 3"]
#             for name in names:
#                 await TestDAO.add(session=session, product_name=name, manufacturer_id=1, is_moderated=False)
#
#             items = await TestDAO.find_all(session=session, filters=None)
#             assert len(items) >= 3
#
#
# @pytest.mark.asyncio
# async def test_update_one_by_id(setup_database):
#     async with TestingSessionLocal() as session:
#         async with session.begin():
#             added = await TestDAO.add(session=session, product_name="Old Name", manufacturer_id=1, is_moderated=False)
#             update_data = SProductUpdate(product_name="New Name")
#             result = await TestDAO.update_one_by_id(session=session, data_id=added.id, values=update_data)
#             assert result.product_name == "New Name"
#
#
# @pytest.mark.asyncio
# async def test_delete(setup_database):
#     async with TestingSessionLocal() as session:
#         async with session.begin():
#             added = await TestDAO.add(session=session, product_name="ToDelete", manufacturer_id=1, is_moderated=False)
#             result = await TestDAO.delete(session=session, id=added.id)
#             assert "мягко удален" in result["message"] or "удален" in result["message"]
#
#             deleted = await TestDAO.find_one_or_none_by_id(session=session, data_id=added.id)
#             assert deleted is None
#
#
# @pytest.mark.asyncio
# async def test_soft_delete(setup_database):
#     async with TestingSessionLocal() as session:
#         async with session.begin():
#             added = await TestDAO.add(session=session, product_name="SoftDeleteMe", manufacturer_id=1, is_moderated=False)
#             await TestDAO.delete(session=session, id=added.id)
#
#             query = select(Product).where(Product.id == added.id, Product.deleted_at.is_not(None))
#             result = await session.execute(query)
#             assert result.scalars().first() is not None
#
#             result = await TestDAO.find_one_or_none(session=session, filters=SProductFilter(product_name="SoftDeleteMe"))
#             assert result is None
#
#
# @pytest.mark.asyncio
# async def test_filtering(setup_database):
#     async with TestingSessionLocal() as session:
#         async with session.begin():
#             names = ["Apple", "Banana", "Cherry"]
#             for name in names:
#                 await TestDAO.add(session=session, product_name=name, manufacturer_id=1, is_moderated=False)
#
#             results = await TestDAO.find_all(session=session, filters=SProductFilter(product_name="Apple"))
#             assert len(results) == 1
#             assert results[0].product_name == "Apple"
#
#
# @pytest.mark.asyncio
# async def test_update_many_by_filtr(setup_database):
#     async with TestingSessionLocal() as session:
#         async with session.begin():
#             for i in range(3):
#                 await TestDAO.add(session=session, product_name=f"Old{i}", manufacturer_id=1, is_moderated=False)
#
#             filters = SProductFilter(product_name="Old0")
#             updates = SProductUpdate(comment_text="Updated Desc")
#
#             updated_records = await TestDAO.update_many_by_filtr(session=session, filters=filters, values=updates)
#             assert len(updated_records) == 1
#             assert updated_records[0].comment_text == "Updated Desc"
#
