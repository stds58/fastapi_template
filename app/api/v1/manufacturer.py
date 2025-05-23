from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.get_db import connection
from app.services.manufacturer import fetch_all_manufacturers
from app.schemas.manufacturer import SManufacturerFilter
from sqlalchemy.ext.asyncio import AsyncSession


#router = APIRouter()
router = APIRouter()

@router.get("/all")
async def get_products(filters: SManufacturerFilter = Depends(), session: AsyncSession = Depends(connection)):
    manufacturers = await fetch_all_manufacturers(filters=filters, session=session)
    return {"data": manufacturers}


