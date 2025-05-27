#класс с универсальными методами по работе с базой данных.
from typing import Optional, List, Dict, TypeVar, Any, Generic, AsyncGenerator
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, class_mapper, declarative_base
from fastapi import HTTPException
from pydantic import BaseModel
from app.crud.base import BaseDAO
from app.models.manufacturer import Manufacturer
from app.schemas.manufacturer import SManufacturer, SManufacturerFilter, SManufacturerAdd, SManufacturerUpdate


class ManufacturerDAO(BaseDAO[Manufacturer, SManufacturerAdd, SManufacturerUpdate, SManufacturerFilter]):
    model = Manufacturer
    create_schema = SManufacturerAdd
    update_schema = SManufacturerUpdate
    filter_schema = SManufacturerFilter
    pydantic_model = SManufacturer
