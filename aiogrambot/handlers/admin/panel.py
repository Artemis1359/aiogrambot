from aiogram import F, Router
from aiogram.types import  CallbackQuery
from aiogrambot.keyboards.inline.admin import InlineAdmin
from aiogrambot.utils.user_helpers import admin_required

admin_router = Router()

@admin_router.callback_query(F.data == 'back_to_admin')
@admin_required
async def admin_panel(callback: CallbackQuery):
    """Открывает панель администратора"""

    await callback.answer('Вы выбрали Админ-панель!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())
