import requests
import os
import shutil
import subprocess
import sys

# URL for the latest script
SCRIPT_URL = 'https://raw.githubusercontent.com/jmassanopoli/git-repo-testing/refs/heads/main/script.py?token=GHSAT0AAAAAACZWEKHCQH7UB6CX2LL3OMNYZZCMU4Q'
VERSION_URL = 'https://raw.githubusercontent.com/jmassanopoli/git-repo-testing/refs/heads/main/version.txt?token=GHSAT0AAAAAACZWEKHDKAIHND7AIA2DU4EYZZCMVNA'
CURRENT_VERSION = '0'  # Update this when you change script.py

def check_for_updates():
    response = requests.get(VERSION_URL)
    latest_version = response.text.strip()
    return latest_version != CURRENT_VERSION

def download_update():
    response = requests.get(SCRIPT_URL)
    with open('script_tmp.py', 'wb') as f:
        f.write(response.content)

def replace_script():
    if os.path.exists('script.py'):
        os.remove('script.py')  # Remove old script
    shutil.move('script_tmp.py', 'script.py')  # Move new script to original name

def run_script():
    subprocess.run([sys.executable, 'script.py'])

if __name__ == "__main__":
    if check_for_updates():
        print("Updating script...")
        download_update()
        replace_script()

    run_script()
