"""
pytest tests/crud/test_dao_manufacturer.py -v

Как увидеть print() в тестах?
pytest tests/crud/test_dao_manufacturer.py -v -s
pytest tests/crud/test_dao_manufacturer.py -v --capture=no
"""
from app.crud.manufacturer import ManufacturerDAO
from tests.crud.test_dao import BaseDAOTestCase


class TestManufacturerDAO(BaseDAOTestCase):
    @classmethod
    def setup_class(cls):
        super().setup_class(
            dao=ManufacturerDAO,
            create_data={"manufacturer_name": "Apple", "is_valid": True},
            update_data={"manufacturer_name": "Samsung"},
            filter_data={"is_valid": True}
        )

