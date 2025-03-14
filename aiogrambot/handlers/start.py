from turtledemo.penrose import start

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import aiogrambot.keyboards.reply as reply
import aiogrambot.keyboards.inline as inline
from aiogrambot.states.registration import Reg

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('''Откройте для себя вкус настоящей домашней еды с Маминой Кухней👩🏼‍🍳
''', reply_markup=inline.settings)

@start_router.message(Command('start2'))
async def cmd_start(message: Message):
    await message.reply(
        f'Привет.\nТвой ID: {message.from_user.id}\nИмя: {message.from_user.first_name}',
    reply_markup=reply.main)

@start_router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('ХЕЛП', reply_markup=await reply.cars())

@start_router.message(Command('help2'))
async def get_help(message: Message):
    await message.answer('ХЕЛП', reply_markup=await inline.inline_cars())

@start_router.message(F.text == 'Как дела?')
async def ok(message: Message):
    await message.answer('ОК')

@start_router.message(F.photo)
async def photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}' )

@start_router.message(Command('photo'))
async def get_photo(message: Message):
    # Посмотреть что можно передавать
    await message.answer_photo(photo='photoID', caption='Описание')


@start_router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('Вы выбрали каталог!')
    # await callback.message.answer('Привет')
    await callback.message.edit_text(
        'Выберите категорию, чтобы посмотреть список товаров',
        reply_markup=await inline.inline_categories())


@start_router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data.split('_')[1]}!')
    # await callback.message.answer('hi')
    await callback.message.edit_text(
        'Выберите товар, чтобы посмотреть дополнительную информацию',
        reply_markup=await inline.inline_goods(category_id=int(callback.data.split('_')[2])))



@start_router.message(Command('reg'))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите ваше имя')

@start_router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите номер телефона')

@start_router.message(Reg.number)
async def reg_three(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f'Регистрация завершена {data}')
    await state.clear()