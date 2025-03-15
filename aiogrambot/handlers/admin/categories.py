from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

import aiogrambot.keyboards.reply as reply
from aiogrambot.database.repository import Good, Category
from aiogrambot.keyboards.inline.admin import InlineAdmin
from aiogrambot.states.admin import AddGood

categories_router = Router()

@categories_router.callback_query(F.data == 'add_cat')
async def add_cat(callback: CallbackQuery):
    await callback.answer('Вы выбрали Добавить категорию!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())

@categories_router.callback_query(F.data == 'edit_cat')
async def edit_cat(callback: CallbackQuery):
    await callback.answer('Вы выбрали Изменить категорию!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())