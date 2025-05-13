import enum
from datetime import datetime
from email.policy import default

from aiogrambot.database.db import Base
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated, Optional


intpk=Annotated[int, mapped_column(primary_key=True)]

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[Optional[str]]
    phone_number: Mapped[Optional[str]]
    is_admin: Mapped[bool] = mapped_column(default=False)


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[intpk]
    name: Mapped[str]

class Measurement(enum.Enum):
    kg = 'кг.'
    piece = 'шт.'
    l6 = '0,6 л.'
    l5 = '0,5 л.'


class Goods(Base):
    __tablename__ = 'goods'

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('categories.id', ondelete='SET NULL'))
    price: Mapped[int]
    measurement: Mapped[Measurement]
    image_id: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)


class BasketStatuses(enum.Enum):
    created = 'Создана'
    collected = 'Собрана'


class OrderStatuses(enum.Enum):
    created = 'Создан'
    canceled = 'Отменен'
    closed = 'Закрыт'


class Baskets(Base):
    __tablename__ = 'baskets'

    id: Mapped[intpk]
    client_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=datetime.now)
    status: Mapped[BasketStatuses]


class GoodsBaskets(Base):
    __tablename__ = 'goods_baskets'
    id: Mapped[intpk]
    good_id: Mapped[int] = mapped_column(ForeignKey('goods.id'))
    price: Mapped[int]
    basket_id: Mapped[int] = mapped_column(ForeignKey('baskets.id'))
    quantity: Mapped[float]


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[intpk]
    client_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))
    basket_id: Mapped[int] = mapped_column(ForeignKey('baskets.id'))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=datetime.now)
    Status: Mapped[OrderStatuses]