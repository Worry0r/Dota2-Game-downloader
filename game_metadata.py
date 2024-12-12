import requests
import sqlite3
import time
import os
import sys
import json

FREE_API_LIMIT_MINUTE = 60

def fetch_and_save_match_details(db_path, limit_per_minute=FREE_API_LIMIT_MINUTE, amount_of_games=sys.maxsize):
    # Fetches match details for games and updates the database.
    # api URL
    base_url = "https://api.opendota.com/api/matches/"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Select matches with metadata 0
    cursor.execute("SELECT id FROM matches WHERE meta_downloaded = 0 LIMIT ?", (amount_of_games,))
    game_ids = [row[0] for row in cursor.fetchall()]

    if not game_ids:
        print("No new matches to update.")
        conn.close()
        return

    call_count = 0
    last_request_time = 0

    # Select or create folder to save metadata
    output_dir = os.path.join(os.path.dirname(__file__), "metadata")
    os.makedirs(output_dir, exist_ok=True)

    for match_id in game_ids:
        now = time.time()
        elapsed_time = now - last_request_time
        if call_count >= limit_per_minute and elapsed_time < 60:
            sleep_time = 60 - elapsed_time
            print(f"Sleeping for {sleep_time:.2f} seconds to respect rate limit...")
            time.sleep(sleep_time)
            call_count = 0

        url = base_url + str(match_id)
        response = requests.get(url)
        call_count += 1
        last_request_time = now

        # Save metadata into json in metadata folder
        if response.status_code == 200:
            match_details = response.json()
            filename = os.path.join(output_dir, f"{match_id}.json")
            with open(filename, "w") as f:
                json.dump(match_details, f, indent=4)
            print(f"Metadata for match {match_id} downloaded and saved into {filename}.")

            # Update sqlite table
            cursor.execute("UPDATE matches SET meta_downloaded = 1 WHERE id = ?", (match_id,))
            conn.commit()
        else:
            print(f"Error while downloading metadata for match {match_id}: {response.status_code}")

    conn.close()

def main():
    db_path = os.path.join(os.path.dirname(__file__), "matches.db")
    fetch_and_save_match_details(db_path)

if __name__ == "__main__":
    main()
