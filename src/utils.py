import requests
import time

from config import *
from variables import *


def user_access(user_id):
    if int(user_id) in allow_users:
        return True
    else:
        return False
    

def check_balance():
    billing = requests.get(url_biling, headers=headers)
    current_balance = round(billing.json()['billing_history'][0]['balance'], 2)
    if current_balance > 0:
        current_balance_message = f"Current balance (debt): -{abs(current_balance)}💲"
    elif current_balance < 0:
        current_balance_message = f"Current balance: {abs(current_balance)}💲"
    else:
        current_balance_message = f"Current balance: 0💲"
    return current_balance_message

instances = requests.get(url_instances, headers=headers)

def get_label_instances(instances):
    labels = [label['label'] for label in instances.json()['instances']]
    label_instances = ["Name server: " + label for label in labels]
    return label_instances

def get_region_instances(instances):
    regions = [region['region'] for region in instances.json()['instances']]
    region_instances = [regions_dict.get(region) for region in regions]
    region_instances = ["Region: " + region for region in region_instances]
    return region_instances

def get_os_instances(instances):
    os_instances = [os['os'] for os in instances.json()['instances']]
    os_instances = ["OS: " + os for os in os_instances]
    return os_instances

def get_main_ips(instances):
    main_ips = [ip_addr['main_ip'] for ip_addr in instances.json()['instances']]
    main_ips = ["IP: " + ip for ip in main_ips]
    return main_ips

def get_power_instances(instances):
    power_instances = [power['power_status'] for power in instances.json()['instances']]
    power_instances = ["Status server: " + power for power in power_instances]
    return power_instances

def get_date_created_instances(instances):
    date_created_instances = [date['date_created'] for date in instances.json()['instances']]
    dates_created = []
    for item in date_created_instances:
        date = item.split("T")[0]
        dates_created.append(date)
    date_created_instances = ["Date created: " + date for date in dates_created]
    return date_created_instances

def get_id_instances(instances):
    id_instances = [id['id'] for id in instances.json()['instances']]
    id_instances = ["ID instances: " + id for id in id_instances]
    return id_instances

def get_all_servers_data(label_instances, region_instances, os_instances, main_ips, power_instances, date_created_instances, id_instances):
    all_servers_data = '\n'.join([f"{label}\n{region}\n{os}\n{ip}\n{power}\n{date}\n{id}\n" for label, region, os, ip, power, date, id in zip(label_instances, region_instances, os_instances, main_ips, power_instances, date_created_instances, id_instances)])
    return all_servers_data

def get_data_instances():
    label_instances = get_label_instances(instances)
    region_instances = get_region_instances(instances)
    os_instances = get_os_instances(instances)
    main_ips = get_main_ips(instances)
    power_instances = get_power_instances(instances)
    date_created_instances = get_date_created_instances(instances)
    id_instances = get_id_instances(instances)
    all_servers_data = get_all_servers_data(label_instances, region_instances, os_instances, main_ips, power_instances, date_created_instances, id_instances)
    return all_servers_data

# ----- REFACTORING CODE ------

def get_remove_data(instances):
    label_instances = [label['label'] for label in instances.json()['instances']]
    id_instances = [id['id'] for id in instances.json()['instances']]
    merged_dict = dict(zip(label_instances, id_instances))
    return merged_dict


#getting id os, concat all
os = requests.get(url_os, headers=headers)
id_os = [id['id'] for id in os.json()['os']]
name_os = [name['name'] for name in os.json()['os']]
os_dict = dict(zip(name_os, id_os))

#getting id regions and city, concat all
regions = requests.get(url_regions, headers=headers)
id_regions = [id['id'] for id in regions.json()['regions']]
city_regions = [city['city'] for city in regions.json()['regions']]
regions_dict = dict(zip(id_regions, city_regions))

reversed_os_dict = {}
for os_id, os_name in os_dict.items():
    reversed_os_dict[os_name] = os_id

reversed_regions_dict = {}
for region_id, region_name in regions_dict.items():
    reversed_regions_dict[region_name] = region_id

def create_instances_and_get_password():
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
