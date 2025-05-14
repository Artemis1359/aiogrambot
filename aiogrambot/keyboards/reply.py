# import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from aiogrambot.database.repository import Admin


# from aiogrambot.database.repository import select_categories
#
# main = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text='🛒 Каталог')],
#         [KeyboardButton(text='🧺Корзина')]
#     ],
#     resize_keyboard=True,
#     input_field_placeholder='Выберите пункт меню'
# )
#
#
#
async def main_page(telegram_id: int):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text='🛒 Каталог'))
    keyboard.add(KeyboardButton(text='🧺 Корзина'))
    keyboard.add(KeyboardButton(text='📦 Оформить заказ'))
    keyboard.add(KeyboardButton(text='🗑️ Очистить корзину'))

    is_admin = await Admin.is_user_admin(telegram_id=telegram_id)
    if is_admin:
        keyboard.add(
            KeyboardButton(text='💼 Админ-панель')
        )
    return keyboard.adjust(2).as_markup(resize_keyboard=True, input_field_placeholder="Выберите пункт меню 👇")
#
# async def reply_cars():
#     keyboard = ReplyKeyboardBuilder()
#     for car in cars:
#         keyboard.add(KeyboardButton(text=car))
#     return keyboard.adjust(2).as_markup() # 2 это число кнопок в строке