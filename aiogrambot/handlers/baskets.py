from aiogram import F, Router

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from aiogrambot.database.repository import Basket, GoodBasket
from aiogrambot.keyboards.inline import InlineBasket, InlineCategory
from aiogrambot.utils.text_helpers import basket_text

basket_router = Router()


@basket_router.callback_query(F.data.startswith('b_add_'))
async def basket_add(callback: CallbackQuery, state: FSMContext):
    """Добавляет товар в корзину."""

    parts = callback.data.split('_')
    telegram_id = callback.from_user.id
    basket_id = await Basket.select_basket(telegram_id)
    if not basket_id:
        basket_id = await Basket.create_new_basket(telegram_id)
    else:
        basket_id = basket_id.get('id')
    good_id = int(parts[-1])
    price = int(parts[-2])
    quantity = int(parts[-3])
    from_basket = True if parts[-4] == 'b' else None

    data = await state.get_data()
    category_id = data.get("category_id")

    await GoodBasket.input_good_to_basket(basket_id, good_id, quantity, price)
    if not from_basket:
        await callback.message.edit_text(
            "✅ Товар добавлен в корзину!",
            reply_markup=await InlineCategory.inline_back_to_category(category_id=category_id)
        )
    else:
        await callback.message.edit_text(
            "✅ Количество товаров изменено!",
            reply_markup=await InlineBasket.inline_back_to_basket()
        )
    await callback.answer()


@basket_router.callback_query(F.data == 'back_to_basket')
async def back_to_basket(callback: CallbackQuery):
    """Возвращается к корзине."""

    telegram_id = callback.from_user.id

    data = await GoodBasket.select_goods_in_basket(telegram_id)
    text = await basket_text(data)
    if data:
        basket_id = data[0].get('basket_id')
        await callback.message.edit_text(
            text,
            parse_mode='Markdown',
            reply_markup=await InlineBasket.inline_goods_in_basket(basket_id=basket_id))
    else:
        await callback.message.edit_text('🧺 Корзина пуста')

    await callback.answer()

@basket_router.message(F.text == '🧺 Корзина')
async def basket_good_quantity(message: Message):
    """Открывает корзину."""

    telegram_id = message.from_user.id

    data = await GoodBasket.select_goods_in_basket(telegram_id)
    text = await basket_text(data)
    if data:
        basket_id = data[0].get('basket_id')
        await message.answer(
            text,
            parse_mode='Markdown',
            reply_markup=await InlineBasket.inline_goods_in_basket(basket_id=basket_id))
    else:
        await message.answer('🧺 Корзина пуста')


@basket_router.callback_query(F.data.startswith('del_menu_'))
async def del_menu(callback: CallbackQuery):
    """Меню удаления позиции из корзины."""

    telegram_id = callback.from_user.id
    basket_id = int(callback.data.split('_')[-1])

    text = 'Выберите позицию, которую хотите удалить:'
    await callback.message.edit_text(
        text,
        reply_markup=await InlineBasket.inline_del_good_in_basket(telegram_id=telegram_id, basket_id=basket_id))
    await callback.answer()

@basket_router.callback_query(F.data.startswith('del_pos_'))
async def del_pos(callback: CallbackQuery):
    """Удаление позиции из корзины."""
    basket_id = int(callback.data.split('_')[-1])
    good_id = int(callback.data.split('_')[-2])
    await GoodBasket.delete_good_from_basket(
        basket_id=basket_id,
        good_id=good_id
    )
    await callback.message.edit_text(
        'Товар убран из корзины.',
        reply_markup=await InlineBasket.inline_back_to_basket())
    await callback.answer()


@basket_router.callback_query(F.data =='edit_menu')
async def edit_menu(callback: CallbackQuery):
    """Меню изменения количества позиции в корзине."""

    telegram_id = callback.from_user.id

    text = 'Выберите позицию, которую хотите изменить:'
    await callback.message.edit_text(
        text,
        reply_markup=await InlineBasket.inline_edit_good_in_basket(telegram_id=telegram_id))
    await callback.answer()