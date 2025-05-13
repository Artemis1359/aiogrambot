# import asyncio
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
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
# async def cars():
#     keyboard = ReplyKeyboardBuilder()
#     cars = await select_categories()
#     for car in cars:
#         keyboard.add(KeyboardButton(text=car))
#     return keyboard.adjust(1).as_markup()
#
# async def reply_cars():
#     keyboard = ReplyKeyboardBuilder()
#     for car in cars:
#         keyboard.add(KeyboardButton(text=car))
#     return keyboard.adjust(2).as_markup() # 2 это число кнопок в строке