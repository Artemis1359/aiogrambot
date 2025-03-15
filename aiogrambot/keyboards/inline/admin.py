from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogrambot.database.repository import Admin, Category


class InlineAdmin:

    @staticmethod
    async def inline_is_admin(telegram_id: int):
        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text='Каталог', callback_data='catalog'),
            InlineKeyboardButton(text='Корзина', callback_data='basket'),
            InlineKeyboardButton(text='Контакты', callback_data='contacts')
        )
        is_admin = await Admin.is_user_admin(telegram_id=telegram_id)
        print(is_admin)
        if is_admin:
            keyboard.add(
                InlineKeyboardButton(text='Админ-панель', callback_data='admin')
            )

        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def admin_panel():
        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text='Добавить товар', callback_data='add_good'),
            InlineKeyboardButton(text='Изменить товар', callback_data='edit_good'),
            InlineKeyboardButton(text='Удалить товар', callback_data='del_good'),
            InlineKeyboardButton(text='Добавить категорию', callback_data='add_cat'),
            InlineKeyboardButton(text='Изменить категорию', callback_data='edit_cat'),
            InlineKeyboardButton(text='Назначить админа', callback_data='add_adm'),
            InlineKeyboardButton(text='Удалить админа', callback_data='del_adm'),
            InlineKeyboardButton(text='Назад', callback_data='back_to_start')
        )
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_admin_categories():

        keyboard = InlineKeyboardBuilder()
        categories = await Category.select_categories()
        for category in categories:
            keyboard.add(InlineKeyboardButton(text=category[1], callback_data=f'admin_category_add_{category[0]}'))
        return keyboard.adjust(1).as_markup()  # 2 это число кнопок в строке as_markup() всегда в конце

