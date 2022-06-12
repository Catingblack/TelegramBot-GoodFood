from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


from database import food_db, drink_db



#основное 
def kb_base():
    kb = InlineKeyboardMarkup()
    btn_1 = InlineKeyboardButton('Меню', callback_data='btn_menu')

    kb.add(btn_1)
    return kb



#общее меню
def kb_menu():
    kb = InlineKeyboardMarkup()
    btn_1 = InlineKeyboardButton('Еда', callback_data='btn_food')
    btn_2 = InlineKeyboardButton('Напитки', callback_data='btn_drink')

    kb.add(btn_1, btn_2)
    return kb



#меню выбора еды



def kb_food():
    pass
    



#меню выбора напитков
def kb_drink():
    pass





#button =  InlineKeyboardButton(text="Лайкнуть", callback_data=cb.new(id=5, action="like"))

