import sqlite3

async def db_start():
    global db, cur

    db = sqlite3.connect("db/bot.db")
    cur = db.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS servers
                (id TEXT, name TEXT, date TEXT)''')
    db.commit()

async def create_instances(id, name, date):
    cur.execute("INSERT INTO servers VALUES (?, ?, ?)", (id, name, date))
    db.commit()