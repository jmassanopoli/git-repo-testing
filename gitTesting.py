import requests
import os
import shutil
import subprocess
import sys

# URL for the latest script
SCRIPT_URL = 'https://raw.githubusercontent.com/jmassanopoli/git-repo-testing/refs/heads/main/script.py'
VERSION_URL = 'https://raw.githubusercontent.com/jmassanopoli/git-repo-testing/refs/heads/main/version.txt'

def get_latest_version():
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching latest version: {e}")
        sys.exit(1)

def download_update():
    try:
        response = requests.get(SCRIPT_URL)
        response.raise_for_status()
        with open('script_tmp.py', 'wb') as f:
            f.write(response.content)
    except requests.RequestException as e:
        print(f"Error downloading update: {e}")
        sys.exit(1)

def replace_script():
    try:
        if os.path.exists('script.py'):
            os.remove('script.py')
        os.rename('script_tmp.py', 'script.py')
    except Exception as e:
        print(f"Error replacing script: {e}")
        sys.exit(1)

def get_script_path():
    if getattr(sys, 'frozen', False):
        # If the application is frozen (running as an exe)
        return os.path.join(sys._MEIPASS, 'script.py')
    else:
        # If running as a script
        return os.path.join(os.path.dirname(__file__), 'script.py')

def run_script():
    try:
        script_path = get_script_path()
        print("Running the script at:", script_path)
        result = subprocess.run(["python", script_path], check=True)
        print("Script finished with return code:", result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"Script execution failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("The script file was not found. Please ensure it exists.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running the script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    current_version = ''
    if os.path.exists('version.txt'):
        print("version.txt is there")
        with open('version.txt', 'r') as version_file:
            current_version = version_file.read().strip()
            print(f"version is {current_version}") 

    latest_version = get_latest_version()
    print(f"lastest version is {latest_version}") 
    if latest_version != current_version:
        print("Updating script...")
        download_update()
        replace_script()

        with open('version.txt', 'w') as version_file:
            version_file.write(latest_version)

    run_script()