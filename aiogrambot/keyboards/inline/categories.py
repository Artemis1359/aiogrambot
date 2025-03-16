from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogrambot.database.repository import Category



class InlineCategory:

    @staticmethod
    async def inline_categories():
        """Клавиатура в каталоге."""

        keyboard = InlineKeyboardBuilder()
        categories = await Category.select_categories()
        for category in categories:
            keyboard.add(InlineKeyboardButton(text=category[1], callback_data=f'category_{category[0]}'))
        keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_to_start'))
        return keyboard.adjust(1).as_markup()

    # @staticmethod
    # async def inline_categories_admin():
    #
    #     keyboard = InlineKeyboardBuilder()
    #     categories = await Category.select_categories()
    #     for category in categories:
    #         keyboard.add(InlineKeyboardButton(text=category[1], callback_data=f'category_{category[1]}_{category[0]}'))
    #     keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_to_start'))
    #     return keyboard.adjust(1).as_markup()  # 2 это число кнопок в строке as_markup() всегда в конце
