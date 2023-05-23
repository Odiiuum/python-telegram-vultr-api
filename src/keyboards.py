from utils import *
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# --- create menu ---
def get_menu(buttons_name_list):
    buttons = []
    for text_button in buttons_name_list:
        button = types.KeyboardButton(text_button)
        buttons.append(button)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard

def get_confirmation_menu(buttons_name_list, callback_data_list):
    buttons = []
    for i, text_button in enumerate(buttons_name_list):
        callback_data = callback_data_list[i]
        button = types.InlineKeyboardButton(text_button, callback_data=callback_data)
        buttons.append(button)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard

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

