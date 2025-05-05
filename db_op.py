import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''DROP TABLE characters''')
conn.commit()
conn.close()