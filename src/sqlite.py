import sqlite3
from datetime import datetime

async def db_start():
    global db, cur

    db = sqlite3.connect("db/bot.db")
    cur = db.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS servers
                (id_instance TEXT PRIMARY KEY UNIQUE, 
                name_instance TEXT,
                ip_instance TEXT,
                os_instance TEXT,
                region_instance TEXT,
                plan_instance TEXT,
                date_created TEXT)
                ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS os_table
                (id TEXT PRIMARY KEY UNIQUE,
                os_name TEXT)
                ''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS regions_table
                (id TEXT PRIMARY KEY UNIQUE,
                region_city TEXT)
                ''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS plans_table
                (id TEXT PRIMARY KEY UNIQUE)
                ''')
    db.commit()

async def db_save(os_response, regions_response, plans_response):
    global db, cur
    
    os_data = os_response['os']
    for data in os_data:
        os_id = data['id']
        os_name = data['name']
        cur.execute("INSERT OR IGNORE INTO os_table (id, os_name) VALUES (?, ?)", (os_id, os_name))
        db.commit()

    regions_data = regions_response['regions']
    for data in regions_data:
        region_id = data['id']
        region_city = data['city']
        cur.execute("INSERT OR IGNORE  INTO regions_table (id, region_city) VALUES (?, ?)", (region_id, region_city))
        db.commit()

    plans_data = plans_response['plans']
    for data in plans_data:
        plans_id = data['id']
        cur.execute("INSERT OR IGNORE INTO plans_table (id) VALUES (?)", (plans_id,))
        db.commit()

async def db_get_data(table_name, field):
    global db, cur

    cur.execute("SELECT id, {} FROM {}".format(field, table_name))
    rows = cur.fetchall()

    id_list = []
    data_list = []
    for row in rows:
        id_list.append(row[0])
        data_list.append(row[1])

    return id_list, data_list









    #for item in enumerate(field_item):
    #for item, id_value in zip(field_item, field_id):
        #for field in response[item]:

            #data = field[id_value]
            #id = field['id']
            #cur.execute("INSERT OR IGNORE INTO {} (data, id, last_updated) VALUES (?, ?, datetime('now', 'localtime'))".format(table_name), (data, id))

#        else:
#            id = item['id']
#            cur.execute("INSERT OR IGNORE INTO {} (id, last_updated) VALUES (?, datetime('now', 'localtime'))".format(table_name), (id))

#        db.commit()


async def get_last_update_date(table_name):
    global db, cur

    cur.execute("SELECT last_updated FROM {} ORDER BY last_updated DESC LIMIT 1".format(
                table_name))
    last_updated = cur.fetchone()

    if last_updated:
        return last_updated[0] 
    else:
        return None