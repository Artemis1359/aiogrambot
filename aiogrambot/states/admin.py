from aiogram.fsm.state import StatesGroup, State

class AddGood(StatesGroup):
    waiting_for_name = State()  # Ожидаем имя товара
    waiting_for_description = State()  # Ожидаем описание товара
    waiting_for_price = State()  # Ожидаем цену товара
    waiting_for_measurement = State()
    waiting_for_image = State()
    waiting_for_category = State()