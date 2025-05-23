from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.get_db import connection
from app.services.product import fetch_all_products
from app.schemas.product import SProductFilter
from sqlalchemy.ext.asyncio import AsyncSession


#router = APIRouter()
router = APIRouter()

@router.get("/all")
async def get_products(filters: SProductFilter = Depends(), session: AsyncSession = Depends(connection)):
    products = await fetch_all_products(filters=filters, session=session)
    return {"data": products}



# @connection(isolation_level="READ COMMITTED", commit=False)
# async def get_products(session: AsyncSession = None):
#     result = await session.execute(select(Product))
#     return result.scalars().all()
#
# @app.get("/items/")
# async def read_items():
#     items = await get_products()
#     return {"data": items}