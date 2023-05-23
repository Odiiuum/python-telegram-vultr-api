from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import time

from config import *
from utils import *
from keyboards import *
from sqlite import *

password_ssh = None

bot = Bot(bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(_):
    await db_start()

class RegistrationStates(StatesGroup):
    START = State()
    CONF_SUBMENU = State()
    GET_NAME_DEPLOY = State()
    CHOOSE_OS_DEPLOY = State()
    CHOOSE_REGION_DEPLOY = State()
    CONFIRM_DATA_DEPLOY = State()

    CHOOSE_INSTANCE_REMOVE = State()
    CONFIRM_DATA_REMOVE = State()

@dp.message_handler(commands=['start'], state="*")
async def start_command(message: types.Message):
    name = message.from_user.first_name
    await dp.storage.reset_data(user=message.from_user.id)
    await message.answer(f"Привет, {name}! Чем могу помочь?",
                         reply_markup=get_menu(main_menu))
    
    await RegistrationStates.START.set()


@dp.message_handler(content_types=["text"], state=RegistrationStates.START)
async def text_command(message: types.Message):

    if message.text == "Баланс счёта":
        await message.answer(check_balance())

    elif message.text == "Активные сервера":
        await bot.send_message(message.chat.id,
                            get_data_instances())

    elif message.text == "Настройка серверов":
        await RegistrationStates.CONF_SUBMENU.set()
        await message.answer("Выбери, что тебя интересует.",
                         reply_markup=get_menu(config_server_menu))

@dp.message_handler(content_types=["text"], state=RegistrationStates.CONF_SUBMENU)
async def handle_server_setup(message: types.Message, state: FSMContext):
    if message.text == "Деплой сервера":
        await RegistrationStates.GET_NAME_DEPLOY.set()
        await message.answer("Введи имя сервера.", reply_markup=ReplyKeyboardRemove())
        
    elif message.text == "Удаление сервера":
        await message.answer("Список активных серверов:\n\n"+get_data_instances())
        await message.answer("Выбери инстанс для удаления:", 
                            reply_markup=create_inline_keyboard(get_name_id()))
        await bot.send_message(message.chat.id, 
                                text="Чтобы вернуться обратно, нажми кнопку Отменить.",
                                reply_markup=cancel_keyboard)
        await RegistrationStates.CHOOSE_INSTANCE_REMOVE.set()

    elif message.text == "Вернуться в главное меню":
        await RegistrationStates.START.set()
        await message.answer("Ты вернулся в главное меню.",
                         reply_markup=get_menu(main_menu))


@dp.message_handler(state=RegistrationStates.GET_NAME_DEPLOY)
async def handle_name(message: types.Message, state: FSMContext):
    name = message.text
    
    await state.update_data(name=name)
    await RegistrationStates.CHOOSE_OS_DEPLOY.set()
    await message.answer("Теперь выбери операционную систему из списка:", 
                            reply_markup=os_keyboard)
    await bot.send_message(message.chat.id, 
                           text="Чтобы вернуться обратно, нажми кнопку Отменить.",
                           reply_markup=cancel_keyboard)


@dp.callback_query_handler(state=RegistrationStates.CHOOSE_OS_DEPLOY)
async def handle_conf_os(callback_query: types.CallbackQuery, state: FSMContext):
    os = callback_query.data
    current_os = reversed_os_dict[int(os)]

    await state.update_data(os=current_os)
    await RegistrationStates.CHOOSE_REGION_DEPLOY.set()
    await bot.edit_message_text("Теперь выбери регион из списка:",
                                callback_query.from_user.id,
                                callback_query.message.message_id, 
                                reply_markup=region_keyboard)


@dp.callback_query_handler(state=RegistrationStates.CHOOSE_REGION_DEPLOY)
async def handle_conf_region(callback_query: types.CallbackQuery, state: FSMContext):
    region = callback_query.data
    current_region = regions_dict[region]

    await state.update_data(region=current_region)
    await RegistrationStates.CONFIRM_DATA_DEPLOY.set()

    async with state.proxy() as data:
        name = data['name']
        os = data['os']
        region = data['region']

    message_text = f"Подтверди введенные данные:\n\nИмя инстанса: {name}\nOS: {os}\nГород: {region}"
    
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
        await state.finish()
        await callback_query.answer("Запрос отправлен")
        password_ssh = None #post_create_instances_and_get_password()
        await bot.send_message(callback_query.from_user.id, 
                                "Деплой сервера начался, он будет готов через одну минуту, ты перенаправлен в меню серверов.",
                                reply_markup=get_menu(config_server_menu))
        await bot.send_message(callback_query.from_user.id, f"Пароль от нового сервера: {password_ssh}")
        #time.sleep(5)
        await RegistrationStates.CONF_SUBMENU.set()

    elif callback_query.data == "change":
        await RegistrationStates.GET_NAME_DEPLOY.set()
        await bot.send_message(callback_query.from_user.id, "Введите новое имя:")

@dp.callback_query_handler(state=RegistrationStates.CHOOSE_INSTANCE_REMOVE)
async def handle_remove_button(callback_query: types.CallbackQuery, state: FSMContext):
    global remove_id
    remove_button_value = callback_query.data

    await state.update_data(remove_button_value=remove_button_value)

    await RegistrationStates.CONFIRM_DATA_REMOVE.set()

    async with state.proxy() as data:
        remove_id = data['remove_button_value']

    name_remove_instances = remove_instances_get_fullname(get_data_instances() ,remove_id)

    message_text = f"Подтверди удаление инстанса:\n\n{name_remove_instances}"
    
    cancel_submenu = get_confirmation_menu(cancel_submenu_name, cancel_submenu_callback)
    await bot.send_message(callback_query.from_user.id, message_text, 
                            reply_markup=cancel_submenu)


@dp.callback_query_handler(state=RegistrationStates.CONFIRM_DATA_REMOVE)
async def handle_confirmatio_remove(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "confirm":
        await state.finish()
        await callback_query.answer("Запрос отправлен")
        #delete_instances(remove_id)
        await bot.send_message(callback_query.from_user.id, 
                                "Удаление сервера началось. Ты перенаправлен в меню серверов.",
                                reply_markup=get_menu(config_server_menu))
        #time.sleep(5)
        await RegistrationStates.CONF_SUBMENU.set()

    elif callback_query.data == "cancel":
        await RegistrationStates.CHOOSE_INSTANCE_REMOVE.set()
        await bot.send_message(callback_query.from_user.id, "Выбери инстанс для удаления", 
                                reply_markup=create_inline_keyboard(get_name_id()))


@dp.message_handler(text="Отменить" ,state=[RegistrationStates.CHOOSE_OS_DEPLOY,
                                            RegistrationStates.CHOOSE_REGION_DEPLOY, 
                                            RegistrationStates.CONFIRM_DATA_DEPLOY,
                                            RegistrationStates.CHOOSE_INSTANCE_REMOVE])
async def handle_cancel(message: types.Message, state: FSMContext):
    await state.finish()  
    await message.answer("Ты отменил действие. Попробуй еще раз, или выбери другую функцию",
                         reply_markup=get_menu(config_server_menu))
    await RegistrationStates.CONF_SUBMENU.set()




if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
