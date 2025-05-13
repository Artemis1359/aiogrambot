from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from aiogrambot.database.models import Measurement
from aiogrambot.database.repository import Good
from aiogrambot.keyboards.inline import InlineAdmin, InlineCategory, InlineGood
from aiogrambot.utils.callback_helpers import callback_message_editor
from aiogrambot.utils.user_helpers import check_users

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    telegram_id = message.from_user.id
    await message.answer('''Откройте для себя вкус настоящей домашней еды с Маминой Кухней👩🏼‍🍳''',
                         reply_markup=await InlineAdmin.inline_is_admin(telegram_id=telegram_id))


@start_router.callback_query(F.data == 'back_to_start')
async def start_back_to_start(callback: CallbackQuery):
    await callback.answer('Вы выбрали каталог!')
    telegram_id = callback.from_user.id
    await callback.message.edit_text('''Откройте для себя вкус настоящей домашней еды с Маминой Кухней👩🏼‍🍳''',
                                     reply_markup=await InlineAdmin.inline_is_admin(telegram_id=telegram_id))


@start_router.callback_query(F.data == 'start_catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('Вы выбрали каталог!')
    telegram_id = callback.from_user.id
    await check_users(telegram_id)
    await callback.message.edit_text(
        'Выберите категорию, чтобы посмотреть список товаров',
        reply_markup=await InlineCategory.inline_categories())

@start_router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    # await callback.answer(f'Вы выбрали {callback.data.split('_')[1]}!')

    await callback_message_editor(
        callback=callback,
        text='Выберите товар, чтобы посмотреть дополнительную информацию',
        reply_markup=await InlineGood.inline_goods(category_id=int(callback.data.split('_')[-1]))
    )



@start_router.callback_query(F.data.startswith('good_'))
async def category(callback: CallbackQuery):

    good_id = int(callback.data.split('_')[-1])
    good = await Good.select_good(good_id=good_id)
    await callback.answer(f"Вы выбрали {good.get('name')}")
    text = (f"{good.get('name')}\n {good.get('description')}\n "
            f"{good.get('price')}р / {Measurement[good.get('measurement')].value}")
    try:
        await callback.message.edit_media(
            media = InputMediaPhoto(
                media=good.get('image_id'),
                caption=text
            )
        )
    except TelegramBadRequest:
        await callback.message.edit_text(
            text=text
        )

    await callback.message.edit_reply_markup(reply_markup = await InlineGood.inline_good(good))
