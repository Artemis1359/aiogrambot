from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogrambot.config import settings
from aiogrambot.database.repository import GoodBasket, Basket, Order, Admin
from aiogrambot.keyboards.inline import InlineCategory, InlineAdmin
from aiogrambot.keyboards.reply import main_page
from aiogrambot.utils.text_helpers import admin_order_text
from aiogrambot.utils.user_helpers import check_users, check_user_info, admin_required

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    telegram_id = message.from_user.id
    await check_users(telegram_id, message)
    # await message.answer('''Откройте для себя вкус настоящей домашней еды с Маминой Кухней👩🏼‍🍳''',
    #                      reply_markup=await InlineAdmin.inline_is_admin(telegram_id=telegram_id))
    await message.answer('''Привет! 👋 Добро пожаловать в Мамину Кухню.''',
                         reply_markup=await main_page(telegram_id=telegram_id))


@start_router.callback_query(F.data == 'back_to_catalog')
async def back_to_catalog(callback: CallbackQuery):
    await callback.answer('Вы вернулись в каталог!')
    telegram_id = callback.from_user.id
    await check_users(telegram_id, callback.message)
    await callback.message.edit_text(
        'Выберите категорию:',
        reply_markup=await InlineCategory.inline_categories())

@start_router.message(F.text == '🛒 Каталог')
async def catalog(message: Message):
    telegram_id = message.from_user.id
    await check_users(telegram_id, message)
    await message.answer(
        'Выберите категорию:',
        reply_markup=await InlineCategory.inline_categories())


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
    await check_users(telegram_id=telegram_id, message=message)
    await check_user_info(telegram_id=telegram_id,
                          state=state, message=message)

@start_router.message(F.text == '💼 Админ-панель')
@admin_required
async def admin_panel(message: Message):
    """Открывает панель администратора"""

    await message.answer(
        'Выберите действие',
        reply_markup=await InlineAdmin.admin_panel())


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