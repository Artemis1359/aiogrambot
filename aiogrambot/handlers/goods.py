from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogrambot.database.models import Measurement
from aiogrambot.database.repository import Good
from aiogrambot.keyboards.inline import InlineGood, InlineBasket

goods_router = Router()

@goods_router.callback_query(F.data.startswith("q_good_"))
async def quantity_good(callback: CallbackQuery):
    good_id = int(callback.data.split("_")[-1])
    good = await Good.select_good(good_id=good_id)
    quantity = int(callback.data.split("_")[-2])
    from_basket = True if callback.data.split('_')[-3] == 'b' else False
    if quantity >= 1:
        if not from_basket:
            await callback.message.edit_reply_markup(reply_markup = await InlineGood.inline_good(good, quantity))
        else:
            await callback.message.edit_reply_markup(reply_markup=await InlineBasket.inline_edit_quantity(good, quantity))
    await callback.answer()

@goods_router.callback_query(F.data.startswith('good_'))
async def good(callback: CallbackQuery):

    good_id = int(callback.data.split('_')[-1])
    quantity = int(callback.data.split('_')[-2])
    from_basket = True if callback.data.split('_')[-3] == 'b' else False
    good = await Good.select_good(good_id=good_id)
    await callback.answer(f"Вы выбрали {good.get('name')}")
    text = (f"🛒 *{good.get('name')}* {good.get('description')} — "
            f"{good.get('price')} ₽ / {Measurement[good.get('measurement')].value}\n"
            f"Выберите количество:")
    try:
        await callback.message.edit_media(
            media = InputMediaPhoto(
                media=good.get('image_id'),
                caption=text,
                parse_mode='Markdown'
            )
        )
    except TelegramBadRequest:
        await callback.message.edit_text(
            text=text,
            parse_mode='Markdown'
        )
    if not from_basket:
        await callback.message.edit_reply_markup(reply_markup = await InlineGood.inline_good(good, quantity))
    else:
        await callback.message.edit_reply_markup(reply_markup = await InlineBasket.inline_edit_quantity(good, quantity))
