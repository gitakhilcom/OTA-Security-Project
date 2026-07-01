import os
import json
from datetime import datetime

VERSION_FILE = "current_version.json"

def get_current_version():
    """Load the currently installed firmware version from local storage."""
    if not os.path.exists(VERSION_FILE):
        # No version installed yet, default to zero
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
