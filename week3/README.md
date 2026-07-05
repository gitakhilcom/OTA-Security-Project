# Week 3: OTA Firmware Download Module

## Purpose
Download firmware updates from remote source before verification.

## Files
- `download_firmware.py`: Downloads firmware.bin from configurable URL
- `downloads/`: Folder for downloaded firmware files

## Usage
python download_firmware.py
python download_firmware.py --url <custom-url> --out custom_folder

## Config
FIRMWARE_URL: Change this to point to your GitHub Release asset URL
...................................................................