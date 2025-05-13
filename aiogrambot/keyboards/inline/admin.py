from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogrambot.database.models import Measurement
from aiogrambot.database.repository import Admin, Category


class InlineAdmin:

    @staticmethod
    async def inline_is_admin(telegram_id: int):
        """Стартовая клавиатура."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text='🛒 Каталог', callback_data='start_catalog'),
            InlineKeyboardButton(text='🧺 Корзина', callback_data='start_basket'),
            InlineKeyboardButton(text='Контакты', callback_data='start_contacts')
        )
        is_admin = await Admin.is_user_admin(telegram_id=telegram_id)
        print(is_admin)
        if is_admin:
            keyboard.add(
                InlineKeyboardButton(text='💼 Админ-панель', callback_data='admin')
            )

        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def admin_panel():
        """Клавиатура Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text='Товары', callback_data='admin_goods'),
            InlineKeyboardButton(text='Категории', callback_data='admin_categories'),
            InlineKeyboardButton(text='Пользователи', callback_data='admin_users'),
            InlineKeyboardButton(text='⬅ Назад', callback_data='back_to_start')
        )
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def admin_goods():
        """Клавиатура товаров в Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text='Добавить товар', callback_data='add_good'),
            InlineKeyboardButton(text='Изменить товар', callback_data='edit_good'),
            InlineKeyboardButton(text='Удалить товар', callback_data='del_good'),
            InlineKeyboardButton(text='⬅ Назад', callback_data='admin')
        )
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def admin_categories():
        """Клавиатура категорий в Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text='Добавить категорию', callback_data='add_cat'),
            InlineKeyboardButton(text='Изменить категорию', callback_data='edit_cat'),
            InlineKeyboardButton(text='⬅ Назад', callback_data='admin')
        )
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def admin_users():
        """Клавиатура пользователей в Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text='Назначить админа', callback_data='add_adm'),
            InlineKeyboardButton(text='Удалить админа', callback_data='del_adm'),
            InlineKeyboardButton(text='⬅ Назад', callback_data='admin')
        )
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_admin_categories():
        """Клавиатура для выбора категории при добавлении товара в Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        categories = await Category.select_categories()
        for category in categories:
            keyboard.add(InlineKeyboardButton(text=category.get('name'), callback_data=f"admin_category_add_{category.get('id')}"))
        return keyboard.adjust(1).as_markup()  # 2 это число кнопок в строке as_markup() всегда в конце

    @staticmethod
    async def inline_admin_goods_measurement():
        """Клавиатура для выбора единицы измерения при добавлении товара в Админ-панели."""

        keyboard = InlineKeyboardBuilder()

        for measure in Measurement:
            keyboard.add(InlineKeyboardButton(text=measure.value, callback_data=f'admin_good_add_{measure.name}'))
        return keyboard.adjust(1).as_markup()  # 2 это число кнопок в строке as_markup() всегда в конце
