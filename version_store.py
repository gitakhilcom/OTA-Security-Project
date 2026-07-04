import json
from pathlib import Path

VERSION_FILE = "version.json"


def read_version():
    path = Path(VERSION_FILE)
    if not path.exists():
        raise FileNotFoundError(f"Version file not found: {VERSION_FILE}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_current_version():
    data = read_version()
    return data["current_version"]


def save_version(new_version, build, firmware_file, firmware_hash):
    data = {
        "current_version": new_version,
        "build": build,
        "firmware_file": firmware_file,
        "firmware_hash": firmware_hash
    }
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def is_newer_version(new_version):
    current = get_current_version()
    current_parts = list(map(int, current.split(".")))
    new_parts = list(map(int, new_version.split(".")))
    return new_parts > current_parts


if __name__ == "__main__":
    print(f"Current Version: {get_current_version()}")
    test_new = "1.1.0"
    if is_newer_version(test_new):
        print(f"Version {test_new} is newer - ALLOW")
    else:
        print(f"Version {test_new} is older - BLOCK")
