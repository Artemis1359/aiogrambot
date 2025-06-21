from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogrambot.database.repository import Category
from aiogrambot.keyboards.inline.admin import InlineAdmin
from aiogrambot.states.admin import AddCategory
from aiogrambot.utils.user_helpers import admin_required

categories_router = Router()

@categories_router.callback_query(F.data == 'admin_categories')
@admin_required
async def admin_categories(callback: CallbackQuery):
    """Открывает панель администратора с действиями по категориям."""

    await callback.answer('Вы выбрали Категории!')
    await callback.message.edit_text("Выберите действие",
        reply_markup=await InlineAdmin.admin_categories())

@categories_router.callback_query(F.data == 'add_cat')
@admin_required
async def add_cat(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали Добавить категорию!')
    await callback.message.edit_text("Чтобы добавить категорию, напишите её название.")
    await state.set_state(AddCategory.waiting_for_name)
    await state.update_data(action="add_category")

@categories_router.callback_query(F.data == 'add_subcat')
@admin_required
async def add_subcat(callback: CallbackQuery):
    await callback.answer('Вы выбрали Добавить подкатегорию!')
    await callback.message.edit_text(
        'Чтобы добавить подкатегорию, выберите категорию:',
        reply_markup=await InlineAdmin.inline_admin_categories(prefix='admin_subcat'))

@categories_router.callback_query(F.data.startswith('admin_subcat_'))
@admin_required
async def admin_subcat(callback: CallbackQuery, state: FSMContext):

    parent_cat = int(callback.data.split('_')[-1])

    await callback.message.edit_text('Чтобы добавить подкатегорию, напишите её название.')
    await state.set_state(AddCategory.waiting_for_name)
    await state.update_data(action="add_subcategory", parent_cat=parent_cat)

@categories_router.callback_query(F.data == 'edit_cat')
@admin_required
async def edit_cat(callback: CallbackQuery):
    await callback.answer('Вы выбрали Изменить категорию!')
    await callback.message.edit_text(
        'Выберите категорию:',
        reply_markup=await InlineAdmin.inline_admin_categories(prefix='e_admin_сat'))

@categories_router.callback_query(F.data.startswith('e_admin_сat_'))
@admin_required
async def admin_cat_e(callback: CallbackQuery, state: FSMContext):

    cat = int(callback.data.split('_')[-1])

    await callback.message.edit_text('Чтобы изменить категорию, напишите новое название.')
    await state.set_state(AddCategory.waiting_for_name)
    await state.update_data(action="edit_category", cat=cat)

@categories_router.callback_query(F.data == 'edit_subcat')
@admin_required
async def edit_subcat(callback: CallbackQuery):
    await callback.answer('Вы выбрали Изменить подкатегорию!')
    await callback.message.edit_text(
        'Выберите подкатегорию:',
        reply_markup=await InlineAdmin.inline_admin_categories(prefix='e_admin_subcat'))

@categories_router.callback_query(F.data == 'del_cat')
@admin_required
async def del_cat(callback: CallbackQuery):
    await callback.answer('Вы выбрали Удалить категорию!')
    await callback.message.edit_text(
        'ВНИМАНИЕ, ЕСЛИ В КАТЕГОРИИ ЕСТЬ ТОВАРЫ - В КАТАЛОГЕ ИХ НЕ БУДЕТ ВИДНО. '
        'МОЖНО ПЕРЕНЕСТИ В АДМИНКЕ.\nВыберите категорию/подкатегорию:',
        reply_markup=await InlineAdmin.inline_admin_categories(prefix='d_admin_cat', is_active=True))

@categories_router.callback_query(F.data == 'recover_cat')
@admin_required
async def recover_cat(callback: CallbackQuery):
    await callback.answer('Вы выбрали Восстановить категорию!')
    await callback.message.edit_text(
        'Выберите категорию/подкатегорию:',
        reply_markup=await InlineAdmin.inline_admin_categories(prefix='d_admin_cat', is_active=False))

@categories_router.callback_query(F.data.startswith('d_admin_cat_'))
@admin_required
async def d_admin_cat(callback: CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split('_')[-1])
    is_active = int(callback.data.split('_')[-2])

    name = await Category.update_is_active_category({'id': cat_id, 'is_active': is_active})

    if is_active:
        text = f"✅ Категория восстановлена!\nНазвание: {name}\nВыберите дальнейшее действие"

    else:
        text = f"✅ Категория удалена!\nНазвание: {name}\nВыберите дальнейшее действие"

    await callback.message.edit_text(text, reply_markup=await InlineAdmin.admin_panel())


@categories_router.callback_query(F.data.startswith('e_admin_subcat_'))
@admin_required
async def admin_subcat_e(callback: CallbackQuery, state: FSMContext):

    subcat = int(callback.data.split('_')[-1])

    await callback.message.edit_text('Чтобы изменить подкатегорию, напишите новое название.')
    await state.set_state(AddCategory.waiting_for_name)
    await state.update_data(action="edit_subcategory", subcat=subcat)


@categories_router.message(AddCategory.waiting_for_name)
@admin_required
async def process_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)

    data = await state.get_data()
    action = data.get("action")

    if action == "add_category":
        await Category.input_category({"name": name})
        text = f"✅ Категория создана!\nНазвание: {name}\nВыберите дальнейшее действие"

    elif action == "add_subcategory":
        await Category.input_subcategory({"name": name, "parent_cat": data['parent_cat']})
        text = f"✅ Подкатегория создана!\nНазвание: {name}\nВыберите дальнейшее действие"

    elif action == "edit_category":
        await Category.update_category({"name": name, "cat_id": data['cat']})
        text = f"✅ Категория изменена!\nНазвание: {data['name']}\nВыберите дальнейшее действие"

    elif action == "edit_subcategory":
        await Category.update_subcategory({"name": name, "subcat_id": data['subcat']})
        text = f"✅ Подкатегория изменена!\nНазвание: {data['name']}\nВыберите дальнейшее действие"

    else:
        text = "❌ Неизвестное действие"

    await message.edit_text(text, reply_markup=await InlineAdmin.admin_panel())
    await state.clear()
