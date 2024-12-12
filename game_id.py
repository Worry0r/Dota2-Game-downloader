import requests
import sqlite3

# api URL
url = "https://api.opendota.com/api/proMatches"

conn = sqlite3.connect("matches.db")
cursor = conn.cursor()

# Update sqlite table = match_id (unique) + downloaded (0 by default) + meta_downloaded (0 by default)
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY,               -- Match ID (unieuq)
    downloaded INTEGER DEFAULT 0,          -- is replay downloaded 0 = No, 1 = Yes
    meta_downloaded INTEGER DEFAULT 0     -- are metadata downloaded 0 = No, 1 = Yes
)
""")
conn.commit()

# Download and insert match_is from api
response = requests.get(url)

if response.status_code == 200:
    matches = response.json()

    for match in matches:
        match_id = match.get("match_id")
        try:
            cursor.execute("INSERT INTO matches (id) VALUES (?)", (match_id,))
            print(f"New match detected: {match_id}")
        except sqlite3.IntegrityError:
            print(f"Match with ID {match_id} already exists.")
    conn.commit()
else:
    print(f"Error while downloading data: HTTP {response.status_code}")

conn.close()
