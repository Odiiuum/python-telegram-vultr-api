import asyncio
import subprocess
import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import *
from ssh import *
from utils import *
from keyboards import *
from sqlite import *

bot = Bot(bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(_):
    await db_start()
#    await insert_data_to_database(id, name, date)

class RegistrationStates(StatesGroup):
    START = State()
    CONF_SUBMENU = State()
    GET_NAME_DEPLOY = State()
    CHOOSE_OS_DEPLOY = State()
    CHOOSE_REGION_DEPLOY = State()
    CONFIRM_DATA_DEPLOY = State()

    GET_NAME_USER_SERVER = State()
    GET_PASSWORD_USER_SERVER = State()
    GET_IPSEC_KEY_SERVER = State()
    GET_SUBNET_SERVER = State()
    CONFIRM_DATA_SERVER = State()

    CHOOSE_INSTANCE_REMOVE = State()
    CONFIRM_DATA_REMOVE = State()


@dp.message_handler(commands=['start'], state="*")
async def start_command(message: types.Message):
    user_id = message.from_user.id
    if user_access(user_id) == True:
        name = message.from_user.first_name
        await dp.storage.reset_data(user=message.from_user.id)
        await message.answer("Hi, {}! How can I help you?".format(name),
                            reply_markup=get_menu(main_menu))
        await RegistrationStates.START.set()
    else:
        await message.answer("You do not have access to this bot.\nIn order to get access to the bot, write @sh_side. Your User_id {}".format(user_id))
        #return


@dp.message_handler(content_types=["text"], state=RegistrationStates.START)
async def text_command(message: types.Message):
    if message.text == "💰 Balance Account 💰":
        await message.answer(check_balance())
    elif message.text == "🆙 Active Servers 🆙":
        await message.answer(get_data_instances(get_instances()))
    elif message.text == "🛠 Config Servers 🛠":
        await RegistrationStates.CONF_SUBMENU.set()
        await message.answer("Choose what interests you.",
                            reply_markup=get_menu(config_server_menu))


@dp.message_handler(content_types=["text"], state=RegistrationStates.CONF_SUBMENU)
async def handle_server_setup(message: types.Message, state: FSMContext):
    if message.text == "🧩 Deploy new server 🧩":
        await RegistrationStates.GET_NAME_DEPLOY.set()
        await message.answer("Enter server name.", reply_markup=ReplyKeyboardRemove())
    elif message.text == "❌ Delete server ❌":
        await RegistrationStates.CHOOSE_INSTANCE_REMOVE.set()
        await message.answer("Active Servers List:\n\n" + get_data_instances(get_instances()))
        await message.answer("Select instance to delete:", 
                             reply_markup=get_inline_menu(get_remove_data(get_instances())))
        await bot.send_message(message.chat.id, 
                                text="To go back, click the \"⛔️ Cancel ⛔️\" button.",
                                reply_markup=get_button("⛔️ Cancel ⛔️"))
    elif message.text == "⏪ Back to main menu ⏪":
        await RegistrationStates.START.set()
        await message.answer("You returned to main menu.",
                         reply_markup=get_menu(main_menu))


@dp.message_handler(state=RegistrationStates.GET_NAME_DEPLOY)
async def handle_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await RegistrationStates.CHOOSE_OS_DEPLOY.set()
    await message.answer("Select an operating system from the list:", 
                            reply_markup=get_inline_menu(os_dict))
    await bot.send_message(message.chat.id, 
                           text="To go back, click the \"⛔️ Cancel ⛔️\" button.",
                           reply_markup=get_button("⛔️ Cancel ⛔️"))


@dp.callback_query_handler(state=RegistrationStates.CHOOSE_OS_DEPLOY)
async def handle_conf_os(callback_query: types.CallbackQuery, state: FSMContext): 
    current_os = reversed_os_dict[int(callback_query.data)]

    await state.update_data(os=current_os)
    await RegistrationStates.CHOOSE_REGION_DEPLOY.set()
    await bot.edit_message_text("Select an region from the list:",
                                callback_query.from_user.id,
                                callback_query.message.message_id, 
                                reply_markup=get_inline_menu(reversed_regions_dict))


@dp.callback_query_handler(state=RegistrationStates.CHOOSE_REGION_DEPLOY)
async def handle_conf_region(callback_query: types.CallbackQuery, state: FSMContext):
    current_region = regions_dict[callback_query.data]

    await state.update_data(region=current_region)
    await RegistrationStates.CONFIRM_DATA_DEPLOY.set()

    async with state.proxy() as data:
        name = data['name']
        os = data['os']
        region = data['region']

    message_text = f"Confirm the entered data:\n\nName server: {name}\nOS: {os}\nRegion: {region}"
    
    global data_instances
    data_instances["label"] = name
    data_instances["os_id"] = os_dict[os]
    data_instances["region"] = reversed_regions_dict[region]

    confirm_submenu = get_confirmation_menu(confirm_submenu_name, confirm_submenu_callback)
    await bot.send_message(callback_query.from_user.id, message_text, 
                            reply_markup=confirm_submenu)


@dp.callback_query_handler(state=RegistrationStates.CONFIRM_DATA_DEPLOY)
async def handle_confirmation_deploy(callback_query: types.CallbackQuery, state: FSMContext):
    global password_ssh
    if callback_query.data == "confirm":
        await callback_query.answer("Requests sended")
        password_ssh = None #create_instances_and_get_password() # post requests for api
        await state.update_data(password_ssh=password_ssh)
        await RegistrationStates.GET_NAME_USER_SERVER.set()
        await bot.send_message(callback_query.from_user.id, 
                               "Now you need to configure the server.")
        await bot.send_message(callback_query.from_user.id,
                               "Enter a username on access to server:",
                               reply_markup=get_button("⛔️ Cancel ⛔️"))

    elif callback_query.data == "change":
        await RegistrationStates.GET_NAME_DEPLOY.set()
        await bot.send_message(callback_query.from_user.id, "Enter new label:")


@dp.message_handler(state=RegistrationStates.GET_NAME_USER_SERVER)
async def handle_get_user_server(message: types.Message, state: FSMContext):
    user_name = message.text
    await state.update_data(user_name=user_name)
    await RegistrationStates.GET_PASSWORD_USER_SERVER.set()
    await message.answer("Enter a password on access to server:") 
 

@dp.message_handler(state=RegistrationStates.GET_PASSWORD_USER_SERVER)
async def handle_get_password_server(message: types.Message, state: FSMContext):
    user_password = message.text
    await state.update_data(user_password=user_password)
    await message.answer("Enter a IPSec key on access to server:")    
    await RegistrationStates.GET_IPSEC_KEY_SERVER.set()


@dp.message_handler(state=RegistrationStates.GET_IPSEC_KEY_SERVER)
async def handle_get_password_server(message: types.Message, state: FSMContext):
    ipsec_key = message.text
    await state.update_data(ipsec_key=ipsec_key)
    await message.answer("Enter a subnet to VPN server(e.g 10.100.200.100-10.100.200.200):")    
    await RegistrationStates.GET_SUBNET_SERVER.set()


@dp.message_handler(state=RegistrationStates.GET_SUBNET_SERVER)
async def handle_get_password_server(message: types.Message, state: FSMContext):
    subnet_vpn = message.text
    await state.update_data(subnet_vpn=subnet_vpn)
    await message.answer("Enter:")    
    await RegistrationStates.CONFIRM_DATA_SERVER.set()

    async with state.proxy() as data:
        user_name = data['user_name']
        user_password = data['user_password']
        ipsec_key = data['ipsec_key']
        subnet_vpn = data['subnet_vpn']

    global config_server
    config_server["username"] = user_name
    config_server["password"] = user_password
    config_server["ipsec"] = ipsec_key
    config_server["subnet"] = subnet_vpn

    print(config_server)

    message_text = """
Confirm the entered data:

Username server: {}
User password server: {}
IPSec Key VPN: {}
Subnet VPN server: {}
""".format(user_name, user_password, ipsec_key, subnet_vpn)
 
    confirm_submenu = get_confirmation_menu(confirm_submenu_name, confirm_submenu_callback)
    await message.answer(message_text, reply_markup=confirm_submenu)


@dp.callback_query_handler(state=RegistrationStates.CONFIRM_DATA_SERVER)
async def handle_remove_button(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "confirm":
        await callback_query.answer("Requests sended")
        await bot.send_message(callback_query.from_user.id, 
                                "The server deployment has started, it will be ready in five minute.")
        
        #remove_ip = get_main_ips(get_instances())[-1].split(": ")[1]
        #await ssh_upload_install_scripts(str(remove_ip), password_ssh) #upload & run scripts

        await RegistrationStates.CONF_SUBMENU.set()
        await bot.send_message(callback_query.from_user.id,
                               "Yot returned in the server menu.",
                               reply_markup=get_menu(config_server_menu))
        
    elif callback_query.data == "change":
        await RegistrationStates.GET_NAME_USER_SERVER.set()
        await bot.send_message(callback_query.from_user.id, "Enter new user:")


@dp.callback_query_handler(state=RegistrationStates.CHOOSE_INSTANCE_REMOVE)
async def handle_remove_button(callback_query: types.CallbackQuery, state: FSMContext):
    global remove_id
    remove_button_value = callback_query.data
    await state.update_data(remove_button_value=remove_button_value)
    async with state.proxy() as data:
        remove_id = data['remove_button_value']
    name_remove_instances = instances_get_fullname(get_data_instances(get_instances()) ,remove_id)
    message_text = f"Confirm the deleted data:\n\n{name_remove_instances}"
    cancel_submenu = get_confirmation_menu(cancel_submenu_name, cancel_submenu_callback)
    await bot.send_message(callback_query.from_user.id, message_text, 
                            reply_markup=cancel_submenu)
    await RegistrationStates.CONFIRM_DATA_REMOVE.set()


@dp.callback_query_handler(state=RegistrationStates.CONFIRM_DATA_REMOVE)
async def handle_confirmatio_remove(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "confirm":
        await state.finish()
        await callback_query.answer("Requests sended")
        #delete_instances(remove_id)
        await bot.send_message(callback_query.from_user.id, 
                                "Server removal has begun. You are redirected to the servers menu.",
                                reply_markup=get_menu(config_server_menu))
        await RegistrationStates.CONF_SUBMENU.set()

    elif callback_query.data == "cancel":
        await RegistrationStates.CHOOSE_INSTANCE_REMOVE.set()
        await bot.send_message(callback_query.from_user.id,
                                "Select instance to delete:", 
                                reply_markup=get_inline_menu(get_remove_data(get_instances())))


@dp.message_handler(text="⛔️ Cancel ⛔️" ,state=[RegistrationStates.CHOOSE_OS_DEPLOY,
                                            RegistrationStates.CHOOSE_REGION_DEPLOY, 
                                            RegistrationStates.CONFIRM_DATA_DEPLOY,
                                            RegistrationStates.CHOOSE_INSTANCE_REMOVE,
                                            RegistrationStates.GET_NAME_USER_SERVER,
                                            RegistrationStates.GET_PASSWORD_USER_SERVER,
                                            RegistrationStates.GET_IPSEC_KEY_SERVER,
                                            RegistrationStates.GET_SUBNET_SERVER])
async def handle_cancel(message: types.Message, state: FSMContext):
    await state.finish()  
    await message.answer("You canceled the action. Try again or choose another function.",
                         reply_markup=get_menu(config_server_menu))
    await RegistrationStates.CONF_SUBMENU.set()



if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    
