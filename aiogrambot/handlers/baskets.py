from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from aiogrambot.database.models import Measurement
from aiogrambot.database.repository import Good
from aiogrambot.keyboards.inline import InlineBasket

basket_router = Router()

@basket_router.callback_query(F.data.startswith('basket_good_'))
async def basket_good_quantity(callback: CallbackQuery):
    """Открывает панель выбора количества товара."""

    good_id = int(callback.data.split('_')[-1])
    measure = callback.data.split('_')[2]
    print(measure)
    if measure in ('l5', 'l6'):
        text = f'Выберите количество банок {Measurement[measure].value}'
    elif measure == 'kg':
        text = f'Выберите количество кг'
    else:
        text = 'Выберите количество товара.'
    # TODO Убрать дублирование
    if callback.message.text:
        await callback.message.edit_text(
            text,
            reply_markup=await InlineBasket.inline_quantity_in_basket(good_id=good_id, measure=measure))
    else:
        await callback.message.delete()
        await callback.message.answer(
        text,
        reply_markup=await InlineBasket.inline_quantity_in_basket(good_id=good_id, measure=measure))
