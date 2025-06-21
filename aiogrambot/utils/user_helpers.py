from functools import wraps

from aiogram.fsm.context import FSMContext

from aiogrambot.database.repository import User, GoodBasket, Basket, Admin
from aiogram.types import Message

from aiogrambot.keyboards.inline.orders import InlineOrder
from aiogrambot.states.registration import Reg
from aiogrambot.utils.text_helpers import order_text

def admin_required(func):
    @wraps(func)
    async def wrapper(event, **data):
        telegram_id = event.from_user.id
        is_admin = await Admin.is_user_admin(telegram_id)
        if not is_admin:
            if hasattr(event, "message"):
                await event.message.answer("❌ У вас нет доступа к админ-панели.")
            else:
                await event.answer("❌ У вас нет доступа к админ-панели.")
            return

        return await func(event, **data)

    return wrapper




async def check_users(telegram_id: int, message: Message):

    user = await User.select_user(telegram_id=telegram_id)
    name = f'{message.from_user.last_name} {message.from_user.first_name}'
    if not user:
        await User.input_user(telegram_id=telegram_id, name=name)
    else:
        if not user.get('name'):
            await User.input_name(telegram_id=telegram_id, name=name)

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
        name = user_info.get('name')
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
