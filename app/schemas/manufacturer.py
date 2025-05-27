#модели Pydantic  https://habr.com/ru/companies/amvera/articles/851642/
from datetime import datetime, date
from typing import Optional, List
import re
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator, model_validator, computed_field
from app.schemas.base import BaseConfigModel, BaseFilter



class SManufacturer(BaseConfigModel):
    id: Optional[int] = None
    manufacturer_name: Optional[str] = None
    is_valid: Optional[bool] = None

    # id: int
    # manufacturer_name: str = Field(..., description="производитель",alias="manufacturer_name_alias")
    # is_valid: bool = Field(..., description="производитель работает", exclude=True) # exclude=True Исключение полей из сериализации
    # #product: List[Optional['SProduct']] = Field(None, description="вложенная схема Product")

    # @computed_field
    # def full_name(self) -> str:
    #     return f"{self.manufacturer_name} - {self.is_valid}"


class SManufacturerAdd(BaseConfigModel):
    manufacturer_name: str = Field(..., description="производитель")
    is_valid: bool = Field(..., description="производитель работает")

    @model_validator(mode="after")
    def check_is_valid(self):
        if not isinstance(self.is_valid, bool):
            raise ValueError("Поле 'is_valid' должно быть true или false")
        return self


class SManufacturerUpdate(BaseConfigModel):
    manufacturer_name: Optional[str] = None
    is_valid: Optional[bool] = None


class SManufacturerUpdateById(BaseConfigModel):
    manufacturer_name: str = Field(..., description="производитель")
    is_valid: bool = Field(..., description="производитель работает")

class SManufacturerFilter(BaseFilter):
    id: Optional[int] = Field(default=None)
    manufacturer_name: Optional[str] = Field(default=None)
    is_valid: Optional[bool] = Field(default=None)


