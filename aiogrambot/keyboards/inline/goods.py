from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogrambot.database.models import Measurement
from aiogrambot.database.repository import Good

class InlineGood:

    @staticmethod
    async def inline_goods(category_id: int):
        """Клавиатура с выбором товаров внутри категории."""

        keyboard = InlineKeyboardBuilder()
        goods = await Good.select_goods(category_id=category_id)
        for good in goods:
            keyboard.add(InlineKeyboardButton(
                text=f"{good.get('name')} - {good.get('price')}р / {Measurement[good.get('measurement')].value}",
                callback_data=f"good_1_{good.get('id')}"))
        keyboard.add(InlineKeyboardButton(text='⬅ Назад', callback_data='start_catalog'))
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_good(good: dict, quantity: int):
        """Клавиатура внутри полной информации о товаре."""

        good_id = good.get('id')
        price = good.get('price')
        category_id = good.get('category_id')

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='➖', callback_data=f'q_good_{quantity - 1}_{good_id}'))
        keyboard.add(InlineKeyboardButton(text=f'{quantity}', callback_data = "noop"))
        keyboard.add(InlineKeyboardButton(text='➕', callback_data=f'q_good_{quantity + 1}_{good_id}'))
        keyboard.add(InlineKeyboardButton(
            text='✅ Добавить',
            callback_data=f"b_add_{quantity}_{price}_{good_id}"))

        keyboard.add(InlineKeyboardButton(text='⬅ Назад', callback_data=f'category_{category_id}'))
        return keyboard.adjust(3).as_markup()
