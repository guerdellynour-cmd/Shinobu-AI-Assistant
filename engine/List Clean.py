import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shinobu.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. See what's currently in the table
cursor.execute("SELECT id, name, path FROM sys_command")
rows = cursor.fetchall()
print("Current sys_command rows:")
for row in rows:
    print(row)

# 2. Delete a specific row by its id (change 2 to whichever id you want to remove)

cursor.execute("DELETE FROM sys_command WHERE id = ?", (3,))
conn.commit()

# 3. OR: delete all duplicates, keeping only the row with the smallest id per name
# cursor.execute("""
#     DELETE FROM sys_command
#     WHERE id NOT IN (
#         SELECT MIN(id) FROM sys_command GROUP BY name
#     )
# """)
# conn.commit()

conn.close()