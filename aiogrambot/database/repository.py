import asyncio
import enum

from sqlalchemy import text, delete, update
from sqlalchemy.dialects.postgresql import insert


from aiogrambot.database.db import async_session, engine
from aiogrambot.database.models import Base, Categories, Goods, Baskets, BasketStatuses, GoodsBaskets, Users, Orders, \
    OrderStatuses


class Category:

    @staticmethod
    async def select_categories():
        async with async_session() as session:

            query = """
                    SELECT id, name, is_parent
                    FROM categories
                    WHERE parent_cat IS NULL
                    ORDER BY id;
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
                        WHERE parent_cat =:parent_cat
                        ORDER BY id;
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
                        category_id =:category_id
                    ORDER BY id;
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
            basket = result.mappings().first()
            return basket

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

    @staticmethod
    async def select_comment_basket(telegram_id: int):
        async with async_session() as session:
            query = """
                                SELECT 
                                    comment
                                FROM baskets
                                WHERE
                                    status = 'created'
                                    and client_id =:telegram_id;
                                """
            result = await session.execute(text(query), {'telegram_id': telegram_id})
            comment = result.mappings().first()
            return comment

    @staticmethod
    async def input_comment(telegram_id: int, comment: str):
        async with async_session() as session:
            await session.execute(
                update(Baskets)
                .where(Baskets.client_id == telegram_id,
                       Baskets.status == 'created'
                       )
                .values(comment=comment))
            await session.commit()

    @staticmethod
    async def update_basket_status(basket_id: int):
        async with async_session() as session:
            await session.execute(
                update(Baskets)
                .where(Baskets.id == basket_id
                       )
                .values(status='collected'))
            await session.commit()


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
                        goods.id,
                        goods_baskets.basket_id,
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

    @staticmethod
    async def select_goods_by_basket(basket_id: int):
        async with async_session() as session:
            query = """
                    SELECT 
                        goods.id,
                        goods_baskets.basket_id,
                        goods.name,
                        goods_baskets.price,
                        quantity,
                        goods_baskets.price * quantity as amount
                    FROM goods_baskets
                    JOIN baskets
                        on baskets.id=goods_baskets.basket_id
                    JOIN goods
                        on goods.id=goods_baskets.good_id
                    WHERE goods_baskets.basket_id =:basket_id
                    """
            result = await session.execute(text(query), {'basket_id': basket_id})
            good = result.mappings().all()
            return good

    @staticmethod
    async def delete_all_goods_from_basket(basket_id: int):
        async with async_session() as session:
            stmt = delete(GoodsBaskets).where(GoodsBaskets.basket_id == basket_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def delete_good_from_basket(basket_id: int, good_id: int):
        async with async_session() as session:
            stmt = delete(GoodsBaskets).where(
                GoodsBaskets.basket_id == basket_id,
                GoodsBaskets.good_id == good_id
            )
            await session.execute(stmt)
            await session.commit()


class Order:

    @staticmethod
    async def create_new_order(telegram_id: int, basket_id: int):
        async with async_session() as session:
            order = Orders(
                client_id=telegram_id,
                basket_id=basket_id,
                status=OrderStatuses.created
            )
            session.add(order)
            await session.commit()
            return order.id

    @staticmethod
    async def select_order_info(order_id: int):
        async with async_session() as session:
            query = """
                    SELECT 
                        users.name,
                        users.phone_number,
                        baskets.id as basket_id,
                        baskets.comment
                    FROM orders
                    JOIN users
                        ON users.telegram_id = orders.client_id
                    JOIN baskets 
                        ON baskets.id = orders.basket_id
                    WHERE
                        orders.id =:order_id;
                    """
            result = await session.execute(text(query), {'order_id': order_id})
            order = result.mappings().first()
            return order

class User:

    @staticmethod
    async def select_user(telegram_id: int):
        async with async_session() as session:

            query = """
                    SELECT telegram_id
                    FROM users
                    WHERE 
                        telegram_id=:telegram_id;
                    """
            result = await session.execute(text(query), {'telegram_id': telegram_id})
            user_id = result.mappings().first()
            return user_id

    @staticmethod
    async def select_user_info(telegram_id: int):
        async with async_session() as session:
            query = """
                        SELECT name, phone_number
                        FROM users
                        WHERE 
                            telegram_id=:telegram_id;
                        """
            result = await session.execute(text(query), {'telegram_id': telegram_id})
            user_info = result.mappings().all()
            return user_info

    @staticmethod
    async def input_user(telegram_id: int):
        async with async_session() as session:
            user = Users(
                telegram_id=telegram_id
            )
            session.add(user)
            await session.commit()

    @staticmethod
    async def input_phone_number(telegram_id: int, phone_number: str):
        async with async_session() as session:
            await session.execute(
                update(Users)
                .where(Users.telegram_id == telegram_id)
                .values(phone_number=phone_number))
            await session.commit()

    @staticmethod
    async def input_name(telegram_id: int, name: str):
        async with async_session() as session:
            await session.execute(
                update(Users)
                .where(Users.telegram_id == telegram_id)
                .values(name=name))
            await session.commit()


