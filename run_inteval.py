import time
import subprocess

# Runs run_once.py every 8 hours
while True:
    subprocess.run(["python", "run_once.py"])
    time.sleep(28800)