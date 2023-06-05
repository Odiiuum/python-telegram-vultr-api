url_biling = "https://api.vultr.com/v2/billing/history"
url_instances = "https://api.vultr.com/v2/instances"
url_regions =  "https://api.vultr.com/v2/regions"
#url_plans =  "https://api.vultr.com/v2/plans"
url_os =  "https://api.vultr.com/v2/os"

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


main_menu = ["💰 Balance Account 💰", "🆙 Active Servers 🆙", "🛠 Config Servers 🛠"]
config_server_menu = ["🧩 Deploy new server 🧩", "❌ Delete server ❌", "⏪ Back to main menu ⏪"]

confirm_submenu_name = ["Confirm 👍", "Change 👎"]
confirm_submenu_callback = ["confirm", "change"]

cancel_submenu_name = ["Confirm 👍", "Cancel 👎"]
cancel_submenu_callback = ["confirm", "cancel"]

