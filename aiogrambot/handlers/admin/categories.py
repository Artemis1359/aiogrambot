from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

import aiogrambot.keyboards.reply as reply
from aiogrambot.database.repository import Category
from aiogrambot.keyboards.inline.admin import InlineAdmin
from aiogrambot.states.admin import AddCategory

categories_router = Router()

@categories_router.callback_query(F.data == 'admin_categories')
async def admin_categories(callback: CallbackQuery):
    """Открывает панель администратора с действиями по категориям."""

    await callback.answer('Вы выбрали Категории!')
    await callback.message.edit_text("Выберите действие",
        reply_markup=await InlineAdmin.admin_categories())

@categories_router.callback_query(F.data == 'add_cat')
async def add_cat(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали Добавить категорию!')
    await callback.message.edit_text("Чтобы добавить категорию, напишите её название.")
    await state.set_state(AddCategory.waiting_for_name)

@categories_router.message(AddCategory.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)  # Сохраняем имя товара

    data = await state.get_data()

    await message.answer(
        f"""
                Категория создана!
                Название: {data['name']}

                Выберите дальнейшее действие
            """,
        reply_markup=await InlineAdmin.admin_panel())
    await Category.input_category(data)
    await state.clear()


@categories_router.callback_query(F.data == 'edit_cat')
async def edit_cat(callback: CallbackQuery):
    await callback.answer('Вы выбрали Изменить категорию!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())