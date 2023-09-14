from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

show_table_message = InlineKeyboardMarkup()
button = InlineKeyboardButton(text="Просмотр таблицы", url="https://docs.google.com/spreadsheets/d/1gGDKa3RvENbm2lrzlpu9R56wLA5GCejFbd7CBJdW0C4/edit#grid=0")
show_table_message.add(button)
