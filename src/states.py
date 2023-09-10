from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    CHOOSE_TYPE = State()
    CHOOSE_CATEGORY = State()
    ENTER_PRICE = State()
