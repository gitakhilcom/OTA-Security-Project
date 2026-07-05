# anti_rollback.py
# Anti-Rollback Version Control - OTA Security Project
# Member 1 - Week 4: Version Control & Anti-Rollback Lead

import os
import json
from datetime import datetime

VERSION_FILE = "current_version.json"

def get_current_version():
    """Load the currently installed firmware version from local storage."""
    if not os.path.exists(VERSION_FILE):
        return {"version": "0.0.0", "build": 0, "timestamp": ""}
    
    with open(VERSION_FILE, "r") as f:
        return json.load(f)

def save_current_version(version, build):
    """Save the newly installed firmware version to local storage."""
    version_data = {
        "version": version,
        "build": build,
        "timestamp": datetime.utcnow().isoformat()
    }
    with open(VERSION_FILE, "w") as f:
        json.dump(version_data, f, indent=4)
    
    print(f"[INFO] Version {version} (build {build}) saved to device.")

def parse_version(version_str):
    """Convert version string like '1.2.3' into a tuple for comparison."""
    return tuple(int(x) for x in version_str.split("."))

def check_rollback(new_version, new_build):
    """Check if the incoming firmware is newer than the installed version."""
    current = get_current_version()
    current_version = current["version"]
    current_build = current["build"]

    print(f"[INFO] Current version: {current_version} (build {current_build})")
    print(f"[INFO] Incoming version: {new_version} (build {new_build})")

    if parse_version(new_version) > parse_version(current_version):
        print("[SUCCESS] Version check passed. Firmware is newer.")
        return True
    elif parse_version(new_version) == parse_version(current_version):
        if new_build > current_build:
            print("[SUCCESS] Same version but newer build. Proceeding.")
            return True
        else:
            print("[CRITICAL] Rollback attack detected! Same or older build rejected.")
            return False
    else:
        print("[CRITICAL] Rollback attack detected! Older version rejected.")
        return False

if __name__ == "__main__":
    incoming_version = "1.0.1"
    incoming_build = 2

    if check_rollback(incoming_version, incoming_build):
        save_current_version(incoming_version, incoming_build)
        print("[INFO] Firmware version updated successfully.")
    else:
        print("[INFO] Installation blocked due to rollback protection.")
