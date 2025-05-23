from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.get_db import connection
from app.api.v1.manufacturer import router as manufacturer_router
from app.api.v1.product import router as product_router
from sqlalchemy.ext.asyncio import AsyncSession


# Основной роутер для версии v1
v1_router = APIRouter(prefix="/v1/dictionaries")

# Подключение модульных роутеров
v1_router.include_router(manufacturer_router, prefix="/manufacturers", tags=["справочник"])
v1_router.include_router(product_router, prefix="/products", tags=["продукция"])


