from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogrambot.database.repository import Good
from aiogrambot.keyboards.inline.admin import InlineAdmin
from aiogrambot.states.admin import AddGood, EditGood
from aiogrambot.utils.user_helpers import admin_required

goods_router = Router()

@goods_router.callback_query(F.data == 'admin_goods')
@admin_required
async def admin_goods(callback: CallbackQuery):
    """Открывает панель администратора с действиями по товарам."""

    await callback.answer('Вы выбрали Товары!')
    await callback.message.edit_text("Выберите действие",
        reply_markup=await InlineAdmin.admin_goods())

@goods_router.callback_query(F.data == 'add_good')
@admin_required
async def add_good(callback: CallbackQuery, state: FSMContext):
    """Запускает процесс добавления нового товара."""

    await callback.answer('Вы выбрали Добавить товар!')
    await callback.message.edit_text("Чтобы добавить товар, напишите его название.")
    await state.set_state(AddGood.waiting_for_name)


@goods_router.message(AddGood.waiting_for_name)
@admin_required
async def process_name(message: Message, state: FSMContext):
    """Обрабатывает ввод названия товара и запрашивает цену."""
    # """Обрабатывает ввод названия товара и запрашивает описание."""

    name = message.text
    await state.update_data(name=name)  # Сохраняем имя товара
    await message.answer("Теперь введите цену товара.")
    await state.set_state(AddGood.waiting_for_price)
    # await message.answer("Теперь введите описание товара.")
    # await state.set_state(AddGood.waiting_for_description)


# @goods_router.message(AddGood.waiting_for_description)
# async def process_description(message: Message, state: FSMContext):
#     """Обрабатывает описание товара и запрашивает цену."""
#
#     description = message.text
#     await state.update_data(description=description)  # Сохраняем описание товара
#     await message.answer("Теперь введите цену товара.")
#     await state.set_state(AddGood.waiting_for_price)


@goods_router.message(AddGood.waiting_for_price)
@admin_required
async def process_price(message: Message, state: FSMContext):
    """Обрабатывает цену товара и предлагает выбрать единицу измерения."""

    try:
        price = int(message.text)
        await state.update_data(price=price)  # Сохраняем цену товара
        await message.answer("Теперь введите в чем измеряется товар.",
        reply_markup=await InlineAdmin.inline_admin_goods_measurement())
        await state.set_state(AddGood.waiting_for_measurement)  # Переходим к последнему шагу
    except ValueError:
        await message.answer("Цена должна быть числом. Попробуйте еще раз.")


@goods_router.callback_query(F.data.startswith('admin_good_add_'), AddGood.waiting_for_measurement)
@admin_required
async def process_measurement(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает единицу измерения и запрашивает категорию."""
    # """Обрабатывает единицу измерения и запрашивает изображение товара."""

    measurement = callback.data.split('_')[-1]
    await state.update_data(measurement=measurement)
    await callback.message.answer(
        '''В какую категорию добавить товар?''',
        reply_markup=await InlineAdmin.inline_admin_good_categories())
    await state.set_state(AddGood.waiting_for_category)

#     await callback.message.edit_text("Теперь отправьте изображение товара.")
#     await state.set_state(AddGood.waiting_for_image)
#
# @goods_router.message(AddGood.waiting_for_image, F.content_type == ContentType.PHOTO)
# async def process_image(message: Message, state: FSMContext):
#     """Обрабатывает изображение товара и предлагает выбрать категорию."""
#
#     image_id = message.photo[-1].file_id  # Получаем ID изображения
#     await state.update_data(image_id=image_id)  # Сохраняем изображение товара
#     await message.answer(
#         '''В какую категорию добавить товар?''',
#         reply_markup=await InlineAdmin.inline_admin_categories())
#     await state.set_state(AddGood.waiting_for_category)
#     await Category.select_categories()


@goods_router.callback_query(F.data.startswith('admin_category_add_'), AddGood.waiting_for_category)
@admin_required
async def process_category(callback: CallbackQuery, state: FSMContext):
    """Сохраняет товар в БД после выбора категории."""

    category_id = callback.data.split('_')[-1]
    await state.update_data(category_id=int(category_id))
    data = await state.get_data()
    await callback.message.edit_text(
        (f"✅ Товар создан!\n"
         f"Название: {data['name']}\n"
         # f"Описание: {data['description']}\n"
         f"Цена: {data['price']}\n"
         f"В чем измеряется: {data['measurement']}\n"
         # f"Изображение: {data['image_id']}\n"
         f"Категория: {data['category_id']}\n\n"
         f"Выберите дальнейшее действие"),
        reply_markup=await InlineAdmin.admin_panel())
    await Good.input_good(data)

    await state.clear()


@goods_router.callback_query(F.data == 'edit_good')
@admin_required
async def edit_good(callback: CallbackQuery):
    """Запускает процесс изменения товара."""

    await callback.answer('Вы выбрали Изменить товар!')
    await callback.message.edit_text(
        'Выберите товар',
        reply_markup=await InlineAdmin.inline_admin_goods(edit=True))

@goods_router.callback_query(F.data == 'del_good')
@admin_required
async def del_good(callback: CallbackQuery):
    """Запускает процесс удаления товара."""

    await callback.answer('Вы выбрали Удалить товар!')
    await callback.message.edit_text(
        'Выберите товар',
        reply_markup=await InlineAdmin.inline_admin_goods(is_active=True))

@goods_router.callback_query(F.data == 'recover_good')
@admin_required
async def recover_good(callback: CallbackQuery):
    """Запускает процесс восстановления товара."""

    await callback.answer('Вы выбрали Восстановить товар!')
    await callback.message.edit_text(
        'Выберите товар',
        reply_markup=await InlineAdmin.inline_admin_goods(is_active=False))

@goods_router.callback_query(F.data.startswith('admin_good_status_'))
@admin_required
async def change_good_status(callback: CallbackQuery):
    """Изменяет is_active статус товара на противоположный."""

    good_id = int(callback.data.split('_')[-1])
    is_active = int(callback.data.split('_')[-2])

    name = await Good.update_is_active_good({'id': good_id, 'is_active': is_active})

    if is_active:
        text = f"✅ Товар восстановлен!\nНазвание: {name}\nВыберите дальнейшее действие"

    else:
        text = f"✅ Товар удален!\nНазвание: {name}\nВыберите дальнейшее действие"

    await callback.message.answer(text, reply_markup=await InlineAdmin.admin_panel())

@goods_router.callback_query(F.data.startswith('admin_good_edit_'))
@admin_required
async def edit_cur_good(callback: CallbackQuery):
    """Процесс выбора действия для изменения конкретного товара."""

    good_id = int(callback.data.split('_')[-1])
    await callback.message.edit_text("Выберите действие",
                                     reply_markup=await InlineAdmin.admin_goods_edit(good_id))

@goods_router.callback_query(F.data.startswith('edit_good_'))
@admin_required
async def edit_good_field(callback: CallbackQuery, state: FSMContext):
    """
    Общий callback: разбираем, что редактируем и у какого товара.
    Например: edit_good_name_123
    """
    parts = callback.data.split('_')
    field = parts[2]
    good_id = int(parts[3])

    prompts = {
        "name": "Напишите новое название:",
        "price": "Напишите новую цену:",
        "measurement": "Напишите новую единицу измерения:"
    }

    if field == 'cat':
        await callback.message.edit_text(
            "Выберите категорию",
            reply_markup=await InlineAdmin.inline_admin_good_categories(edit=True, good_id=good_id))
    else:
        await callback.message.edit_text(prompts.get(field, "Введите значение:"))
        await state.set_state(EditGood.waiting_for_value)
        await state.update_data(good_id=good_id, field=field)

@goods_router.message(EditGood.waiting_for_value)
@admin_required
async def process_edit_field(message: Message, state: FSMContext):
    """
    Универсальный message-хендлер: получает новое значение и сохраняет.
    """
    value = message.text
    data = await state.get_data()

    good_id = data["good_id"]
    field = data["field"]
    if field == "price":
        try:
            value = float(value)
        except ValueError:
            await message.answer("Цена должна быть числом. Попробуйте ещё раз.")
            return
    await Good.update_good({'good_id': good_id, field: value})
    await message.answer(
        f"✅ Товар обновлён!\n{field.capitalize()}: {value}\nВыберите дальнейшее действие",
        reply_markup=await InlineAdmin.admin_panel()
    )
    await state.clear()

@goods_router.callback_query(F.data.startswith('update_good_cat_'))
@admin_required
async def update_good_cat(callback: CallbackQuery):
    """Изменяет категорию/подкатегорию товара."""

    category_id = int(callback.data.split('_')[-1])
    good_id = int(callback.data.split('_')[-2])

    await Good.update_good({'good_id': good_id, 'category_id': category_id})

    await callback.message.answer(
        f"✅ Товар обновлён!\n\nВыберите дальнейшее действие",
            reply_markup=await InlineAdmin.admin_panel())
