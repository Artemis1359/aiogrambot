from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

import aiogrambot.keyboards.reply as reply
from aiogrambot.database.repository import Good, Category
from aiogrambot.keyboards.inline import InlineAdmin
from aiogrambot.states.admin import AddGood

admin_router = Router()

@admin_router.callback_query(F.data == 'admin')
async def admin_panel(callback: CallbackQuery):
    await callback.answer('Вы выбрали Админ-панель!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())


@admin_router.callback_query(F.data == 'add_good')
async def add_good(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали Добавить товар!')
    await callback.message.edit_text("Чтобы добавить товар, напишите его название.")
    await state.set_state(AddGood.waiting_for_name)

@admin_router.message(AddGood.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)  # Сохраняем имя товара
    await message.answer("Теперь введите описание товара.")
    await state.set_state(AddGood.waiting_for_description)

@admin_router.message(AddGood.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)  # Сохраняем описание товара
    await message.answer("Теперь введите цену товара.")
    await state.set_state(AddGood.waiting_for_price)

@admin_router.message(AddGood.waiting_for_price)
async def process_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)  # Сохраняем цену товара
        await message.answer("Теперь введите в чем измеряется товар. (Например кг. или 0,6 л. и т.д.)")
        await state.set_state(AddGood.waiting_for_measurement)  # Переходим к последнему шагу
    except ValueError:
        await message.answer("Цена должна быть числом. Попробуйте еще раз.")

@admin_router.message(AddGood.waiting_for_measurement)
async def process_measurement(message: Message, state: FSMContext):
    measurement = message.text
    await state.update_data(measurement=measurement.lower())  # Сохраняем описание товара
    await message.answer("Теперь отправьте изображение товара.")
    await state.set_state(AddGood.waiting_for_image)

@admin_router.message(AddGood.waiting_for_image, F.content_type == ContentType.PHOTO)
async def process_image(message: Message, state: FSMContext):
    image_id = message.photo[-1].file_id  # Получаем ID изображения
    await state.update_data(image_id=image_id)  # Сохраняем изображение товара
    await message.answer(
        '''В какую категорию добавить товар?''',
        reply_markup=await InlineAdmin.inline_admin_categories())
    await state.set_state(AddGood.waiting_for_category)



    # Завершаем процесс и сбрасываем состояние

    await Category.select_categories()


@admin_router.callback_query(F.data.startswith('admin_category_add_'), AddGood.waiting_for_category)
async def process_category(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[-1]
    await state.update_data(category_id=int(category_id))  # Сохраняем описание товара

    data = await state.get_data()

    # Здесь можно сохранить данные в базу данных или выполнить другие действия
    await callback.message.edit_text(
        f"""
            Товар создан!
            Название: {data['name']}
            Описание: {data['description']}
            Цена: {data['price']}
            В чем измеряется: {data['measurement']}
            Изображение: {data['image_id']}
            Категория: {data['category_id']}
            
            Выберите дальнейшее действие
        """,
        reply_markup=await InlineAdmin.admin_panel())
    await Good.input_good(data)
    await state.clear()



@admin_router.callback_query(F.data == 'edit_good')
async def edit_good(callback: CallbackQuery):
    await callback.answer('Вы выбрали Изменить товар!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())

@admin_router.callback_query(F.data == 'del_good')
async def del_good(callback: CallbackQuery):
    await callback.answer('Вы выбрали Удалить товар!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())

@admin_router.callback_query(F.data == 'add_cat')
async def add_cat(callback: CallbackQuery):
    await callback.answer('Вы выбрали Добавить категорию!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())

@admin_router.callback_query(F.data == 'edit_cat')
async def edit_cat(callback: CallbackQuery):
    await callback.answer('Вы выбрали Изменить категорию!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())

@admin_router.callback_query(F.data == 'add_adm')
async def add_adm(callback: CallbackQuery):
    await callback.answer('Вы выбрали Назначить админа')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())

@admin_router.callback_query(F.data == 'del_adm')
async def del_adm(callback: CallbackQuery):
    await callback.answer('Вы выбрали Удалить админа!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())
