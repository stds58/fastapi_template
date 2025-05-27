from fastapi import APIRouter, Depends, HTTPException, Query
from app.dependencies.get_db import connection
from app.services.manufacturer import fetch_all_manufacturers
from app.schemas.manufacturer import SManufacturerFilter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Annotated



#router = APIRouter()
router = APIRouter()

# @router.get("/all")
# async def get_products(
#         manufacturer_name: Optional[str] = Query(None),
#         is_valid: Optional[bool] = Query(None),
#         id: Optional[int] = Query(None),
#         #filters: Optional[SManufacturerFilter] = Depends(),
#         session: AsyncSession = ReadOnlyDB
#     ):
#     print('ppppppppppppppppppppp')
#     filters = SManufacturerFilter(
#         manufacturer_name=manufacturer_name,
#         is_valid=is_valid,
#         id=id
#     )
#     manufacturers = await fetch_all_manufacturers(filters=filters, session=session)
#     return {"data": manufacturers}

@router.get("/all")
async def get_manufacturers(
        filters: SManufacturerFilter = Depends(),
        session: AsyncSession = Depends(connection())
    ):
    """isolation_level:READ COMMITTED, REPEATABLE READ, SERIALIZABLEж commit=False"""
    manufacturers = await fetch_all_manufacturers(filters=filters, session=session)
    return {"data": manufacturers}
