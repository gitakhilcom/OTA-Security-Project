# Firmware Hash Generation Documentation

## Objective

Generate a SHA-256 hash for the firmware file to ensure integrity verification.

## Files

* firmware.bin
* firmware_hash.txt

## Steps Performed

1. Created the firmware file firmware.bin.
2. Generated the SHA-256 hash of firmware.bin using Git Bash.
3. Saved the generated hash in firmware_hash.txt.
4. Uploaded the files to the GitHub repository.

## Command Used

sha256sum firmware.bin

## Purpose

SHA-256 hashing helps verify that the firmware file has not been modified or tampered with.

## Result

The SHA-256 hash was successfully generated and stored for future verification.
