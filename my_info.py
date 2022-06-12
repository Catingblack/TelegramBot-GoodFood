import logging
import asyncio
from  aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3



bot = Bot(token = "5380741935:AAHntlKxzbcntSYGM8zA4rPVtwTl0Gw2LZ4")
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level = logging.INFO)





cb = CallbackData("post", "id", "action")


#img
#########


MY_ID = "AgACAgIAAxkDAAP4Ynzbju5X3LRpWd4QHEpQ5UFXsbkAAvK5MRuURulLA6WHtza0hmsBAAMCAANzAAMkBA"
MY_ID2 = "AgACAgIAAxkDAAIBBmJ-LmqzWDs6iJ21WbQF_G2hve6mAALLvTEbZUDxS0IF1uzTFuX5AQADAgADbQADJAQ"


#########
#########





#states
########

available_food_names = ["суши", "спагетти", "хачапури"]
available_food_sizes = ["маленькую", "среднюю", "большую"]

class OrderFood(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_food_size = State()



#########
#########








#handler states

async def food_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_food_names:
        keyboard.add(name)
    await message.answer("Выберите блюдо:", reply_markup=keyboard)
    await OrderFood.waiting_for_food_name.set()


async def food_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_food_names:
        await message.answer("Пожалуйста, выберите блюдо, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_food=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_food_sizes:
        keyboard.add(size)

    await OrderFood.next()
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)


async def food_size_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_food_sizes:
        await message.answer("Пожалуйста, выберите размер порции, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы заказали {message.text.lower()} порцию {user_data['chosen_food']}.\n"
                         f"Попробуйте теперь заказать напитки: /drinks", reply_markup=types.ReplyKeyboardRemove())
    await state.reset_state(with_data=False)


#########
#########





#registration states
########

def register_handlers_food(dp: Dispatcher):
    dp.register_message_handler(food_start, commands="food", state="*")
    dp.register_message_handler(food_chosen, state=OrderFood.waiting_for_food_name)
    dp.register_message_handler(food_size_chosen, state=OrderFood.waiting_for_food_size)



#########
#########





#buttons
########

inline_kb_full = InlineKeyboardMarkup(row_width=2)

button =  InlineKeyboardButton(text="Лайкнуть", callback_data=cb.new(id=5, action="like"))

btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='btn1')
btn_2 = InlineKeyboardButton('Вторая кнопка!', callback_data='btn2')

inline_kb_full.add(btn_1,btn_2,button)


#########
#########






#hendlers
#########

@dp.message_handler(commands="fuck")
async def process_command_2(message: types.Message):
    await message.answer("Отправляю все возможные кнопки", reply_markup=inline_kb_full)



@dp.message_handler(commands = "test1")
async def cmd_test1(message: types.Message):
    await bot.send_photo(message.from_user.id, MY_ID, caption="fuck", reply_markup=inline_kb_full)


@dp.message_handler(content_types=["photo"])
async def download_photo(message: types.Message):

    await message.photo[0].download(destination_dir="/home/catingblack/Рабочий стол/GF/")

##########
##########





#callbacks
##########

@dp.callback_query_handler(text="btn1")
async def send_random_value(call: types.CallbackQuery):
    #await call.message.answer("me")
    await bot.edit_message_caption(chat_id=call.message.chat.id, caption="eee", message_id=call.message.message_id, reply_markup=inline_kb_full)
    #await call.answer(text="Спасибо, что воспользовались ботом!", show_alert=True)
    #await call.message.delete_reply_markup()


@dp.callback_query_handler(text="btn2")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("me")
    await call.answer(text="Спасибо, что воспользовались ботом!", show_alert=True)
    await call.message.delete_reply_markup() 

@dp.callback_query_handler(cb.filter())
async def callbacks(call: types.CallbackQuery, callback_data: dict):
    post_id = callback_data["id"]
    action = callback_data["action"]
    await call.message.answer(post_id)
    await call.message.answer(action)



##########
##########


register_handlers_food(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

