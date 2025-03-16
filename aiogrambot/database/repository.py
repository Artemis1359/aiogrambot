import asyncio
from sqlalchemy import insert, text

from aiogrambot.database.db import async_session, engine
from aiogrambot.database.models import Base, Categories, Goods

class Category:

    @staticmethod
    async def select_categories():
        async with async_session() as session:

            query = """
                    SELECT id, name
                    FROM categories;
                    """
            result = await session.execute(text(query))
            categories = result.fetchall()
            return categories

    @staticmethod
    async def input_category(data):
        async with async_session() as session:
            category = Categories(
                name=data.get('name')
            )
            session.add(category)
            await session.commit()

class Good:

    @staticmethod
    async def input_good(data):
        async with async_session() as session:
            good = Goods(
                name=data.get('name'),
                description=data.get('description'),
                measurement=data.get('measurement'),
                category_id=data.get('category_id'),
                price=data.get('price'),
                image_id=data.get('image_id')
            )
            session.add(good)
            await session.commit()

    @staticmethod
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

    @staticmethod
    async def select_good(good_id: int):
        async with async_session() as session:
            query = """
                            SELECT 
                                id, name, description, 
                                price, measurement,
                                category_id, image_id
                            FROM goods
                            WHERE
                                id =:good_id;
                            """
            result = await session.execute(text(query), {'good_id': good_id})
            good = result.fetchone()
            return good

class Admin:
    @staticmethod
    async def is_user_admin(telegram_id: int):
        async with async_session() as session:
            query = """
                            SELECT 
                                is_admin
                            FROM users
                            WHERE
                                telegram_id =:telegram_id;
                            """
            result = await session.execute(text(query), {'telegram_id': telegram_id})
            is_admin = result.fetchone()
            if is_admin:
                is_admin=is_admin[0]
            return is_admin

class Basket:
    pass

class Order:
    pass

