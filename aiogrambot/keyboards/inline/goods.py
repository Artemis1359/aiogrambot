from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
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
                text=f'{good[1]} - {good[2]}р / {Measurement[good[3]].value}',
                callback_data=f'good_{good[0]}'))
        keyboard.add(InlineKeyboardButton(text='Назад', callback_data='start_catalog'))
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_good(good: tuple):
        """Клавиатура внутри полной информации о товаре."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='Добавить в корзину', callback_data=f'b_g_{good[4]}_{good[3]}_{good[0]}'))
        keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'category_{good[5]}'))
        return keyboard.adjust(1).as_markup()