from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class InlineBasket:


    @staticmethod
    async def inline_goods_in_basket():
        """Клавиатура в просмотре корзины."""
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='Оформить заказ', callback_data='back_to_start'))
        keyboard.add(InlineKeyboardButton(text='Изменить количество', callback_data='back_to_start'))
        keyboard.add(InlineKeyboardButton(text='Удалить позицию', callback_data='back_to_start'))
        keyboard.add(InlineKeyboardButton(text='⬅ Назад', callback_data='back_to_start'))
        return keyboard.adjust(1).as_markup()

