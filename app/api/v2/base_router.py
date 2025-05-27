from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.get_db import connection
from app.api.v2.manufacturer import router as manufacturer_router
from app.api.v2.product import router as product_router
from sqlalchemy.ext.asyncio import AsyncSession


# Основной роутер для версии v1
v2_router = APIRouter(prefix="/v1/dictionaries")

# Подключение модульных роутеров
v2_router.include_router(manufacturer_router, prefix="/manufacturers", tags=["справочник"])
#v2_router.include_router(product_router, prefix="/products", tags=["продукция"])


