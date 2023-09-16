import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from menu.menu import CategoryMenu
from keyboards.keyboards import show_table_message
from states.states import BotStates, CreateMenuButton
from note import add_note

bot = Bot(token=str(os.getenv('TELEGRAM_API_TOKEN')))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
menu = CategoryMenu()
btn = types.KeyboardButton("Отмена")

# Базовые команды

@dp.message_handler(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Привет!\n" +
                         "Я бот для учета финансов. Чтобы узнать мои команды нажми на /help")

@dp.message_handler(Command('help'))
async def send_command_list(message: types.Message):
    await message.answer("Мои команды:\n" +
                         "/start - запуск бота\n" +
                         "/list - показать записи о финанасах\n" +
                         "/new - внести новую запись")


@dp.message_handler(Command('list'))
async def send_note_list(message: types.Message):
    await message.answer("Чтобы посмотреть всю таблицу, нажми на кнопку: ", 
                         reply_markup=show_table_message)


@dp.message_handler(Command('new'))
async def add_new_note(message: types.Message):
    await BotStates.SELECT_TYPE.set()
    keyboard = menu.get_type_menu().add(types.KeyboardButton("Отмена"))
    await message.answer("Пожалуйста, выберите финансовый тип:", 
                         reply_markup=keyboard)

# Внесение данных

@dp.message_handler(state=BotStates.SELECT_TYPE)
async def select_type(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        return
    async with state.proxy() as data:
        data['type'] = message.text
    await BotStates.SELECT_CATEGORY.set()
    await message.answer(f"Выбран тип: '{message.text}'")
    await select_category(message, state)


@dp.message_handler(state=BotStates.SELECT_CATEGORY)
async def select_category(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        return
    if message.text == "Вернуться обратно":
        async with state.proxy() as data:
            keyboard = menu.get_category_menu(menu.get_category_id_by_name(data['type']))
            await message.answer("Выберите категорию", reply_markup=keyboard)
            return 
    keyboard = menu.get_category_menu(menu.get_category_id_by_name(message.text)).add(btn)
    category_id = menu.get_category_id_by_name(message.text)
    is_item = True if category_id == -1 else False 
    if is_item:
        await BotStates.ENTER_VALUE.set()
        async with state.proxy() as data:
            data['category'] = message.text
            await message.answer(f"Вы выбрали категорию: '{data['category']}'\n" + 
                                 "Пожалуйста, напишите сумму:", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(btn))
    else:
        if message.text == "Удалить":
            print("Удалить")
        elif message.text == "Добавить кнопку":
            print("Добавить кнопку")
        else:
            await message.answer("Выберите категорию: ",
                            reply_markup=keyboard)


@dp.message_handler(state=BotStates.ENTER_VALUE)
async def enter_value(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        return

    parts = message.text.split(" ", 1)

    while not parts[0]:
        await message.reply("Некорректный ввод, пожалуйста, введите число:")
        return

    async with state.proxy() as data:
        data['price'] = parts[0]
        if len(parts) > 1:
            data['comment'] = parts[1]
        else:
            data['comment'] = ""
        add_note(message.from_user.full_name, message.date, data)
        await message.reply(f"{data['type']}, {data['category']}, {data['price']}, {data['comment']}")

    await state.finish()
    await add_new_note(message)
    return


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
