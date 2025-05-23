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
from app.models.product import Product
from app.schemas.product import SProduct, SProductAdd, SProductUpdate, SProductFilter



class ProductDAO(BaseDAO[Product, SProductAdd, SProductUpdate, SProductFilter, SProduct]):
    model = Product
    create_schema = SProductAdd
    update_schema = SProductUpdate
    filter_schema = SProductFilter
    pydantic_model = SProduct


