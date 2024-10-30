import requests
import os
import shutil
import subprocess
import sys

# URL for the latest script
SCRIPT_URL = 'https://raw.githubusercontent.com/jmassanopoli/git-repo-testing/refs/heads/main/script.py?token=GHSAT0AAAAAACZWEKHDHDPSD64ER4PLFA32ZZCN22Q'
VERSION_URL = 'https://raw.githubusercontent.com/jmassanopoli/git-repo-testing/refs/heads/main/version.txt?token=GHSAT0AAAAAACZWEKHC3ZPAGHUJU7AC4WU6ZZCN3NQ'

def get_latest_version():
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text.strip()
    except Exception as e:
        print(f"Error fetching latest version: {e}")
        sys.exit(1)

def download_update():
    try:
        response = requests.get(SCRIPT_URL)
        response.raise_for_status()  # Raise an error for bad responses
        with open('script_tmp.py', 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Error downloading the update: {e}")
        sys.exit(1)

def replace_script():
    try:
        # Remove the old script if it exists
        if os.path.exists('script.py'):
            os.remove('script.py')
        # Rename the temporary script to the main script name
        os.rename('script_tmp.py', 'script.py')
    except Exception as e:
        print(f"Error replacing the script: {e}")
        sys.exit(1)

def run_script():
    try:
        print("Running the script...")
        result = subprocess.run([sys.executable, 'script.py'], check=True)
        print("Script finished with return code:", result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"Script execution failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error running the script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        current_version = ''
        if os.path.exists('version.txt'):
            with open('version.txt', 'r') as version_file:
                current_version = version_file.read().strip()

        latest_version = get_latest_version()

        if latest_version != current_version:
            print("Updating script...")
            download_update()
            replace_script()

            # Optionally write the new version to version.txt
            with open('version.txt', 'w') as version_file:
                version_file.write(latest_version)

        run_script()

    except Exception as e:
        print(f"Unhandled exception: {e}")
        sys.exit(1)