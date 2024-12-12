import requests
import sqlite3
import os
import bz2
import json
from concurrent.futures import ThreadPoolExecutor

#Download and decompress replay files, then update database.
def download_and_decompress_replay(replay_url, replay_path, match_id, db_path):
    try:
        # Download and save file
        response = requests.get(replay_url, stream=True, timeout=10)
        response.raise_for_status()

        with bz2.BZ2File(response.raw) as compressed_file:
            with open(replay_path, "wb") as rf:
                rf.write(compressed_file.read())
        print(f"Saved replay to {replay_path}")

        # Update database that file was downloaded
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE matches SET downloaded = 1 WHERE id = ?", (match_id,))
        conn.commit()
        conn.close()
        print(f"Updated 'downloaded' flag for match {match_id} in database.")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {replay_url}: {e}")

# Download replay files for matches with metadata downloaded and update database.
def download_replays(db_path, match_details_dir="metadata", replay_dir="replays", max_workers=5):
    
    os.makedirs(replay_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Choose matches with metadata downloaded and replays not yet downloaded
    cursor.execute("SELECT id FROM matches WHERE meta_downloaded = 1 AND downloaded = 0")
    matches = cursor.fetchall()

    if not matches:
        print("No matches to download replays for.")
        conn.close()
        return
    
    print(f"Found {len(matches)} matches to download replays for.")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for match_id, in matches:
            # Path to the specified metadata file
            match_details_path = os.path.join(match_details_dir, f"{match_id}.json")
            
            if os.path.exists(match_details_path):
                with open(match_details_path, "r") as f:
                    match_details = json.load(f)
                
                # Get replay_url from metadata
                if "replay_url" in match_details and match_details["replay_url"]:
                    replay_url = match_details["replay_url"]
                    replay_filename = f"{match_id}.dem"
                    replay_path = os.path.join(replay_dir, replay_filename)

                    # Download file if not downloaded yet
                    if not os.path.exists(replay_path):
                        executor.submit(download_and_decompress_replay, replay_url, replay_path, match_id, db_path)
                else:
                    print(f"No replay URL found for match {match_id}. Skipping.")
            else:
                print(f"Match details JSON for match {match_id} not found. Skipping.")

    conn.close()

def main():
    db_path = os.path.join(os.path.dirname(__file__), "matches.db")
    replay_dir = os.path.join(os.path.dirname(__file__), "replays")
    download_replays(db_path, replay_dir=replay_dir)

if __name__ == "__main__":
    main()
