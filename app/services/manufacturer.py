
#from app.models.product import Product
#from app.models.manufacturer import Manufacturer
from app.crud.manufacturer import ManufacturerDAO
from app.schemas.manufacturer import SManufacturer, SManufacturerAdd, SManufacturerUpdate, SManufacturerUpdateById, SManufacturerFilter
#from app.dictionaries.filtr import FiltrProduct, FiltrManufacturer
#from app.session_maker import get_session_with_isolation
#from app.users.router import verify_keycloak_token
from app.dependencies.get_db import connection
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_all_manufacturers(filters: SManufacturerFilter, session: AsyncSession):
    print('filters========',filters)
    # Пример бизнес-логики: проверка прав пользователя, дополнительная обработка
    # if not await check_user_permissions(...):
    #     raise HTTPException(status_code=403, detail="Нет доступа")
    manufacturers = await ManufacturerDAO.find_all_opt(session=session, options=None, filters=filters)
    return manufacturers

