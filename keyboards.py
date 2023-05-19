from utils import *
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def get_confirmation_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton("Подтвердить", callback_data="confirm"),
        types.InlineKeyboardButton("Изменить данные", callback_data="change"),
    )
    return keyboard

def get_confirmation_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton("Подтвердить", callback_data="confirm"),
        types.InlineKeyboardButton("Отменить", callback_data="Отменить"),
    )
    return keyboard

# --- startup menu buttons ---
startup_menu_btn1 = types.KeyboardButton("Баланс счёта")
startup_menu_btn2 = types.KeyboardButton("Активные сервера")
startup_menu_btn3 = types.KeyboardButton("Настройка серверов")

startup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
startup_menu.add(startup_menu_btn1, 
                 startup_menu_btn2, 
                 startup_menu_btn3)

# --- config_server menu buttons ---
config_menu_btn1 = types.KeyboardButton("Деплой сервера")
config_menu_btn2 = types.KeyboardButton("Удаление сервера")
config_menu_btn3 = types.KeyboardButton("Вернуться в главное меню")

config_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
config_menu.add(config_menu_btn1,
                 config_menu_btn2, 
                 config_menu_btn3)

# --- create os inline keyboard ---
os_buttons = []
for os_name, os_id in os_dict.items():
    os_button = types.InlineKeyboardButton(os_name, callback_data=str(os_id))
    os_buttons.append(os_button)
            
os_keyboard = types.InlineKeyboardMarkup()
os_keyboard.add(*os_buttons)

# --- create regions inline keyboard ---
region_buttons = []
for region_name, region_id in reversed_regions_dict.items():
    region_button = types.InlineKeyboardButton(region_name, callback_data=region_id)
    region_buttons.append(region_button)

region_keyboard = types.InlineKeyboardMarkup()
region_keyboard.add(*region_buttons)

# --- cancel configuring instances button
cancel_btn = types.KeyboardButton("Отменить")
cancel_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(cancel_btn)

def create_inline_keyboard(button_list):
    buttons = []
    for item in button_list:
        key = list(item.keys())[0]
        value = list(item.values())[0]
        callback_data = str(value)
        button = types.InlineKeyboardButton(key, callback_data=callback_data)
        buttons.append(button)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    
    return keyboard

#async def remove_keyboard(keyboard):
#    keyboard.remove

#async def remove_keyboard(keyboard):
#    keyboard.remove_keyboard()

