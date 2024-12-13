Dota2 Game downloader
API for checking and updating latest available Dota2 games and automatically save them efficiently.

Setup
Code created on Python 3.12.5

python run_once.py
├── runs the code once, closes itself

python run_interval.py
├── runs the code endlessly in given intervals (Default - 8hours)
├── CTRL + C to stop execution


Structure
├── metadata/               # Folder where metadata are saved
├── replays/                # Folder where replays are saved
├── db_check.py             # Code to check sqlite database
├── game_id.py              # Code to get list of newest pro games
├── game_metadata.py        # Code to download metadata for replay and patch info
├── game_replay.py          # Code to download and save compressed replay files
├── run_interval.py         # Python script to execute program in given intervals (8 hours by default)
├── run_unce.py             # Python script to execute program once
├── matches.db              # Sqlite database of available Dota2 pro matches
├── .gitignore              # List of items not to be pushed
└── README.md               # Project documentation and usage guide