from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# --- create menu ---
async def create_reply_menu(button_name_list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for button_name in button_name_list:
        keyboard.add(KeyboardButton(button_name))
    return keyboard

async def create_inline_menu(button_name_list, callback_data_list):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for button_name, callback_data in zip(button_name_list, callback_data_list):
        keyboard.insert(InlineKeyboardButton(button_name, callback_data=callback_data))
    return keyboard

async def create_reply_button(button_name):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_name)
    return keyboard