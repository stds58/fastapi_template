from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies.get_db import connection
from app.services.manufacturer import fetch_all_manufacturers, add_manufacturer
from app.schemas.manufacturer import SManufacturerFilter, SManufacturerAdd
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Annotated
from fastapi.templating import Jinja2Templates
from pathlib import Path
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError


V2_DIR = Path(__file__).resolve().parent
API_DIR = V2_DIR.parent
APP_DIR = API_DIR.parent
TEMPLATES_DIR = APP_DIR / "templates"

router = APIRouter(tags=['Фронтенд'])
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/all")
async def get_manufacturers(
        filters: SManufacturerFilter = Depends(),
        session: AsyncSession = Depends(connection())
    ):
    """isolation_level:READ COMMITTED, REPEATABLE READ, SERIALIZABLE; commit=False"""
    manufacturers = await fetch_all_manufacturers(filters=filters, session=session)
    return {"data": manufacturers}


MODEL_MAP = {
    "manufacturer": SManufacturerAdd
}

@router.get("/add")
async def show_add_form(request: Request, model: str = "manufacturer"):
    ModelClass = MODEL_MAP[model]
    return templates.TemplateResponse("dynamic_form.html", {
        "request": request,
        "fields": ModelClass.model_fields,
        "title": f"Добавить {model}"
    })

@router.post("/add", response_class=HTMLResponse)
async def put_manufacturer(request: Request, session: AsyncSession = Depends(connection())):
    try:
        form_data = await request.form()
        manufacturer_data = SManufacturerAdd(**dict(form_data))

        db_manufacturer = await add_manufacturer(data=manufacturer_data, session=session)

        return templates.TemplateResponse("dynamic_form.html", {
            "request": request,
            "fields": SManufacturerAdd.model_fields,
            "title": "Добавить производителя",
            "form_values": dict(form_data),
            "data": db_manufacturer # или .dict(), зависит от версии Pydantic
        })
    # except ValidationError as e:
    #     return templates.TemplateResponse("dynamic_form.html", {
    #         "request": request,
    #         "fields": SManufacturerAdd.model_fields,
    #         "title": "Добавить производителя",
    #         "form_values": dict(form_data),
    #         "errors": e.errors()
    #     })
    except ValidationError as e:
        # Ошибки валидации Pydantic
        return templates.TemplateResponse("dynamic_form.html", {
            "request": request,
            "fields": SManufacturerAdd.model_fields,
            "title": "Добавить производителя",
            "form_values": dict(form_data),
            "errors": e.errors()
        })

    except IntegrityError as e:
        # Ошибки целостности данных (включая уникальные ограничения)
        await session.rollback()
        error_msg = str(e.orig)
        if isinstance(e.orig, UniqueViolationError):
            error_msg = f"Уже существует запись: {error_msg}"
            print('error_msg ',error_msg)

        # Передаём ошибку в шаблон
        return templates.TemplateResponse("dynamic_form.html", {
            "request": request,
            "fields": SManufacturerAdd.model_fields,
            "title": "Добавить производителя",
            "form_values": dict(form_data),
            "errors": [{"loc": ["База данных"], "msg": error_msg}]
        })
# async def pull_manufacturer(data: SManufacturerAdd,session: AsyncSession = Depends(connection())):
#     manufacturer = await add_manufacturer(data=data, session=session)
#     return {"data": manufacturer}


# @router.get('/manufacturers', response_class=HTMLResponse)
# async def get_manufacturers_html(request: Request):
#     manufacturers = await fetch_all_manufacturers(SManufacturerFilter())
#     return templates.TemplateResponse(
#         name='manufacturers.html',
#         context={'request': request, 'manufacturers': manufacturers}
#     )