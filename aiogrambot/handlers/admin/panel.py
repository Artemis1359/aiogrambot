from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from aiogrambot.database.repository import Admin
from aiogrambot.keyboards.inline.admin import InlineAdmin


admin_router = Router()

@admin_router.callback_query(F.data == 'back_to_admin')
async def admin_panel(callback: CallbackQuery):
    """Открывает панель администратора"""

    await callback.answer('Вы выбрали Админ-панель!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())


@admin_router.message(F.text == '💼 Админ-панель')
async def admin_panel(message: Message):
    """Открывает панель администратора"""

    telegram_id = message.from_user.id
    is_admin = await Admin.is_user_admin(telegram_id=telegram_id)
    if is_admin:
        await message.answer(
            'Выберите действие',
            reply_markup=await InlineAdmin.admin_panel())