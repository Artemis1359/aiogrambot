from aiogram import F, Router

from aiogram.types import CallbackQuery

from aiogrambot.database.repository import User
from aiogrambot.keyboards.inline import InlineAdmin
from aiogrambot.keyboards.reply import main_page
from aiogrambot.utils.user_helpers import admin_required

users_router = Router()

@users_router.callback_query(F.data == 'admin_users')
@admin_required
async def admin_users(callback: CallbackQuery):
    """Открывает панель администратора с действиями по пользователям."""

    await callback.answer('Вы выбрали Пользователи!')
    await callback.message.edit_text("Выберите действие",
        reply_markup=await InlineAdmin.admin_users())

@users_router.callback_query(F.data == 'add_adm')
@admin_required
async def add_adm(callback: CallbackQuery):
    await callback.answer('Вы выбрали Назначить админа')
    await callback.message.edit_text(
        'Выберите пользователя',
        reply_markup=await InlineAdmin.inline_admin_users(action='add'))

@users_router.callback_query(F.data == 'del_adm')
@admin_required
async def del_adm(callback: CallbackQuery):
    await callback.answer('Вы выбрали Удалить админа!')
    await callback.message.edit_text(
        'Выберите пользователя',
        reply_markup=await InlineAdmin.inline_admin_users(action='del'))

@users_router.callback_query(F.data.startswith('admin_user_'))
@admin_required
async def admin_user(callback: CallbackQuery):

    telegram_id = int(callback.data.split('_')[-1])
    is_admin = bool(not int(callback.data.split('_')[-2]))

    await User.update_role(telegram_id, is_admin)
    await callback.message.edit_text(
        f"✅ Статус пользователя обновлен.",
        reply_markup=await InlineAdmin.admin_panel())
    keyboard = await main_page(telegram_id)
    await callback.bot.send_message(
        chat_id=telegram_id, text="Статус пользователя обновлен.\nНовая клавиатура:", reply_markup=keyboard)

