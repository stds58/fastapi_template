from sqlalchemy import ForeignKey, text, Text, UniqueConstraint, Index, func, CheckConstraint, column
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref
from typing import List, Optional
from sqlalchemy import String, Boolean
from app.db.base import (Base, str_uniq, int_pk, str_null_true, created_at, updated_at,
                          bool_null_false, fk_protect_nullable)



class Manufacturer(Base):
    id: Mapped[int_pk]
    manufacturer_name: Mapped[str] = mapped_column(info={"verbose_name": "производитель"})
    is_valid: Mapped[bool_null_false] = mapped_column(info={"verbose_name": "производитель работает"})

    product: Mapped[List["Product"]] = relationship("Product", back_populates="manufacturer")

    __table_args__ = (
        Index('uix_manufacturer_name_lower', func.lower(column('manufacturer_name')), unique=True),
        CheckConstraint("access_id > 0", name="access_id_positive_number_check"),
    )

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"manufacturer_name={self.manufacturer_name!r})")

    def __repr__(self):
        return str(self)

    def to_dict(self) -> dict:
        return {'id': self.id,
                'manufacturer_name': self.manufacturer_name,
                'is_valid': self.is_valid
                }

