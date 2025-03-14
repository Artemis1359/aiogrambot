import asyncio
from sqlalchemy import insert, text

from aiogrambot.database.db import async_session, engine
from aiogrambot.database.models import Base, Categories, Goods




async def select_categories():
    async with async_session() as session:

        query = """
                SELECT id, name
                FROM categories;
                """
        result = await session.execute(text(query))
        categories = result.fetchall()
        return categories


async def select_goods(category_id: int):
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

async def select_good(good_id: int):
    async with async_session() as session:
        query = """
                        SELECT 
                            id, name, description, 
                            price, measurement,
                            image_id
                        FROM goods
                        WHERE
                            id =:good_id;
                        """
        result = await session.execute(text(query), {'good_id': good_id})
        good = result.fetchall()
        return good


result = asyncio.run(select_good(good_id=5))
print(result)
