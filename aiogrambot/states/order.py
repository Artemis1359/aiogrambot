from aiogram.fsm.state import StatesGroup, State

class OrderComment(StatesGroup):
    comment = State()