from folder import Filesystem

import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

#from states import States
#from entry import add_entry, show_entrys
#from keyboards import action_keyboard, entry_keyboard, sale_category_keyboard, purchase_category_keyboard


bot = Bot(token=str(os.getenv('TELEGRAM_API_TOKEN')))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
folders = Filesystem()


#@dp.message_handler(commands=['start'])
#async def send_welcome(message: types.Message):
    #await message.answer('Привет! Я бот для внесения расходов. Пожалуйста, выбери нужное действие:', reply_markup=action_keyboard)


#@dp.message_handler(commands=['help'])
#async def send_command_list(message: types.Message):
    #await message.answer('Список комманд, который я могу выполнять:\n' 
                        # + '/start - запустить бота\n'
                        # + '/new - добавить новую запись\n'
                        # + '/list - вывести записи')


#@dp.message_handler(text='Внести запись')
#@dp.message_handler(commands=['new'])
#async def add_new_entry(message: types.Message):
    #await States.CHOOSE_TYPE.set()
    #await message.answer('Выберите тип (Доход/Расход):', reply_markup=entry_keyboard)


#@dp.message_handler(state=States.CHOOSE_TYPE)
#async def choose_entry_type(message: types.Message, state: FSMContext):
    #async with state.proxy() as data:
        #data['type'] = message.text

    #await States.CHOOSE_CATEGORY.set()
    
    #selected_keyboard = purchase_category_keyboard
    #async with state.proxy() as data:
        #if data['type'] == 'Продажа':
            #selected_keyboard = sale_category_keyboard

    #await message.answer("Выберите категорию:", reply_markup=selected_keyboard)


#@dp.message_handler(state=States.CHOOSE_CATEGORY)
#async def choose_entry_category(message: types.Message, state: FSMContext):
    #async with state.proxy() as data:
        #data['category'] = message.text

    #await States.ENTER_PRICE.set()
    #await message.answer("Введите цену")


#@dp.message_handler(state=States.ENTER_PRICE)
#async def enter_entry_price(message: types.Message, state: FSMContext):
    #while not message.text.isdigit():
        #await message.reply("Некорректный ввод. Пожалуйста, введите число: ")
        #return

    #async with state.proxy() as data:
        #data['price'] = message.text
        #add_entry(message.from_user.full_name, message.date, data)

    #await message.answer('Запись занесена!', reply_markup=action_keyboard)

    #await state.finish()



#@dp.message_handler(text='Посмотреть записи')
#@dp.message_handler(commands=['list'])
#async def show_list_entry(message: types.Message):
    #await message.answer('Последние 5 записей:\n' 
    #                    + f'{show_entrys()}\n'
    #                    + 'Вся таблица:\nhttps://docs.google.com/spreadsheets/d/1gGDKa3RvENbm2lrzlpu9R56wLA5GCejFbd7CBJdW0C4/edit?usp=sharing')

from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    START_TYPE = State()
    CHOOSE_CATEGORY = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Выберите элемент:", reply_markup=folders.get_markup_keyboard(0))
    await States.CHOOSE_CATEGORY.set()


@dp.message_handler(state=States.CHOOSE_CATEGORY)
async def choose(message: types.Message):
    keyboard = folders.get_markup_keyboard(folders.get_id_by_name(message.text))
    current_item = folders.get_folder(message.text)
    
    if (current_item is None):
        await message.answer(f"Выбран {message.text}")
        return

    if (current_item.parent != -1):
        keyboard.add(types.KeyboardButton(folders.get_folder_by_id(current_item.parent).name))

    await message.answer(f"В {message.text} есть: ", reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
