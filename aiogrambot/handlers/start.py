from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from aiogrambot.database.models import Measurement
from aiogrambot.database.repository import Good, Category, GoodBasket, Basket
from aiogrambot.keyboards.inline import InlineAdmin, InlineCategory, InlineGood, InlineBasket
from aiogrambot.keyboards.reply import main_page
from aiogrambot.states.category import CategoryStates
from aiogrambot.utils.callback_helpers import callback_message_editor
from aiogrambot.utils.user_helpers import check_users

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    telegram_id = message.from_user.id
    # await message.answer('''Откройте для себя вкус настоящей домашней еды с Маминой Кухней👩🏼‍🍳''',
    #                      reply_markup=await InlineAdmin.inline_is_admin(telegram_id=telegram_id))
    await message.answer('''Привет! 👋 Добро пожаловать в Мамину Кухню.''',
                         reply_markup=await main_page(telegram_id=telegram_id))


# @start_router.callback_query(F.data == 'back_to_start')
# async def start_back_to_start(callback: CallbackQuery):
#     await callback.answer('Вы выбрали каталог!')
#     telegram_id = callback.from_user.id
#     await callback.message.edit_text('''Привет! 👋 Добро пожаловать в Мамину Кухню.''',
#                                      reply_markup=await InlineAdmin.inline_is_admin(telegram_id=telegram_id))


@start_router.callback_query(F.data == 'back_to_catalog')
async def back_to_catalog(callback: CallbackQuery):
    await callback.answer('Вы вернулись в каталог!')
    telegram_id = callback.from_user.id
    await check_users(telegram_id)
    await callback.message.edit_text(
        'Выберите категорию:',
        reply_markup=await InlineCategory.inline_categories())

@start_router.message(F.text == '🛒 Каталог')
async def catalog(message: Message):
    telegram_id = message.from_user.id
    await check_users(telegram_id)
    await message.answer(
        'Выберите категорию:',
        reply_markup=await InlineCategory.inline_categories())

@start_router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery, state: FSMContext):

    category_id = int(callback.data.split('_')[-1])

    await state.set_state(CategoryStates.viewing)
    await state.update_data(category_id=category_id)

    subcategory = await Category.select_is_subcat(category_id)
    print(subcategory)
    await callback_message_editor(
        callback=callback,
        text='Выберите товар, чтобы посмотреть дополнительную информацию',
        reply_markup=await InlineGood.inline_goods(category_id=category_id, subcategory=subcategory)
    )


@start_router.callback_query(F.data.startswith('subcategory_'))
async def subcategory(callback: CallbackQuery):
    await callback_message_editor(
        callback=callback,
        text='Выберите подкатегорию:',
        reply_markup=await InlineCategory.inline_subcategories(category_id=int(callback.data.split('_')[-1]))
    )

@start_router.callback_query(F.data.startswith("q_good_"))
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

@start_router.callback_query(F.data.startswith('good_'))
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


@start_router.message(F.text == '🗑️ Очистить корзину')
async def clean_basket(message: Message):
    telegram_id = message.from_user.id
    basket = await Basket.select_basket(telegram_id=telegram_id)
    if basket:
        await GoodBasket.delete_all_goods_from_basket(basket.get('id'))
        await message.answer('🧺 Корзина очищена.')

@start_router.callback_query(F.data == "noop")
async def noop_callback(callback: CallbackQuery):

    await callback.answer()