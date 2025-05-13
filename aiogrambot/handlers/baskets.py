from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto


from aiogrambot.database.repository import Basket, GoodBasket
from aiogrambot.keyboards.inline import InlineBasket, InlineCategory
from aiogrambot.utils.callback_helpers import callback_message_editor
from aiogrambot.utils.text_helpers import basket_text

basket_router = Router()

# @basket_router.callback_query(F.data.startswith('b_g_'))
# async def basket_good_quantity(callback: CallbackQuery):
#     """Открывает панель выбора количества товара."""
#
#     good_id = int(callback.data.split('_')[-1])
#     price = int(callback.data.split('_')[3])
#     measure = callback.data.split('_')[2]
#     text = await measure_check(measure)
#     await callback_message_editor(
#         callback=callback,
#         text=text,
#         reply_markup=await InlineBasket.inline_quantity_in_basket(good_id=good_id, measure=measure, price=price)
#     )


@basket_router.callback_query(F.data.startswith('b_add_'))
async def basket_add(callback: CallbackQuery, state: FSMContext):
    """Добавляет товар в корзину."""

    parts = callback.data.split('_')
    telegram_id = callback.from_user.id
    basket_id = await Basket.select_basket(telegram_id)
    if not basket_id:
        basket_id = await Basket.create_new_basket(telegram_id)
    else:
        basket_id = basket_id[0]
    good_id = int(parts[-1])
    price = int(parts[-2])
    quantity = int(parts[2])

    data = await state.get_data()
    category_id = data.get("category_id")

    await GoodBasket.input_good_to_basket(basket_id, good_id, quantity, price)
    await callback.message.edit_text(
        "✅ Товар добавлен в корзину!",
        reply_markup=await InlineCategory.inline_back_to_category(category_id=category_id)
    )
    await callback.answer()


@basket_router.callback_query(F.data == 'start_basket')
async def basket_good_quantity(callback: CallbackQuery):
    """Открывает корзину."""

    telegram_id = callback.from_user.id

    data = await GoodBasket.select_goods_in_basket(telegram_id)
    text = await basket_text(data)
    await callback.message.edit_text(text,
                                     parse_mode='Markdown',
                                     reply_markup=await InlineBasket.inline_goods_in_basket())



