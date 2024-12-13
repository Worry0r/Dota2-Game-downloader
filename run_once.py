import subprocess

def run_script(script_name):
    try:
        print(f"Starting {script_name}...")
        subprocess.run(["python", script_name], check=True)
        print(f"{script_name} finished.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error while starting {script_name}: {e}")
        exit(1)

# Run all the scripts in order
def main():
    run_script("game_id.py")
    
    run_script("game_metadata.py")
    
    run_script("game_replay.py")

if __name__ == "__main__":
    main()
