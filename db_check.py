import sqlite3

# Database check if needed
conn = sqlite3.connect("matches.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM matches")
all_matches = cursor.fetchall()
print("\nZáznamy v databázi:")
for row in all_matches:
    print(row)

conn.close()