import os
import urllib.request

FIRMWARE_URL = "https://github.com/gitakhilcom/OTA-Security-Project/releases/download/V1.1/firmware.bin"
SIGNATURE_URL = "https://github.com/gitakhilcom/OTA-Security-Project/releases/download/V1.1/firmware.sig"

DOWNLOAD_DIR = "downloads"


def download_file(url, filename):
    token = os.getenv("GITHUB_TOKEN")

    headers = {
        "User-Agent": "OTA-Updater"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        with open(filename, "wb") as f:
            f.write(response.read())

    print(f"✅ Download complete: {filename}")


def download_firmware():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    firmware_path = os.path.join(DOWNLOAD_DIR, "firmware.bin")
    signature_path = os.path.join(DOWNLOAD_DIR, "firmware.sig")

    try:
        download_file(FIRMWARE_URL, firmware_path)
        download_file(SIGNATURE_URL, signature_path)
    except Exception as e:
        print(f"❌ Download failed: {e}")


if __name__ == "__main__":
    download_firmware()