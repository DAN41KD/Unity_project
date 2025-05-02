import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
        id INTEGER NOT NULL UNIQUE
        vards TEXT,
        speks TEXT,
        veikliba TEXT,
        izturiba TEXT,
        harizma TEXT,
        manipulacija TEXT,
        savaldiba TEXT,
        intelekts TEXT,
        prats TEXT,
        apnemiba TEXT,
        data DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY("id" AUTOINCREMENT)
        )
    ''')
    conn.commit()
    conn.close()

init_db()
