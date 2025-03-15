from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogrambot.database.repository import Good

class InlineGood:

    @staticmethod
    async def inline_goods(category_id: int):

        keyboard = InlineKeyboardBuilder()
        goods = await Good.select_goods(category_id=category_id)
        for good in goods:
            keyboard.add(InlineKeyboardButton(
                text=f'{good[1]} - {good[2]}р / {good[3]}',
                callback_data=f'good_{good[0]}'))
        keyboard.add(InlineKeyboardButton(text='Назад', callback_data='catalog'))
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_good(good: tuple):

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'category_{good[5]}'))
        return keyboard.adjust(1).as_markup()