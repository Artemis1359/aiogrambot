from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogrambot.database.repository import Good
from aiogrambot.keyboards.inline import InlineAdmin, InlineCategory, InlineGood

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    telegram_id = message.from_user.id
    await message.answer('''Откройте для себя вкус настоящей домашней еды с Маминой Кухней👩🏼‍🍳
''', reply_markup=await InlineAdmin.inline_is_admin(telegram_id=telegram_id))


@start_router.callback_query(F.data == 'back_to_start')
async def back_to_start(callback: CallbackQuery):
    await callback.answer('Вы выбрали каталог!')
    telegram_id = callback.from_user.id
    await callback.message.edit_text('''Откройте для себя вкус настоящей домашней еды с Маминой Кухней👩🏼‍🍳
''', reply_markup=await InlineAdmin.inline_is_admin(telegram_id=telegram_id))


@start_router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('Вы выбрали каталог!')

    await callback.message.edit_text(
        'Выберите категорию, чтобы посмотреть список товаров',
        reply_markup=await InlineCategory.inline_categories())

@start_router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    # await callback.answer(f'Вы выбрали {callback.data.split('_')[1]}!')
    # TODO Убрать дублирование
    if callback.message.text:
        await callback.message.edit_text(
            'Выберите товар, чтобы посмотреть дополнительную информацию',
            reply_markup=await InlineGood.inline_goods(category_id=int(callback.data.split('_')[-1])))
    else:
        # Если в сообщении только фото — удаляем его и отправляем новое
        await callback.message.delete()
        await callback.message.answer(
            "Выберите товар, чтобы посмотреть дополнительную информацию",
            reply_markup=await InlineGood.inline_goods(category_id=int(callback.data.split('_')[-1])))


@start_router.callback_query(F.data.startswith('good_'))
async def category(callback: CallbackQuery):

    good_id = int(callback.data.split('_')[-1])
    good = await Good.select_good(good_id=good_id)
    await callback.answer(f'Вы выбрали {good[1]}')

    try:
        await callback.message.edit_media(
            media = InputMediaPhoto(
                media=good[6],
                caption=f"{good[1]}\n {good[2]}\n {good[3]}р / {good[4]}"
            )
        )
    except TelegramBadRequest:
        await callback.message.edit_text(
            text=f"{good[1]}\n {good[2]}\n {good[3]}р / {good[4]}"
        )

    await callback.message.edit_reply_markup(reply_markup = await InlineGood.inline_good(good))

@start_router.message(Command('photo'))
async def get_photo(message: Message):
    # Посмотреть что можно передавать
    await message.answer_photo(photo='photoID', caption='Описание')