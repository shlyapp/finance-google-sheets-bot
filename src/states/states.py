from aiogram.dispatcher.filters.state import StatesGroup, State


class BotStates(StatesGroup):
    SELECT_TYPE = State()
    SELECT_CATEGORY = State()
    ENTER_VALUE = State()


class CreateMenuButton(StatesGroup):
    SELECT_TYPE = State()
    ENTER_NAME = State()
