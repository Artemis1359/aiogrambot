from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogrambot.database.repository import  Basket, User
from aiogrambot.states.order import OrderComment
from aiogrambot.states.registration import Reg
from aiogrambot.utils.text_helpers import is_valid_phone, admin_order_text
from aiogrambot.utils.user_helpers import check_user_info


reg_router = Router()

@reg_router.message(Reg.number)
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

@reg_router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):

    telegram_id = message.from_user.id
    name = message.text
    await User.input_name(telegram_id=telegram_id,
                          name=name)
    await check_user_info(telegram_id=telegram_id, state=state, message=message)
    await state.clear()

@reg_router.message(OrderComment.comment)
async def order_comment(message: Message, state: FSMContext):

    telegram_id = message.from_user.id
    comment = message.text
    await Basket.input_comment(telegram_id=telegram_id,
                          comment=comment)
    await check_user_info(telegram_id=telegram_id, state=state, message=message)
    await state.clear()


@reg_router.callback_query(F.data == 'order_name')
async def order_name(callback: CallbackQuery, state: FSMContext):

    await state.set_state(Reg.name)
    await callback.message.edit_text('Введите новое имя')
    await callback.answer()


@reg_router.callback_query(F.data == 'order_number')
async def order_number(callback: CallbackQuery, state: FSMContext):

    await state.set_state(Reg.number)
    await callback.message.edit_text('Введите номер в формате: +7XXXXXXXXXX')
    await callback.answer()


@reg_router.callback_query(F.data == 'order_comment')
async def order_comment(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderComment.comment)
    await callback.message.edit_text('Введите новый комментарий')
    await callback.answer()
