
from aiogrambot.database.repository import GoodBasket, Order
import re

PHONE_REGEX = re.compile(r"^\+7\d{10}$")

async def basket_text(data, order: bool = False):
    """Возвращает данные по корзине пользователя."""

    # amount = 0
    text = ''
    if not order:
        text = f'В корзине:\n\n'
    for good in data:
        text += (f" - {good.get('name')}\n    ({int(good.get('quantity'))} × {int(good.get('price'))}₽) - "
                 f"{int(good.get('amount'))}₽\n\n")
        # amount += int(good.get('amount'))
    # text += f'💰 *Итого* {amount}₽'
    return text

async def order_text(telegram_id:int,
                     name: str, number: str,
                     comment: str):

    goods = await GoodBasket.select_goods_in_basket(telegram_id)
    text = await basket_text(goods, order=True)
    order_text = (
        f"🧾 <b>Новый заказ<b>\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {number}\n"
        f"📝 Комментарий: {comment}\n"
        f"🛍 Состав заказа:\n\n"
        f"{text}")
    return order_text

async def admin_order_text(order_id: int):

    order_info = await Order.select_order_info(order_id=order_id)
    name = order_info.get('name')
    number = order_info.get('phone_number')
    basket_id = order_info.get('basket_id')
    comment = order_info.get('comment')
    goods = await GoodBasket.select_goods_by_basket(basket_id=basket_id)

    text = await basket_text(goods, order=True)
    order_text = (
        f"🧾 *Заказ №{order_id}*\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {number}\n"
        f"📝 Комментарий: {comment}\n"
        f"🛍 Состав заказа:\n\n"
        f"{text}")
    return order_text

async def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone))