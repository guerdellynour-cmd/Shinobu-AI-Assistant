import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shinobu.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# to insert values  // replace visual studio code with any app u have

# query = "INSERT INTO sys_command VALUES (null,'WhatsApp', 'C:\\Program Files\\WindowsApps\\************\\WhatsApp.exe')"//
# cursor.execute(query)
conn.commit()

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

# to insert values  // replace facebook with any link u want

# query = "INSERT INTO web_command VALUES (null,'Canva', 'https://canva.com')"
# cursor.execute(query)
conn.commit()

conn.close()

# #testing module
# query = "Visual Studio Code"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (query,))
# results = cursor.fetchall()
# print(results[0][0])