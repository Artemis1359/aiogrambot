from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

import aiogrambot.keyboards.reply as reply
from aiogrambot.database.repository import Good, Category
from aiogrambot.keyboards.inline import InlineAdmin
from aiogrambot.states.admin import AddGood

users_router = Router()

@users_router.callback_query(F.data == 'admin_users')
async def admin_users(callback: CallbackQuery):
    """Открывает панель администратора с действиями по пользователям."""

    await callback.answer('Вы выбрали Пользователи!')
    await callback.message.edit_text("Выберите действие",
        reply_markup=await InlineAdmin.admin_users())

@users_router.callback_query(F.data == 'add_adm')
async def add_adm(callback: CallbackQuery):
    await callback.answer('Вы выбрали Назначить админа')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())

@users_router.callback_query(F.data == 'del_adm')
async def del_adm(callback: CallbackQuery):
    await callback.answer('Вы выбрали Удалить админа!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())
