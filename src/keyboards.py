from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


action_buttons = [
    KeyboardButton("Внести запись"),
    KeyboardButton("Посмотреть записи")
]

entry_buttons = [
    KeyboardButton("Продажа"),
    KeyboardButton("Покупка")
]

sale_category_buttons = [
    KeyboardButton("Ламинат"),
    KeyboardButton("Кварц.винил"),
    KeyboardButton("Паркет")
]

purchase_category_buttons = [
    KeyboardButton("Ламинат"),
    KeyboardButton("Кварц.винил"),
    KeyboardButton("Паркет")
]

action_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
action_keyboard.add(*action_buttons)

entry_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
entry_keyboard.add(*entry_buttons)

sale_category_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
sale_category_keyboard.add(*sale_category_buttons)

purchase_category_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
purchase_category_keyboard.add(*purchase_category_buttons)
