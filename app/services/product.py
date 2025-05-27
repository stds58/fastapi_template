
#from app.models.product import Product
#from app.models.manufacturer import Manufacturer
#from app.crud.manufacturer import ManufacturerDAO
from app.crud.product import ProductDAO
from app.schemas.product import SProduct, SProductAdd, SProductFilter
#from app.dictionaries.filtr import FiltrProduct, FiltrManufacturer
#from app.session_maker import get_session_with_isolation
#from app.users.router import verify_keycloak_token
from app.dependencies.get_db import connection
from sqlalchemy.ext.asyncio import AsyncSession



async def fetch_all_products(filters: SProductFilter, session: AsyncSession):
    # Пример бизнес-логики: проверка прав пользователя, дополнительная обработка
    # if not await check_user_permissions(...):
    #     raise HTTPException(status_code=403, detail="Нет доступа")
    products = await ProductDAO.find_all_opt(session=session, options=None, filters=filters)
    return products

