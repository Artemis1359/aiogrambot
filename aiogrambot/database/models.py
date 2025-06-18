import enum
from datetime import datetime
from email.policy import default

from aiogrambot.database.db import Base
from sqlalchemy import ForeignKey, func, UniqueConstraint, CheckConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated, Optional


intpk=Annotated[int, mapped_column(primary_key=True)]

class Users(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[intpk] = mapped_column(BigInteger, unique=True)
    name: Mapped[Optional[str]]
    phone_number: Mapped[Optional[str]]
    is_admin: Mapped[bool] = mapped_column(default=False)


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[intpk]
    name: Mapped[str]
    parent_cat: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id', ondelete='SET NULL'))
    is_parent: Mapped[bool]  = mapped_column(default=False)

class Measurement(enum.Enum):
    kg = 'кг.'
    g5 = '500 г.'
    piece = 'шт.'
    l6 = '0,6 л.'
    l5 = '0,5 л.'
    p10 = '10 шт.'


class Goods(Base):
    __tablename__ = 'goods'

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('categories.id', ondelete='CASCADE'))
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
    comment: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=datetime.now)
    status: Mapped[BasketStatuses]


class GoodsBaskets(Base):
    __tablename__ = 'goods_baskets'
    id: Mapped[intpk]
    good_id: Mapped[int] = mapped_column(ForeignKey('goods.id', ondelete="CASCADE"))
    price: Mapped[int]
    basket_id: Mapped[int] = mapped_column(ForeignKey('baskets.id', ondelete="CASCADE"))
    quantity: Mapped[int]

    __table_args__ = (
        UniqueConstraint("basket_id", "good_id", name="uix_basket_good"),
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('price > 0', name='check_price_positive')
    )


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[intpk]
    client_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id', ondelete="CASCADE"))
    basket_id: Mapped[int] = mapped_column(ForeignKey('baskets.id', ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=datetime.now)
    status: Mapped[OrderStatuses]