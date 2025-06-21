from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogrambot.database.models import Measurement
from aiogrambot.database.repository import Admin, Category, Good, User


class InlineAdmin:

    # @staticmethod
    # async def inline_is_admin(telegram_id: int):
    #     """Стартовая клавиатура."""
    #
    #     keyboard = InlineKeyboardBuilder()
    #     keyboard.add(
    #         InlineKeyboardButton(text='🛒 Каталог', callback_data='back_to_catalog'),
    #         InlineKeyboardButton(text='🧺 Корзина', callback_data='back_to_basket'),
    #         InlineKeyboardButton(text='Контакты', callback_data='start_contacts')
    #     )
    #     is_admin = await Admin.is_user_admin(telegram_id=telegram_id)
    #     if is_admin:
    #         keyboard.add(
    #             InlineKeyboardButton(text='💼 Админ-панель', callback_data='admin')
    #         )
    #
    #     return keyboard.adjust(1).as_markup()

    @staticmethod
    async def admin_panel():
        """Клавиатура Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text='🍑 Товары', callback_data='admin_goods'),
            InlineKeyboardButton(text='📚 Категории', callback_data='admin_categories'),
            InlineKeyboardButton(text='👤 Пользователи', callback_data='admin_users'),
            # InlineKeyboardButton(text='⬅ Назад', callback_data='back_to_start')
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
            InlineKeyboardButton(text='Восстановить товар', callback_data='recover_good'),
            InlineKeyboardButton(text='⬅ Назад', callback_data='back_to_admin')
        )
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def admin_categories():
        """Клавиатура категорий в Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text='Добавить категорию', callback_data='add_cat'),
            InlineKeyboardButton(text='Добавить подкатегорию', callback_data='add_subcat'),
            InlineKeyboardButton(text='Изменить категорию', callback_data='edit_cat'),
            InlineKeyboardButton(text='Изменить подкатегорию', callback_data='edit_subcat'),
            InlineKeyboardButton(text='Удалить категорию/подкатегорию', callback_data='del_cat'),
            InlineKeyboardButton(text='Восстановить категорию/подкатегорию', callback_data='recover_cat'),
            InlineKeyboardButton(text='⬅ Назад', callback_data='back_to_admin')
        )
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def admin_users():
        """Клавиатура пользователей в Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text='Назначить админа', callback_data='add_adm'),
            InlineKeyboardButton(text='Удалить админа', callback_data='del_adm'),
            InlineKeyboardButton(text='⬅ Назад', callback_data='back_to_admin')
        )
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_admin_categories(prefix: str, is_active: bool = True):
        """
        Клавиатура категорий в админке.
        Для изменения, удаления, восстановления и добавления подкатегорий.
        """

        keyboard = InlineKeyboardBuilder()
        categories = await Category.select_categories()
        if prefix == 'e_admin_subcat':
            categories = await Category.select_all_subcategories()
        elif prefix == 'd_admin_cat':
            status = int(not is_active)
            prefix = f'd_admin_cat_{status}'
            categories = await Category.select_all_from_categories(is_active=is_active)

        for category in categories:
            callback_data = f"{prefix}_{category.get('id')}"
            keyboard.add(InlineKeyboardButton(
                text=category.get('name'), callback_data=callback_data))
        keyboard.add(InlineKeyboardButton(text='⬅ Назад', callback_data='admin_categories'))
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_admin_good_categories(edit:bool=False, good_id:int=None):
        """Клавиатура для выбора категории при добавлении товара в Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        categories = await Category.select_all_categories()
        if edit:
            callback_text = f'update_good_cat_{good_id}'
        else:
            callback_text = 'admin_category_add'
        for category in categories:
            keyboard.add(InlineKeyboardButton(
                text=category.get('name'),
                callback_data=f"{callback_text}_{category.get('id')}"))
        keyboard.add(InlineKeyboardButton(text='⬅ Назад', callback_data='admin_goods'))

        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_admin_goods_measurement():
        """Клавиатура для выбора единицы измерения при добавлении товара в Админ-панели."""

        keyboard = InlineKeyboardBuilder()

        for measure in Measurement:
            keyboard.add(InlineKeyboardButton(text=measure.value, callback_data=f'admin_good_add_{measure.name}'))
        keyboard.add(InlineKeyboardButton(text='⬅ Назад', callback_data='admin_goods'))

        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_admin_goods(is_active:bool = True, edit:bool = False):
        """Клавиатура для выбора товара при изменении/удалении/восстановление товара в Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        goods = await Good.select_all_goods(is_active=is_active)
        if edit:
            callback_text = f'admin_good_edit'
        else:
            status = int(bool(not is_active))
            callback_text = f'admin_good_status_{status}'

        for good in goods:
            keyboard.add(InlineKeyboardButton(text=good.get('name'),
                                              callback_data=f"{callback_text}_{good.get('id')}"))
        keyboard.add(InlineKeyboardButton(text='⬅ Назад', callback_data='admin_goods'))
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def admin_goods_edit(good_id:int):
        """Клавиатура изменения товара в Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text='Изменить название', callback_data=f'edit_good_name_{good_id}'),
            InlineKeyboardButton(text='Изменить цену', callback_data=f'edit_good_price_{good_id}'),
            InlineKeyboardButton(text='Изменить единицу измерения', callback_data=f'edit_good_measurement_{good_id}'),
            InlineKeyboardButton(text='Изменить категорию/подкатегорию', callback_data=f'edit_good_cat_{good_id}'),
            InlineKeyboardButton(text='⬅ Назад', callback_data='admin_goods')
        )
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_admin_users(action: str):
        """Клавиатура для выбора пользователей при назначении и снятии прав в Админ-панели."""

        keyboard = InlineKeyboardBuilder()
        is_admin = int(action == 'del')
        users = await User.select_users_admin(is_admin=is_admin)
        for user in users:
            keyboard.add(InlineKeyboardButton(
                text=f"{user.get('name')} {user.get('phone_number')}",
                callback_data=f"admin_user_{is_admin}_{user.get('telegram_id')}"))
        keyboard.add(InlineKeyboardButton(text='⬅ Назад', callback_data='admin_users'))

        return keyboard.adjust(1).as_markup()