import asyncio
import subprocess
import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import *
from utils import *
from keyboards import *
from sqlite import *

bot = Bot(bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(_):
    await db_start()
    await get_data_api_on_deploy()

class RegistrationStates(StatesGroup):
    MAIN_MENU_STATE = State()
    SERVER_MENU_STATE = State()
    DEPLOY_GET_NAME_STATE = State()
    DEPLOY_CHOOSE_OS_STATE = State()
    DEPLOY_CHOOSE_REGION_STATE = State()
    DEPLOY_CONFIRM_CONFIG_STATE = State()
        
@dp.message_handler(commands=['start'], state="*")
async def start_command_handler(message: types.Message):
    user_id = message.from_user.id
    if await user_access(user_id) == True:
        name = message.from_user.first_name
        await dp.storage.reset_data(user=message.from_user.id)
        await message.answer("Hi, {}! How can I help you?".format(name),
                            reply_markup=await create_reply_menu(main_menu))
        await RegistrationStates.MAIN_MENU_STATE.set()

    else:
        await message.answer("You do not have access to this bot.\nIn order to get access to the bot, write @sh_side.\nYour User_id {}".format(user_id))

@dp.message_handler(content_types=["text"], state=RegistrationStates.MAIN_MENU_STATE)
async def main_menu_handler(message: types.Message, state:FSMContext) -> None:
    if message.text == "💰 Balance Account 💰":
        await message.answer(await get_balance())

    elif message.text == "🆙 Active Servers 🆙":
        await message.answer("Development now.")
       # await get_active_servers()

    elif message.text == "🛠 Config Servers 🛠":
        await message.answer("Choose what interest you.",
                             reply_markup=await create_reply_menu(server_config_menu))
        await RegistrationStates.SERVER_MENU_STATE.set()

@dp.message_handler(content_types=["text"], state=RegistrationStates.SERVER_MENU_STATE)
async def server_menu_handler(message: types.Message, state:FSMContext) -> None:
    if message.text == "🧩 Deploy new server 🧩":
        keyboard = await create_reply_button("⛔️ Cancel ⛔️")
        await message.answer("Entered server name.", 
                             reply_markup=await create_reply_button("⛔️ Cancel ⛔️"))
        await message.answer("To go back, click the \"⛔️ Cancel ⛔️\" button.")
        await RegistrationStates.DEPLOY_GET_NAME_STATE.set()

    elif message.text == "❌ Delete server ❌":
        await message.answer("Choose server to need remove.", 
                             reply_markup=await create_reply_button("⛔️ Cancel ⛔️"))
        await message.answer("To go back, click the \"⛔️ Cancel ⛔️\" button.")
        #await RegistrationStates.DEPLOY_CHOOSE_REGION_STATE.set()

    elif message.text == "⏪ Back to main menu ⏪":
        keyboard = await create_reply_menu(main_menu)
        await message.answer("You returned to main menu.", reply_markup=keyboard)
        await RegistrationStates.MAIN_MENU_STATE.set()

@dp.message_handler(content_types=["text"], state=RegistrationStates.DEPLOY_GET_NAME_STATE)
async def get_name_deploy_handler(message: types.Message, state:FSMContext) -> None:
    name_server = message.text
    await state.update_data(name_server=name_server)
    await RegistrationStates.DEPLOY_CHOOSE_OS_STATE.set()
    id_list, os_name_list = await db_get_data("os_table", "os_name") # type: ignore
    await message.answer("Select an operating system from the list: ", 
                         reply_markup=await create_inline_menu(os_name_list, id_list))
    await message.answer("To go back, click the \"⛔️ Cancel ⛔️\" button.",
                         reply_markup=await create_reply_button("⛔️ Cancel ⛔️"))
    
@dp.callback_query_handler(state=RegistrationStates.DEPLOY_CHOOSE_OS_STATE)
async def get_os_deploy_hanlder(callback_query: types.CallbackQuery, state:FSMContext) -> None:
    os_server = callback_query.data
    await state.update_data(os_server=os_server)
    await RegistrationStates.DEPLOY_CHOOSE_REGION_STATE.set()
    id_list, region_name_list = await db_get_data("regions_table", "region_city")
    await bot.edit_message_text("Select an region from the list: ",
                                callback_query.from_user.id,
                                callback_query.message.message_id,
                                reply_markup=await create_inline_menu(region_name_list, id_list))

@dp.callback_query_handler(state=RegistrationStates.DEPLOY_CHOOSE_REGION_STATE)
async def get_region_deploy_hanlder(callback_query: types.CallbackQuery, state:FSMContext) -> None:
    region_server = callback_query.data
    await state.update_data(region_server=region_server)
    await RegistrationStates.DEPLOY_CONFIRM_CONFIG_STATE.set()
    id_list, os_name_list = await db_get_data("os_table", "os_name")# type: ignore
    os_dict = dict(zip(id_list, os_name_list))
    id_list, region_name_list = await db_get_data("regions_table", "region_city")# type: ignore
    region_dict = dict(zip(id_list, region_name_list))
    async with state.proxy() as data:
        server_name = data["name_server"]
        os_server = os_dict[data["os_server"]]
        region_server = region_dict[data["region_server"]]

    message_text = """Confirm the entered data:
Name server: {}
OS: {}
Region: {}
    """.format(server_name, os_server, region_server)

    await bot.edit_message_text(message_text,
                                callback_query.from_user.id,
                                callback_query.message.message_id,
                                reply_markup=await create_inline_menu(change_submenu_name, change_submenu_callback))

@dp.callback_query_handler(state=RegistrationStates.DEPLOY_CONFIRM_CONFIG_STATE)
async def get_confirm_config_deploy_hanlder(callback_query: types.CallbackQuery, state:FSMContext) -> None:
    if callback_query.data == "confirm":
        await callback_query.answer("Requests sended")
        await RegistrationStates.SERVER_MENU_STATE.set()
        await bot.send_message(callback_query.from_user.id,
                               "Choose what interest you.",
                               reply_markup=await create_reply_menu(server_config_menu))

    elif callback_query.data == "change":
        await bot.send_message(callback_query.from_user.id,
                               "Enter a new server name")
        await RegistrationStates.DEPLOY_GET_NAME_STATE.set()



@dp.message_handler(text="⛔️ Cancel ⛔️" ,state=[RegistrationStates.DEPLOY_GET_NAME_STATE,
                                            RegistrationStates.DEPLOY_CHOOSE_OS_STATE, 
                                            RegistrationStates.DEPLOY_CHOOSE_REGION_STATE,
                                            RegistrationStates.DEPLOY_CONFIRM_CONFIG_STATE])
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()  
    await message.answer("You canceled the action. Try again or choose another function.",
                         reply_markup=await create_reply_menu(server_config_menu))
    await RegistrationStates.SERVER_MENU_STATE.set()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    
