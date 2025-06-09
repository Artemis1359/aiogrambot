from aiogram.fsm.context import FSMContext

from aiogrambot.database.repository import User, GoodBasket, Basket
from aiogram.types import Message

from aiogrambot.keyboards.inline.orders import InlineOrder
from aiogrambot.states.registration import Reg
from aiogrambot.utils.text_helpers import order_text


async def check_users(telegram_id: int):

    if not await User.select_user(telegram_id=telegram_id):
        await User.input_user(telegram_id=telegram_id)

async def check_name(message: Message, name: str):
    if not name:
        name = message.from_user.username
    return name

async def check_phone_number(phone_number: str):
    if not phone_number:
        phone_number=None
    return phone_number

async def check_comment(comment: str):
    if not comment:
        comment='не указан'
    return comment

async def check_user_info(telegram_id: int, state: FSMContext, message: Message):
    goods = await GoodBasket.select_goods_in_basket(telegram_id)
    if goods:
        user_info = await User.select_user_info(telegram_id=telegram_id)
        user_info = user_info[0] if user_info else {}

        name = await check_name(message=message, name=user_info.get('name'))
        phone_number = await check_phone_number(phone_number=user_info.get('phone_number'))

        if not phone_number:
            await state.update_data(name=name)
            await state.set_state(Reg.number)
            await message.answer('Введите номер в формате: +7XXXXXXXXXX')
        else:
            basket_info = await Basket.select_comment_basket(telegram_id=telegram_id)
            comment = basket_info.get('comment')
            if not comment:
                comment = 'не указан'
            text = await order_text(telegram_id=telegram_id,
                                    name=name, number=phone_number,
                                    comment=comment)

            await message.answer(text, reply_markup=await InlineOrder.inline_make_order(), parse_mode="HTML")
    else:
        await message.answer('🧺 Корзина пуста')
