from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogrambot.database.repository import GoodBasket


class InlineBasket:


    @staticmethod
    async def inline_goods_in_basket(basket_id: int):
        """Клавиатура в просмотре корзины."""
        keyboard = InlineKeyboardBuilder()
        # keyboard.add(InlineKeyboardButton(text='Оформить заказ', callback_data='back_to_start'))
        keyboard.add(InlineKeyboardButton(text='Изменить количество', callback_data=f'edit_menu_{basket_id}'))
        keyboard.add(InlineKeyboardButton(text='Удалить позицию', callback_data=f'del_menu_{basket_id}'))
        # keyboard.add(InlineKeyboardButton(text='⬅ Назад', callback_data='back_to_start'))
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_del_good_in_basket(telegram_id: int, basket_id: int):
        """Клавиатура выбора товара для удаления из корзины."""

        keyboard = InlineKeyboardBuilder()
        goods = await GoodBasket.select_goods_in_basket(telegram_id=telegram_id)
        for good in goods:
            good_id = good.get('id')
            name = good.get('name')
            keyboard.add(InlineKeyboardButton(text=name, callback_data=f'del_pos_{good_id}_{basket_id}'))
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_edit_good_in_basket(telegram_id: int):
        """Клавиатура выбора товара для изменения количества в корзине."""

        keyboard = InlineKeyboardBuilder()
        goods = await GoodBasket.select_goods_in_basket(telegram_id=telegram_id)
        for good in goods:
            good_id = good.get('id')
            name = good.get('name')
            quantity = good.get('quantity')
            keyboard.add(InlineKeyboardButton(text=name, callback_data=f'good_b_{quantity}_{good_id}'))
        return keyboard.adjust(1).as_markup()

    @staticmethod
    async def inline_edit_quantity(good: dict, quantity: int):
        """Клавиатура изменения количества товара."""

        good_id = good.get('id')
        price = good.get('price')

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='➖', callback_data=f'q_good_b_{quantity - 1}_{good_id}'))
        keyboard.add(InlineKeyboardButton(text=f'{quantity}', callback_data="noop"))
        keyboard.add(InlineKeyboardButton(text='➕', callback_data=f'q_good_b_{quantity + 1}_{good_id}'))
        keyboard.add(InlineKeyboardButton(
            text='✅ Изменить',
            callback_data=f"b_add_b_{quantity}_{price}_{good_id}"))
        keyboard.add(InlineKeyboardButton(text='⬅ Назад', callback_data=f'back_to_basket'))
        return keyboard.adjust(3).as_markup()

    @staticmethod
    async def inline_back_to_basket():
        """Клавиатура в просмотре корзины."""
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='⬅ Назад', callback_data='back_to_basket'))
        return keyboard.adjust(1).as_markup()