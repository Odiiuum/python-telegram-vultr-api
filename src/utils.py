import requests
import datetime

from config import *
from variables import *
from sqlite import *


async def user_access(user_id):
    if int(user_id) in allow_users:
        return True
    else:
        return False
    
async def get_balance():

    billing = requests.get(url["billing"], headers=headers)
    current_balance = round(billing.json()['billing_history'][0]['balance'], 2)
    if current_balance > 0:
        current_balance_message = f"Current balance (debt): -{abs(current_balance)}💲"
    elif current_balance < 0:
        current_balance_message = f"Current balance: {abs(current_balance)}💲"
    else:
        current_balance_message = f"Current balance: 0💲"
    return current_balance_message

async def get_data_api_on_deploy():
    os_response = requests.get(url_table['os_table'], headers=headers)
    region_response = requests.get(url_table['region_table'], headers=headers)
    plans_response = requests.get(url_table['plans_table'], headers=headers)
    await db_save(os_response.json(), region_response.json(), plans_response.json())

