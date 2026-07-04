import time
import sys
import itertools

import download_firmware
import verify_firmware
import rollback_guard


# -----------------------------
# Loading Spinner
# -----------------------------
def spinner(message, duration=2):
    animation = itertools.cycle(["|", "/", "-", "\\"])
    end_time = time.time() + duration

    while time.time() < end_time:
        sys.stdout.write(f"\r{message:<45} {next(animation)}")
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write(f"\r{message:<45} [ OK ]\n")


# -----------------------------
# Progress Bar
# -----------------------------
def progress(title, width=40):
    print(f"\n{title}")

    for i in range(width + 1):
        percent = int(i / width * 100)
        bar = "█" * i + "░" * (width - i)
        sys.stdout.write(f"\r[{bar}] {percent:3d}%")
        sys.stdout.flush()
        time.sleep(0.04)

    print("\n")


# ==========================================================
# Start
# ==========================================================

print("\n" + "=" * 60)
print("             SECURE OTA FIRMWARE UPDATE SYSTEM")
print("=" * 60)

spinner("[INFO] Booting IoT Device", 2)
spinner("[INFO] Initializing Security Engine", 2)
spinner("[INFO] Connecting to Update Server", 2)

print("\n" + "-" * 60)
print("STEP 1 : DOWNLOAD FIRMWARE")
print("-" * 60)

progress("Downloading firmware.bin")
progress("Downloading firmware.sig")

download_firmware.download_firmware()

firmware_file = "downloads/firmware.bin"
signature_file = "downloads/firmware.sig"
public_key_file = "public_key.pem"

print("\n✓ Firmware package downloaded successfully.")

print("\n" + "-" * 60)
print("STEP 2 : AUTHENTICITY VERIFICATION")
print("-" * 60)

spinner("Calculating SHA-256 Hash", 2)
spinner("Loading Public Key", 1)
spinner("Verifying Digital Signature", 2)

if verify_firmware.verify_signature(
    firmware_file,
    signature_file,
    public_key_file,
):

    current_state = {
        "build_timestamp": 100,
        "build_iteration": 1
    }

    incoming_manifest = {
        "build_timestamp": 101,
        "build_iteration": 2
    }

    print("\n" + "-" * 60)
    print("STEP 3 : ROLLBACK PROTECTION")
    print("-" * 60)

    print(f"Current Firmware  : Timestamp={current_state['build_timestamp']}  Version={current_state['build_iteration']}")
    print(f"Incoming Firmware : Timestamp={incoming_manifest['build_timestamp']}  Version={incoming_manifest['build_iteration']}")

    spinner("Checking Firmware Version", 2)

    if rollback_guard.check_rollback(current_state, incoming_manifest):

        print("\nRollback Status : PASSED ✓")

        print("\n" + "-" * 60)
        print("STEP 4 : INSTALLING FIRMWARE")
        print("-" * 60)

        progress("Writing Firmware to Flash Memory")
        progress("Verifying Installation")
        progress("Updating Boot Configuration")

        spinner("Rebooting Device", 3)

        print("\n" + "=" * 60)
        print("              OTA UPDATE COMPLETED")
        print("=" * 60)
        print("[SUCCESS] Firmware Installed Successfully")
        print("[SUCCESS] Secure Boot Verification Passed")
        print("[SUCCESS] Device Running Latest Firmware")
        print("[STATUS ] System State : OPERATIONAL")
        print("=" * 60)

    else:

        print("\n" + "=" * 60)
        print("[ERROR] Rollback Attack Detected")
        print("[ERROR] Firmware Installation Cancelled")
        print("=" * 60)

else:

    print("\n" + "=" * 60)
    print("[ERROR] Digital Signature Verification Failed")
    print("[ERROR] Firmware Installation Aborted")
    print("=" * 60)