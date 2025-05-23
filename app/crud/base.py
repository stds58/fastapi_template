"""
класс с универсальными методами по работе с базой данных.

- ModelType: мы можем задать границу типа, т.о. мы будем уверены при статическом анализе,
  что использованы верные типы как минимум в иерархии
- assert issubclass(Base, DeclarativeBase) ,"Base должна наследоваться от DeclarativeBase"

Python < 3.12:
import typing
T = typing.TypeVar("T", bound=Base) # мы можем задать границу типа, т.о. мы будем уверены при статическом анализе
                                      что использованы верные типы как минимум в иерархии
class BaseDAO(typing.Generic[T]):
    model: type[T]
Python >= 3.12:
# точно так же можно задать границу дженерика
class BaseDAO[T: Base]:
    model: type[T]

- async def update: Когда вы загружаете объект из БД через session.execute(query) и scalars().first(),
                    SQLAlchemy начинает отслеживать изменения этого объекта.
                    Как только вы изменяете его атрибуты через setattr(...),
                    SQLAlchemy помечает их как "грязные" (dirty) и при вызове await session.flush()
                    автоматически генерирует и выполняет соответствующий SQL-запрос UPDATE.
                    Это называется Unit of Work паттерн: вы работаете с объектами,
                    а SQLAlchemy сама заботится о синхронизации изменений с БД.
"""

from datetime import datetime
from typing import Optional, List, Dict, TypeVar, Any, Generic, ClassVar, AsyncGenerator
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload, class_mapper, declarative_base, DeclarativeBase
from fastapi import HTTPException
from pydantic import BaseModel as PydanticModel
from app.db.base import Base


assert issubclass(Base, DeclarativeBase)

ModelType = TypeVar("ModelType", bound=Base)
#FilterType = TypeVar("FilterType", bound=PydanticModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=PydanticModel)

class SoftDeleteMixin:
    model: type[DeclarativeBase]  # Должен быть переопределен в потомке

    @classmethod
    def _build_query(cls, filters: dict = None) -> Select:
        query = select(cls.model)
        if filters:
            query = query.filter_by(**filters)
        return cls._apply_soft_delete(query)

    @classmethod
    def _apply_soft_delete(cls, query: Select) -> Select:
        """
        Применяет фильтр `deleted_at IS NULL`, если модель поддерживает soft-delete.
        """
        if hasattr(cls.model, "deleted_at"):
            return query.where(cls.model.deleted_at.is_(None))
        return query

class FiltrMixin:
    model: type[DeclarativeBase]

    @classmethod
    def _apply_filters(cls, query, filters: FilterSchemaType):
        """игнорирование полей фильтрации, которых нет в модели"""
        allowed_fields = cls.filter_schema.model_fields.keys()
        filter_dict = {
            k: v for k, v in filters.model_dump().items()
            if k in allowed_fields and v is not None
        }
        return query.filter_by(**filter_dict)


class BaseDAO(SoftDeleteMixin, FiltrMixin, Generic[ModelType, CreateSchemaType, UpdateSchemaType, FilterSchemaType]):
    model: ClassVar[type[ModelType]]
    create_schema: ClassVar[type[CreateSchemaType]]
    update_schema: ClassVar[type[UpdateSchemaType]]
    filter_schema: ClassVar[type[FilterSchemaType]]

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: FilterSchemaType) -> List[ModelType]:
        query = select(cls.model)
        query = cls._apply_soft_delete(query)
        if filters is not None:
            query = cls._apply_filters(query, filters)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_all_opt(cls, session: AsyncSession, options: Optional[List[Any]] = None, filters: FilterSchemaType = None) -> List[PydanticModel]:
        query = select(cls.model)
        query = cls._apply_soft_delete(query)
        if filters is not None:
            query = cls._apply_filters(query, filters)
        if options:
            query = query.options(*options)
        result = await session.execute(query)
        results = result.unique().scalars().all()  # Получаем все записи
        return [cls.pydantic_model.model_validate(obj, from_attributes=True) for obj in results]

    @classmethod
    async def find_all_stream(cls,
                              session: AsyncSession,
                              options: Optional[List[Any]] = None,
                              filters: FilterSchemaType = None
                             ) -> AsyncGenerator[ModelType, None]:
        query = select(cls.model)
        query = cls._apply_soft_delete(query)
        if filters is not None:
            query = cls._apply_filters(query, filters)
        if options:
            query = query.options(*options)
        stream = await session.stream_scalars(query)
        async for record in stream:
            yield record
        #Можно добавить документацию про использование в больших датасетах.

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, options: Optional[List[Any]] = None, filters: FilterSchemaType = None) -> Optional[ModelType]:
        query = select(cls.model)
        query = cls._apply_soft_delete(query)
        if filters is not None:
            query = cls._apply_filters(query, filters)
        if options:
            query = query.options(*options)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession) -> Optional[PydanticModel]:
        if hasattr(cls.model, "deleted_at"):
            query = select(cls.model).where(
                cls.model.id == data_id,
                cls.model.deleted_at.is_(None)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
        else:
            return await session.get(cls.model, data_id)

    @classmethod
    async def add(cls, session: AsyncSession, **values) -> ModelType:
        new_instance = cls.model(**values)
        session.add(new_instance)
        await session.flush()
        await session.refresh(new_instance)
        return new_instance

    @classmethod
    async def update_one_by_id(cls, session: AsyncSession, data_id: int, values: UpdateSchemaType) -> Optional[ModelType]:
        query = select(cls.model).where(cls.model.id == data_id)
        query = cls._apply_soft_delete(query)

        result = await session.execute(query)
        instance = result.scalars().first()

        if not instance:
            raise HTTPException(status_code=404, detail=f"Объект с ID {data_id} не найден")

        values_dict = values.model_dump(exclude_unset=True)
        for key, value in values_dict.items():
            setattr(instance, key, value)

        await session.flush()
        return instance

    @classmethod
    async def update_many_by_filtr(cls,
                                   session: AsyncSession,
                                   filters: FilterSchemaType,
                                   values: UpdateSchemaType
                                   ) -> List[Optional[PydanticModel]]:
        values_dict = values.model_dump(exclude_unset=True)
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}

        # Начинаем формировать запрос
        stmt = sqlalchemy_update(cls.model).filter_by(**filter_dict).values(**values_dict)

        stmt = cls._apply_soft_delete(stmt)

        # Используем RETURNING для получения обновлённых записей
        stmt = stmt.returning(cls.model)

        # Выполняем запрос и получаем результат
        result = await session.execute(stmt)
        updated_records = result.scalars().all()

        # Фиксируем изменения
        await session.flush()

        # Возвращаем Pydantic-объекты
        return [
            cls.pydantic_model.model_validate(record, from_attributes=True)
            for record in updated_records
        ]

    @classmethod
    async def delete_old(cls, session: AsyncSession, id: int) -> dict:
        """физически удаляет запись из бд,даже помеченную как удалённую"""
        query = sqlalchemy_delete(cls.model).filter_by(id=id)
        result = await session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Объект с ID {id} не найден")
        return {"message": f"Объект с id {id} удален!", "deleted_count": result.rowcount}
        #Можно добавить поддерж soft-delete через флаг deleted_at.

    @classmethod
    async def delete(cls, session: AsyncSession, id: int) -> dict:
        """soft-delete"""
        obj = await session.get(cls.model, id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"Объект с ID {id} не найден")

        if hasattr(obj, "deleted_at"):
            obj.deleted_at = datetime.utcnow()
            await session.flush()
            return {"message": f"Объект с ID {id} мягко удален"}
        else:
            query = sqlalchemy_delete(cls.model).where(cls.model.id == id)
            result = await session.execute(query)
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Объект с ID {id} не найден")
            return {"message": f"Объект с ID {id} удален", "deleted_count": result.rowcount}


