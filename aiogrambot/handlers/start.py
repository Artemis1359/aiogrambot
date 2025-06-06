from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from aiogrambot.config import settings
from aiogrambot.database.models import Measurement
from aiogrambot.database.repository import Good, Category, GoodBasket, Basket, User, Order
from aiogrambot.keyboards.inline import InlineAdmin, InlineCategory, InlineGood, InlineBasket
from aiogrambot.keyboards.inline.orders import InlineOrder
from aiogrambot.keyboards.reply import main_page
from aiogrambot.states.category import CategoryStates
from aiogrambot.states.order import OrderComment
from aiogrambot.states.registration import Reg
from aiogrambot.utils.callback_helpers import callback_message_editor
from aiogrambot.utils.text_helpers import basket_text, order_text, is_valid_phone, admin_order_text
from aiogrambot.utils.user_helpers import check_users, check_name, check_phone_number, check_user_info

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    telegram_id = message.from_user.id
    await check_users(telegram_id)
    # await message.answer('''Откройте для себя вкус настоящей домашней еды с Маминой Кухней👩🏼‍🍳''',
    #                      reply_markup=await InlineAdmin.inline_is_admin(telegram_id=telegram_id))
    await message.answer('''Привет! 👋 Добро пожаловать в Мамину Кухню.''',
                         reply_markup=await main_page(telegram_id=telegram_id))


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

@start_router.message(F.text == '📦 Оформить заказ')
async def place_order(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    await check_users(telegram_id=telegram_id)
    await check_user_info(telegram_id=telegram_id,
                          state=state, message=message)



@start_router.message(Reg.number)
async def reg_number(message: Message, state: FSMContext):

    telegram_id = message.from_user.id
    number = message.text
    if await is_valid_phone(number):
        await User.input_phone_number(telegram_id=telegram_id,
                                      phone_number=number)
        await check_user_info(telegram_id=telegram_id, state=state, message=message)
        await state.clear()
    else:
        await message.answer('❌ Неверный формат номера.\nВведите номер в формате: +7XXXXXXXXXX')

@start_router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):

    telegram_id = message.from_user.id
    name = message.text
    await User.input_name(telegram_id=telegram_id,
                          name=name)
    await check_user_info(telegram_id=telegram_id, state=state, message=message)
    await state.clear()

@start_router.message(OrderComment.comment)
async def order_comment(message: Message, state: FSMContext):

    telegram_id = message.from_user.id
    comment = message.text
    await Basket.input_comment(telegram_id=telegram_id,
                          comment=comment)
    await check_user_info(telegram_id=telegram_id, state=state, message=message)
    await state.clear()


@start_router.callback_query(F.data == 'order_name')
async def order_name(callback: CallbackQuery, state: FSMContext):

    await state.set_state(Reg.name)
    await callback.message.edit_text('Введите новое имя')
    await callback.answer()


@start_router.callback_query(F.data == 'order_number')
async def order_number(callback: CallbackQuery, state: FSMContext):

    await state.set_state(Reg.number)
    await callback.message.edit_text('Введите номер в формате: +7XXXXXXXXXX')
    await callback.answer()


@start_router.callback_query(F.data == 'order_comment')
async def order_comment(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderComment.comment)
    await callback.message.edit_text('Введите новый комментарий')
    await callback.answer()


@start_router.callback_query(F.data == 'order_confirm')
async def order_confirm(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    basket = await Basket.select_basket(telegram_id=telegram_id)
    basket_id = basket.get('id')
    order_id = await Order.create_new_order(telegram_id=telegram_id,
                                             basket_id=basket_id)
    text = await admin_order_text(order_id=order_id)
    await Basket.update_basket_status(basket_id=basket_id)
    await callback.bot.send_message(settings.ADMIN_ID, text, parse_mode="Markdown")
    await callback.message.answer(f"Спасибо! Заказ №{order_id} принят. Мы свяжемся с вами в ближайшее время. 💛")


@start_router.callback_query(F.data == "noop")
async def noop_callback(callback: CallbackQuery):

    await callback.answer()