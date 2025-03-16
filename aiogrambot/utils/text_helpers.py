from aiogrambot.database.models import Measurement


async def measure_check(measure):
    """Возвращает текст в зависимости от единицы измерения."""

    if measure in ('l5', 'l6'):
        text = f'Выберите количество банок {Measurement[measure].value}'
    elif measure == 'kg':
        text = f'Выберите количество кг'
    else:
        text = 'Выберите количество товара.'
    return text

async def basket_text(data):
    """Возвращает данные по корзине пользователя."""

    amount = 0
    text = f'В корзине:\n\n'
    for good in data:
        text += f' • {good[0]} - ({good[2]} * {int(good[1])}р)\n {int(good[3])}р\n\n'
        amount += int(good[3])
    text += f'Общая стоимость {amount}'
    return text
