#модели Pydantic  https://habr.com/ru/companies/amvera/articles/851642/
from datetime import datetime, date
from typing import Optional, List
import re
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator, model_validator, computed_field
from app.schemas.base import BaseConfigModel, BaseFilter


class SProduct(BaseConfigModel):
    model_config = ConfigDict(from_attributes=True, max_recursion_depth=1)
    id: int
    product_name: str = Field(..., description="наименование")
    manufacturer_id: Optional[int] = Field(None, ge=1, description="производитель")
    manufacturer: Optional['SManufacturer'] = Field(None, description="вложенная схема производителя")
    artikul: Optional[str] = Field(None, description="артикул")
    #subcategory_id: Optional[int] = Field(None, ge=1, description="подкатегория")
    #dimension_id: Optional[int] = Field(None, ge=1, description="ед изм")
    comment_text: Optional[str] = Field(None, description="комментарий")
    date_create: datetime = Field(..., description="дата создания")
    is_moderated: bool = Field(..., description="изменено")
    date_moderated: datetime = Field(..., description="дата изменения")
    name_full: Optional[str] = Field(None, description="полное наименование")
    parent_id: Optional[int] = Field(None, ge=1, description="псевдоним")


class SProductAdd(BaseConfigModel):
    product_name: str = Field(..., description="наименование")
    manufacturer_id: Optional[int] = Field(None, ge=1, description="производитель")
    artikul: Optional[str] = Field(None, description="артикул")
    #subcategory_id: Optional[int] = Field(None, ge=1, description="подкатегория")
    #dimension_id: Optional[int] = Field(None, ge=1, description="ед изм")
    comment_text: Optional[str] = Field(None, description="комментарий")
    is_moderated: bool = Field(..., description="изменено")
    name_full: Optional[str] = Field(None, description="полное наименование")
    parent_id: Optional[int] = Field(None, ge=1, description="псевдоним")

class SProductUpdate(BaseConfigModel):
    product_name: Optional[str] = None
    manufacturer_id: Optional[int] = Field(None, ge=1)
    artikul: Optional[str] = None
    is_moderated: Optional[bool] = None
    name_full: Optional[str] = None
    parent_id: Optional[int] = None

class SProductFilter(BaseFilter):
    id: Optional[int] = None
    product_name: Optional[str] = None
    manufacturer_id: Optional[int] = None
    artikul: Optional[str] = None
    #subcategory_id: Optional[int] = None
    #dimension_id: Optional[int] = None
    comment_text: Optional[str] = None
    #date_create: datetime | None = None,
    is_moderated: Optional[bool] = None
    #date_moderated: datetime | None = None,
    name_full: Optional[str] = None
    parent_id: Optional[int] = None
