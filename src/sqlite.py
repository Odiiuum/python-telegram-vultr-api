import sqlite3

async def db_start():
    global db, cur

    db = sqlite3.connect("db/bot.db")
    cur = db.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS servers
                (id TEXT UNIQUE , name TEXT, date_created TEXT)''')
    db.commit()

async def insert_data_to_database(id_list, label_list, date_list):
    for i in range(len(date_list)):
        date = date_list[i].split(': ')[1]
        label = label_list[i].split(': ')[1]
        id = id_list[i].split(': ')[1]
        cur.execute("INSERT OR IGNORE INTO servers (id, name, date_created) VALUES (?, ?, ?)", (id, label, date))
    
    db.commit()

