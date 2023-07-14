url = {
    "billing": "https://api.vultr.com/v2/billing/history",
    "instances": "https://api.vultr.com/v2/instances",
    "regions": "https://api.vultr.com/v2/regions",
    "plans": "https://api.vultr.com/v2/plans",
    "os": "https://api.vultr.com/v2/os"
}

url_table = {
    "os_table": url['os'],
    "region_table": url["regions"],
    "plans_table": url["plans"]
}

table_data_list = [
    "os_table",
    "region_table",
    "plans_table"
]

#plan instances
plan = "vhp-1c-1gb-amd"

data_instances = {
    "region": None,
    "plan" : plan,
    "label": None,
    "os_id": None,
    "backups": "disabled",
    "ddos_protection" : False
}

config_server = {
    "username" : None,
    "password" : None,
    "ipsec" : None,
    "subnet" : None
}

main_menu = ["💰 Balance Account 💰", "🆙 Active Servers 🆙", "🛠 Config Servers 🛠", ]
server_config_menu = ["🧩 Deploy new server 🧩", "❌ Delete server ❌", "⏪ Back to main menu ⏪"]



change_submenu_name = ["Confirm ✅", "Change ❓"]
change_submenu_callback = ["confirm", "change"]

cancel_submenu_name = ["Confirm ✅", "Cancel ❌"]
cancel_submenu_callback = ["confirm", "cancel"]
