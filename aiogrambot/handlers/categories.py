from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogrambot.database.repository import Category
from aiogrambot.keyboards.inline import InlineCategory, InlineGood
from aiogrambot.states.category import CategoryStates
from aiogrambot.utils.callback_helpers import callback_message_editor


categories_router = Router()

@categories_router.callback_query(F.data.startswith('category_'))
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


@categories_router.callback_query(F.data.startswith('subcategory_'))
async def subcategory(callback: CallbackQuery):
    await callback_message_editor(
        callback=callback,
        text='Выберите подкатегорию:',
        reply_markup=await InlineCategory.inline_subcategories(category_id=int(callback.data.split('_')[-1]))
    )