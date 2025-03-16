from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogrambot.database.repository import Good, Category
from aiogrambot.keyboards.inline.admin import InlineAdmin
from aiogrambot.states.admin import AddGood

goods_router = Router()

@goods_router.callback_query(F.data == 'admin_goods')
async def admin_goods(callback: CallbackQuery):
    """Открывает панель администратора с действиями по товарам."""

    await callback.answer('Вы выбрали Товары!')
    await callback.message.edit_text("Выберите действие",
        reply_markup=await InlineAdmin.admin_goods())

@goods_router.callback_query(F.data == 'add_good')
async def add_good(callback: CallbackQuery, state: FSMContext):
    """Запускает процесс добавления нового товара."""

    await callback.answer('Вы выбрали Добавить товар!')
    await callback.message.edit_text("Чтобы добавить товар, напишите его название.")
    await state.set_state(AddGood.waiting_for_name)


@goods_router.message(AddGood.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Обрабатывает ввод названия товара и запрашивает описание."""

    name = message.text
    await state.update_data(name=name)  # Сохраняем имя товара
    await message.answer("Теперь введите описание товара.")
    await state.set_state(AddGood.waiting_for_description)


@goods_router.message(AddGood.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    """Обрабатывает описание товара и запрашивает цену."""

    description = message.text
    await state.update_data(description=description)  # Сохраняем описание товара
    await message.answer("Теперь введите цену товара.")
    await state.set_state(AddGood.waiting_for_price)


@goods_router.message(AddGood.waiting_for_price)
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
async def process_measurement(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает единицу измерения и запрашивает изображение товара."""
    measurement = callback.data.split('_')[-1]
    await state.update_data(measurement=measurement)
    await callback.message.edit_text("Теперь отправьте изображение товара.")
    await state.set_state(AddGood.waiting_for_image)

@goods_router.message(AddGood.waiting_for_image, F.content_type == ContentType.PHOTO)
async def process_image(message: Message, state: FSMContext):
    """Обрабатывает изображение товара и предлагает выбрать категорию."""

    image_id = message.photo[-1].file_id  # Получаем ID изображения
    await state.update_data(image_id=image_id)  # Сохраняем изображение товара
    await message.answer(
        '''В какую категорию добавить товар?''',
        reply_markup=await InlineAdmin.inline_admin_categories())
    await state.set_state(AddGood.waiting_for_category)
    await Category.select_categories()


@goods_router.callback_query(F.data.startswith('admin_category_add_'), AddGood.waiting_for_category)
async def process_category(callback: CallbackQuery, state: FSMContext):
    """Сохраняет товар в БД после выбора категории."""

    category_id = callback.data.split('_')[-1]
    await state.update_data(category_id=int(category_id))  # Сохраняем описание товара

    data = await state.get_data()

    # Здесь можно сохранить данные в базу данных или выполнить другие действия

    #TODO поправить текст, чтобы выводился ровно везде
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
    # Завершаем процесс и сбрасываем состояние
    await state.clear()


@goods_router.callback_query(F.data == 'edit_good')
async def edit_good(callback: CallbackQuery):
    await callback.answer('Вы выбрали Изменить товар!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())

@goods_router.callback_query(F.data == 'del_good')
async def del_good(callback: CallbackQuery):
    await callback.answer('Вы выбрали Удалить товар!')
    await callback.message.edit_text(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())