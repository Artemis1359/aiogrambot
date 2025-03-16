from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class InlineBasket:

    @staticmethod
    async def inline_quantity_in_basket(good_id: int, measure: str, price: int):
        """Клавиатура выбора количества товаров в зависимости от единицы измерения."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='1', callback_data=f'b_add_1_{price}_{good_id}'))
        keyboard.add(InlineKeyboardButton(text='2', callback_data=f'b_add_2_{price}_{good_id}'))
        keyboard.add(InlineKeyboardButton(text='3', callback_data=f'b_add_3_{price}_{good_id}'))
        keyboard.add(InlineKeyboardButton(text='4', callback_data=f'b_add_4_{price}_{good_id}'))
        keyboard.add(InlineKeyboardButton(text='Другое', callback_data=f'b_{measure}_{good_id}'))
        keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'good_{good_id}'))
        return keyboard.adjust(2).as_markup()

    @staticmethod
    async def inline_goods_in_basket():
        """Клавиатура в просмотре корзины."""
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='Оформить заказ', callback_data='back_to_start'))
        keyboard.add(InlineKeyboardButton(text='Изменить количество', callback_data='back_to_start'))
        keyboard.add(InlineKeyboardButton(text='Удалить позицию', callback_data='back_to_start'))
        keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_to_start'))
        return keyboard.adjust(1).as_markup()

