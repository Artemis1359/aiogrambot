from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class InlineOrder:

    @staticmethod
    async def inline_make_order():
        """Клавиатура при оформлении заказа."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='👤 Изменить имя', callback_data=f'order_name'))
        keyboard.add(InlineKeyboardButton(text='📞 Изменить номер', callback_data=f'order_number'))
        keyboard.add(InlineKeyboardButton(text='📝 Изменить комментарий', callback_data=f'order_comment'))
        keyboard.add(InlineKeyboardButton(text='✅ Оформить', callback_data=f'order_confirm'))


        return keyboard.adjust(1).as_markup()