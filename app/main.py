from fastapi import FastAPI, HTTPException, Request
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

#from app.models import Item
#from app.schemas import ItemCreate, ItemResponse
from sqlalchemy.orm import Session
#from app.database import engine, Base, AsyncSessionLocal, get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy import text
#from app  all import connection, Product, get_db
from app.api.v1.base_router import v1_router
from fastapi.responses import JSONResponse
import traceback
import logging
logging.basicConfig(level=logging.DEBUG)
#app = FastAPI(debug=settings.DEBUG)
app = FastAPI(debug=settings.app.DEBUG, title="API", version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# http://localhost:8000/api/v1/dictionaries/manufacturers/all/
# Подключаем версию API
app.include_router(v1_router, prefix="/api")

@app.get("/test")
def test():
    return {"message": "Hello, world"}


# @app.get("/items/")
# async def read_items(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Product))
#     items = result.scalars().all()
#     return items

# @connection(isolation_level="READ COMMITTED", commit=False)
# async def get_products(session: AsyncSession = None):
#     result = await session.execute(select(Product))
#     return result.scalars().all()
#
# @app.get("/items/")
# async def read_items():
#     items = await get_products()
#     return {"data": items}


# @app.get("/items/", response_model=list[ItemResponse])
# async def read_items(db: AsyncSession = Depends(get_db)):
#     # Добавляем 2 тестовые записи, если их ещё нет
#     await db.execute(
#         insert(Item).values([
#             {"name": "Test Item 01", "description": "This is item 01"},
#             {"name": "Test Item 02", "description": "This is item 02"}
#         ])
#     )
#     await db.commit()
#
#     result = await db.execute(select(Item))
#     items = result.scalars().all()
#     return items
#
# @app.get("/test-db")
# async def test_db(db: AsyncSession = Depends(get_db)):
#     try:
#         await db.execute(text("SELECT 1"))
#         return {"status": "OK"}
#     except Exception as e:
#         return {"status": "ERROR", "detail": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, host="localhost", port=8000)
    #uvicorn.run("main:app", reload=True)