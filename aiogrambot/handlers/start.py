from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

import aiogrambot.keyboards.reply as reply
import aiogrambot.keyboards.inline as inline
from aiogrambot.states.registration import Reg

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('''Откройте для себя вкус настоящей домашней еды с Маминой Кухней👩🏼‍🍳
''', reply_markup=inline.settings)


@start_router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('Вы выбрали каталог!')
    await callback.message.edit_text(
        'Выберите категорию, чтобы посмотреть список товаров',
        reply_markup=await inline.inline_categories())


@start_router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data.split('_')[1]}!')
    await callback.message.edit_text(
        'Выберите товар, чтобы посмотреть дополнительную информацию',
        reply_markup=await inline.inline_goods(category_id=int(callback.data.split('_')[2])))
