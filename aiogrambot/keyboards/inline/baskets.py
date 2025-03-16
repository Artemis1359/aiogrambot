from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class InlineBasket:

    @staticmethod
    async def inline_quantity_in_basket(good_id: int, measure: str):
        """Клавиатура выбора количества товаров в зависимости от единицы измерения."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='1', callback_data=f'basket_add_1_{good_id}'))
        keyboard.add(InlineKeyboardButton(text='2', callback_data=f'basket_add_2_{good_id}'))
        keyboard.add(InlineKeyboardButton(text='3', callback_data=f'basket_add_3_{good_id}'))
        keyboard.add(InlineKeyboardButton(text='4', callback_data=f'basket_add_4_{good_id}'))
        keyboard.add(InlineKeyboardButton(text='Другое', callback_data=f'basket_{measure}_{good_id}'))
        keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'good_{good_id}'))
        return keyboard.adjust(2).as_markup()

