import asyncio
import enum

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert


from aiogrambot.database.db import async_session, engine
from aiogrambot.database.models import Base, Categories, Goods, Baskets, BasketStatuses, GoodsBaskets, Users


class Category:

    @staticmethod
    async def select_categories():
        async with async_session() as session:

            query = """
                    SELECT id, name, is_parent
                    FROM categories
                    WHERE parent_cat IS NULL;
                    """
            result = await session.execute(text(query))
            categories = result.mappings().all()
            return categories


    @staticmethod
    async def select_subcategories(parent_cat: int):
        async with async_session() as session:
            query = """
                        SELECT id, name
                        FROM categories
                        WHERE parent_cat =:parent_cat;
                        """
            result = await session.execute(text(query), {'parent_cat': parent_cat})
            categories = result.mappings().all()
            return categories


    @staticmethod
    async def select_is_subcat(category_id: int):
        async with async_session() as session:
            query = """
                            SELECT parent_cat
                            FROM categories
                            WHERE id =:category_id
                                AND parent_cat IS NOT NULL;
                            """
            result = await session.execute(text(query), {'category_id': category_id})
            categories = result.mappings().first()
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
            goods = result.mappings().all()
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
            good = result.mappings().first()
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

    @staticmethod
    async def select_basket(telegram_id: int):
        async with async_session() as session:
            query = """
                            SELECT 
                                id
                            FROM baskets
                            WHERE
                                status = 'created'
                                and client_id =:telegram_id;
                            """
            result = await session.execute(text(query), {'telegram_id': telegram_id})
            good = result.fetchone()
            return good

    @staticmethod
    async def create_new_basket(telegram_id: int):
        async with async_session() as session:
            basket = Baskets(
                client_id=telegram_id,
                status=BasketStatuses.created
            )
            session.add(basket)
            await session.commit()
            return basket.id

class GoodBasket:

    @staticmethod
    async def input_good_to_basket(basket_id: int, good_id: int, quantity: int, price: int):
        async with async_session() as session:
            stmt = insert(GoodsBaskets).values(
                basket_id=basket_id,
                good_id=good_id,
                quantity=quantity,
                price=price
            ).on_conflict_do_update(
                index_elements=["basket_id", "good_id"],
                set_={
                    "quantity": quantity,
                    "price": price
                }
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def select_goods_in_basket(telegram_id: int):
        async with async_session() as session:
            query = """
                                SELECT 
                                    goods.name,
                                    goods_baskets.price,
                                    quantity,
                                    goods_baskets.price * quantity as amount
                                FROM goods_baskets
                                JOIN baskets
                                    on baskets.id=goods_baskets.basket_id
                                    AND baskets.status = 'created'
                                    AND client_id =:telegram_id
                                JOIN goods
                                    on goods.id=goods_baskets.good_id
                                """
            result = await session.execute(text(query), {'telegram_id': telegram_id})
            good = result.mappings().all()
            return good

class Order:
    pass

class User:

    @staticmethod
    async def select_user(telegram_id: int):
        async with async_session() as session:

            query = """
                    SELECT id
                    FROM users
                    WHERE 
                        telegram_id=:telegram_id;
                    """
            result = await session.execute(text(query), {'telegram_id': telegram_id})
            id = result.mappings().first()
            return id

    @staticmethod
    async def input_user(telegram_id: int):
        async with async_session() as session:
            user = Users(
                telegram_id=telegram_id
            )
            session.add(user)
            await session.commit()

