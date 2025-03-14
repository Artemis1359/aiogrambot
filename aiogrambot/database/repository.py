import asyncio
from sqlalchemy import insert, text

from aiogrambot.database.db import async_session, engine
from aiogrambot.database.models import Base, Categories, Goods



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def select_async():
    async with async_session() as session:

        query = """
                SELECT id, name
                FROM categories;
                """
        result = await session.execute(text(query))
        categories = result.fetchall()
        return categories


async def select_async_goods(category_id: int):
    async with async_session() as session:

        query = """
                SELECT id, name, price, measurement
                FROM goods
                WHERE
                    category_id =:category_id;
                """
        result = await session.execute(text(query), {'category_id': category_id})
        goods = result.fetchall()
        return goods


async def input_async():
    async with async_session() as session:
 

        category1 = Categories(
            id=1,
            name="Соленья и заправки")
        category2 = Categories(
            id=2,
            name="Блины")
        category3 = Categories(
            id=3,
            name="Пельмени и хинкали")
        category4 = Categories(
            id=4,
            name="Котлеты и зразы")
        session.add_all([category1, category2,
                         category3, category4])
        await session.commit()

async def input_async_good():
    async with async_session() as session:
        good1 = Goods(
            name="Заправка для борща",
            description="",
            category_id=1,
            price=250,
            measurement="0,5 л.",
            image_id=""
        )
        good2 = Goods(
            name="Огурцы маринованные",
            description="",
            category_id=1,
            price=220,
            measurement="0,6 л.",
            image_id=""
        )
        good3 = Goods(
            name="Баклажаны в аджике",
            description="",
            category_id=1,
            price=300,
            measurement="0,5 л.",
            image_id=""
        )
        good4 = Goods(
            name="Аджика из кабачка",
            description="",
            category_id=1,
            price=200,
            measurement="0,5 л.",
            image_id=""
        )
        good5 = Goods(
            name="Лечо",
            description="",
            category_id=1,
            price=250,
            measurement="0,6 л.",
            image_id=""
        )
        good6 = Goods(
            name="Икра кабачковая",
            description="",
            category_id=1,
            price=200,
            measurement="0,5 л.",
            image_id=""
        )
        good7 = Goods(
            name="Огурцы в горчичной заливке",
            description="",
            category_id=1,
            price=230,
            measurement="0,5 л.",
            image_id=""
        )
        good8 = Goods(
            name="Блины с курицей",
            description="",
            category_id=2,
            price=60,
            measurement="шт.",
            image_id=""
        )
        good9 = Goods(
            name="Блины с творогом",
            description="",
            category_id=2,
            price=60,
            measurement="шт.",
            image_id=""
        )
        good10 = Goods(
            name="Пельмени с курицей",
            description="",
            category_id=3,
            price=600,
            measurement="кг.",
            image_id=""
        )
        good11 = Goods(
            name="Пельмени со свининой",
            description="",
            category_id=3,
            price=700,
            measurement="кг.",
            image_id=""
        )
        good12 = Goods(
            name="Хинкали со свининой и говядиной",
            description="",
            category_id=3,
            price=950,
            measurement="кг.",
            image_id=""
        )
        good13 = Goods(
            name="Хинкали с индейкой",
            description="",
            category_id=3,
            price=750,
            measurement="кг.",
            image_id=""
        )
        good14 = Goods(
            name="Хинкали с картошкой и зеленью",
            description="",
            category_id=3,
            price=750,
            measurement="кг.",
            image_id=""
        )
        good15 = Goods(
            name="Котлеты из курицы",
            description="",
            category_id=4,
            price=500,
            measurement="кг.",
            image_id=""
        )
        good16 = Goods(
            name="Котлеты свинные",
            description="",
            category_id=4,
            price=600,
            measurement="кг.",
            image_id=""
        )
        good17 = Goods(
            name="Зразы с яйцом",
            description="",
            category_id=4,
            price=620,
            measurement="кг.",
            image_id=""
        )
        session.add_all([good1, good2, good3, good4,
                        good5, good6, good7, good8,
                         good9, good10, good11, good12,
                         good13, good14, good15, good16,
                         good17])
        await session.commit()

# result = asyncio.run(select_async_goods(category_id=3))
# print(result)
# from aiogrambot.config import settings
#
# print(settings.get_db_url())

# from pathlib import Path
#
# print(Path(__file__).resolve().parents[2])