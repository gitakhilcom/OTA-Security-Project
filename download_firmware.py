import os
import urllib.request
import argparse

FIRMWARE_URL = "https://github.com/gitakhilcom/OTA-Security-Project/releases/download/V1.1/firmware.bin"
DOWNLOAD_DIR = "downloads"

def download_firmware(url=FIRMWARE_URL, dest_dir=DOWNLOAD_DIR):
    token = os.getenv("GITHUB_TOKEN")

    os.makedirs(dest_dir, exist_ok=True)
    filename = os.path.join(dest_dir, "firmware.bin")

    try:
        headers = {"User-Agent": "OTA-Updater"}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req) as response:
            with open(filename, "wb") as f:
                f.write(response.read())

        print(f"✅ Download complete: {filename}")

    except Exception as e:
        print(f"❌ Download failed: {e}")

if __name__ == "__main__":
    download_firmware()