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

# --- create inline confirm menu ---
def get_confirmation_menu(buttons_name_list, callback_data_list):
    buttons = []
    for i, text_button in enumerate(buttons_name_list):
        callback_data = callback_data_list[i]
        button = types.InlineKeyboardButton(text_button, callback_data=callback_data)
        buttons.append(button)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard

# --- create inline keyboard from dict ---
def get_inline_menu(dict):
    buttons = []
    for name, key in dict.items():
        region_button = types.InlineKeyboardButton(name, callback_data=key)
        buttons.append(region_button)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard

# --- cancel configuring instances button
def get_button(name_button):
    button = types.KeyboardButton(name_button)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    return keyboard

# --- REFACTORING FUNC ---
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

