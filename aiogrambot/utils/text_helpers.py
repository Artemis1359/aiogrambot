from aiogrambot.database.models import Measurement


# async def measure_check(measure):
#     """Возвращает текст в зависимости от единицы измерения."""
#
#     if measure in ('l5', 'l6'):
#         text = f'Выберите количество банок {Measurement[measure].value}'
#     elif measure == 'kg':
#         text = f'Выберите количество кг'
#     else:
#         text = 'Выберите количество товара.'
#     return text

async def basket_text(data):
    """Возвращает данные по корзине пользователя."""

    # amount = 0
    text = f'В корзине:\n\n'
    for good in data:
        text += (f" - {good.get('name')}\n ({int(good.get('quantity'))} × {int(good.get('price'))}₽) - "
                 f"{int(good.get('amount'))}₽\n\n")
        # amount += int(good.get('amount'))
    # text += f'💰 *Итого* {amount}₽'
    return text
