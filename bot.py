from  aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

from config import TOKEN
from keyboards import kb_base, kb_menu
from database import food_db, drink_db, add_db




bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level = logging.INFO)




@dp.message_handler(commands="fuck")
async def process_command_2(message: types.Message):
    await message.answer("Отправляю все возможные кнопки", reply_markup=kb_menu())



    

cb_food = CallbackData("food", "name", "count")
cb_dop = CallbackData("dop", "name", "count")

#Выбор еды
##########



@dp.callback_query_handler(text="btn_food")
async def get_food_list(call: types.CallbackQuery):

    await call.message.answer("Выберите еду")


    for food in food_db:
        btn = InlineKeyboardButton("Выбрать:0", callback_data=cb_food.new(name=food, count=0))
        await bot.send_photo(call.from_user.id, food_db[food], caption=food, reply_markup=InlineKeyboardMarkup().add(btn))


def get_additional_list():
    btn = InlineKeyboardButton("Продолжить", callback_data="cont")
    kb = InlineKeyboardMarkup(row_width=3)

    for name in add_db:
        kb.add(InlineKeyboardButton(name+":0", callback_data=cb_dop(name=name, count=0)))
    return kb



@dp.callback_query_handler(cb_food.filter())
async def add_counter_food(call: types.CallbackQuery, callback_data: dict):

    _name = callback_data["name"]
    _count = int(callback_data["count"]) + 1

    btn_1 = InlineKeyboardButton(f"Выбрать:{_count}", callback_data=cb_food.new(name=_name, count=_count))

    btn_spaice = InlineKeyboardButton("+соус:0", callback_data="pass")
    btn_chiken = InlineKeyboardButton("+курица:0", callback_data="pass")
    btn_cheese = InlineKeyboardButton("+сыр:0", callback_data="pass")

    btn_finish = InlineKeyboardButton("Продолжить", callback_data="pass")

    kb = InlineKeyboardMarkup()
    kb.add(btn_1)
    kb.row(btn_spaice, btn_chiken, btn_cheese)
    kb.add(btn_finish)

    await call.message.edit_reply_markup(kb)

##############
##############


#Выбор напитка
##############
@dp.callback_query_handler(text="btn_drink")
async def get_drink(call: types.CallbackQuery):
    await call.message.answer("Выберите напиток")

    for drink in drink_db:
        await bot.send_photo(call.from_user.id, drink_db[drink], caption=drink,
                             reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Выбрать',
                                                               callback_data=cb.new(type="drink", name=drink, count=0))))
###############
###############



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
