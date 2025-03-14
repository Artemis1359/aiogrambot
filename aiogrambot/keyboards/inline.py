from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogrambot.database.repository import select_categories, select_goods

settings_old = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Youtube', url='https://youtube.com/')],

    ]
)

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
        [InlineKeyboardButton(text='Корзина', callback_data='basket')],
        [InlineKeyboardButton(text='Контакты', callback_data='contacts')]
    ]

)
goods = [
    ('Яйца домашние', 170, 'шт.', '', '', 'eggs'),
    ('Заправка для борща', 250, 'шт.', 0.5, 'л.', 'borsch'),
    ('Огурцы маринованные', 220, 'шт.', 0.6, 'л.', 'pickles'),
    ('Баклажаны в аджике', 300, 'шт.', 0.5, 'л.', 'eggplants'),
    ('Аджика из кабачка', 200, 'шт.', 0.5, 'л.', 'adjica'),
    ('Лечо', 250, 'шт.', 0.6, 'л.', 'lecho'),
    ('Икра кабачковая', 200, 'шт.', 0.5, 'л.', 'ikra kabachk'),
    ('Огурцы в горчичной заливке', 230, 'шт.', 0.5, 'л.', 'pickles_zaliv'),
    ('Котлеты из курицы', 500, 'кг.', '', '', 'kotlet_chicken'),
    ('Котлеты свиные', 600, 'кг.', '', '', 'kotlet_pig'),
    ('Зразы с яйцом', 620, 'кг.', '', '', 'zrazi'),
    ('Блины с курицей', 60, 'шт.', '', '', 'pancakes_chicken'),
    ('Блины с творогом', 60, 'шт.', '', '', 'pancakes_tvorog'),
    ('Блины со свининой', 70, 'шт.', '', '', 'pancakes_pig'),
    ('Пельмени с курицей', 600, 'кг.', '', '', 'pelmeni_chicken'),
    ('Пельмени со свининой', 700, 'кг.', '', '', 'pelmeni_pig'),

]

async def inline_categories():

    keyboard = InlineKeyboardBuilder()
    categories = await select_categories()
    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category[1], callback_data=f'category_{category[1]}_{category[0]}'))

    return keyboard.adjust(1).as_markup() # 2 это число кнопок в строке as_markup() всегда в конце


async def inline_goods(category_id: int):

    keyboard = InlineKeyboardBuilder()
    goods = await select_goods(category_id=category_id)
    for good in goods:
        keyboard.add(InlineKeyboardButton(text=f'{good[1]} - {good[2]} / {good[3]}', callback_data=f'category_{good[0]}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='catalog'))
    return keyboard.adjust(1).as_markup()