import requests
from config import *
#from debug import *
import json
import time
import re
from aiogram.utils import markdown

# variables
url_biling = "https://api.vultr.com/v2/billing/history"
url_instances = "https://api.vultr.com/v2/instances"
url_regions =  "https://api.vultr.com/v2/regions"
#url_plans =  "https://api.vultr.com/v2/plans"
url_os =  "https://api.vultr.com/v2/os"

#getting id os
plan = "vc2-1c-1gb"

data_instances = {
    "region": None,
    "plan" : plan,
    "label": None,
    "os_id": None,
    "backups": "disabled",
    "ddos_protection" : False
}

name_servers = None
id_servers = None
create_servers = None

#getting id os, concat all
os = requests.get(url_os, headers=headers)
id_os = [id['id'] for id in os.json()['os']]
name_os = [name['name'] for name in os.json()['os']]
os_dict = dict(zip(name_os, id_os))

reversed_os_dict = {}
for os_id, os_name in os_dict.items():
    reversed_os_dict[os_name] = os_id

#getting id regions and city, concat all
regions = requests.get(url_regions, headers=headers)
id_regions = [id['id'] for id in regions.json()['regions']]
city_regions = [city['city'] for city in regions.json()['regions']]
regions_dict = dict(zip(id_regions, city_regions))

reversed_regions_dict = {}
for region_id, region_name in regions_dict.items():
    reversed_regions_dict[region_name] = region_id

#print(reversed_regions_dict)

def check_balance():
    #getting current balance 
    billing = requests.get(url_biling, headers=headers)
    current_balance = round(billing.json()['billing_history'][0]['balance'], 2)

    if current_balance > 0:
        current_balance_message = f"Текущий баланс (долг): -{abs(current_balance)}$"
    elif current_balance < 0:
        current_balance_message = f"Текущий баланс : {abs(current_balance)}$"
    else:
        current_balance_message = f"Текущий баланс : 0$"

    return current_balance_message

def get_name_id():
    get_data_instances()
    data_name_id_dict = [{key: value} for key, value in zip(name_servers, id_servers)]
    return data_name_id_dict

def get_data_instances():
    global name_servers, id_servers, create_servers
    #getting active instances
    instances = requests.get(url_instances, headers=headers)
    #getting name instances
    label_instances = [label['label'] for label in instances.json()['instances']]
    name_servers = label_instances
    label_instances = ["Name server: " + label for label in label_instances ]
    #getting name instances
    region_instances = [region['region'] for region in instances.json()['instances']]
    region_instances = [regions_dict.get(region) for region in region_instances]
    region_instances = ["Region: " + region for region in region_instances ]
    #getting os instances
    os_instances = [os['os'] for os in instances.json()['instances']]
    os_instances = ["OS: " + os for os in os_instances ]
    #getting ip instances
    main_ips = [ip_addr['main_ip'] for ip_addr in instances.json()['instances']]
    main_ips = ["IP: " + ip for ip in main_ips ]
    #getting power instances
    power_instances = [power['power_status'] for power in instances.json()['instances']]
    power_instances = ["Status server: " + power for power in power_instances ]

    date_created_instances = [date['date_created'] for date in instances.json()['instances']]
    dates_created = []
    for item in date_created_instances:
        date = item.split("T")[0]
        dates_created.append(date)
    create_servers = dates_created
    date_created_instances = ["Date created: " + date for date in dates_created ]

    id_instances = [id['id'] for id in instances.json()['instances']]
    id_servers = id_instances
    id_instances = ["ID instances: " + id for id in id_instances ]

    all_servers_data = '\n'.join([f"{label}\n{region}\n{os}\n{ip}\n{power}\n{date}\n{id}\n" for label, region, os, ip, power, date, id in zip(label_instances, region_instances, os_instances, main_ips, power_instances, date_created_instances, id_instances)])

    return all_servers_data


def post_create_instances_and_get_password():
    response = requests.post(url_instances, json=data_instances, headers=headers)
    time.sleep(30)
    instance_password = response.json()["instance"]["default_password"]
    return instance_password


def delete_instances(instance_id):
    remove_instance = url_instances + "/" + instance_id
    response = requests.delete(remove_instance, headers=headers)


def remove_instances_get_fullname(text, remove_id):
    server_blocks = text.split('\n\n') 

    server_dataset = []
    for block in server_blocks:
        if f"ID instances: {remove_id}" in block:
            server_dataset.append(block)

    if server_dataset:
        server_dataset = "\n\n".join(server_dataset)
    else:
        server_dataset = None

    return server_dataset
