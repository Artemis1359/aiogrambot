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
                callback_data=f"good_{good.get('id')}"))
        keyboard.add(InlineKeyboardButton(text='Назад', callback_data='start_catalog'))
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_good(good: dict):
        """Клавиатура внутри полной информации о товаре."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(
            text='Добавить в корзину',
            callback_data=f"b_g_{good.get('measurement')}_{good.get('price')}_{good.get('id')}"))
        keyboard.add(InlineKeyboardButton(
            text='Назад',
            callback_data=f"category_{good.get('category_id')}"))
        return keyboard.adjust(1).as_markup()