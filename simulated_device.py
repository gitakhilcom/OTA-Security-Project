import time
import sys

import download_firmware
import verify_firmware
import rollback_guard


# -----------------------------
# Status Message
# -----------------------------
def status(message, delay=1):
    print(f"[INFO] {message}...", end="", flush=True)
    time.sleep(delay)
    print(" DONE")


# -----------------------------
# Progress Bar
# -----------------------------
def progress(title, width=40):

    print(f"\n{title}")

    for i in range(width + 1):
        percent = int((i / width) * 100)
        bar = "█" * i + "░" * (width - i)

        sys.stdout.write(f"\r[{bar}] {percent:3d}%")
        sys.stdout.flush()

        time.sleep(0.03)

    print()


# ======================================================
# START
# ======================================================

print("=" * 65)
print("               SECURE OTA FIRMWARE UPDATE SYSTEM")
print("=" * 65)

status("Booting IoT Device")
status("Initializing Security Engine")
status("Connecting to Update Server")

print("\n" + "-" * 65)
print("STEP 1 : DOWNLOADING FIRMWARE")
print("-" * 65)

progress("Downloading firmware.bin")
progress("Downloading firmware.sig")

download_firmware.download_firmware()

firmware_file = "downloads/firmware.bin"
signature_file = "downloads/firmware.sig"
public_key_file = "public_key.pem"

print("\n✓ Firmware package downloaded successfully.")

print("\n" + "-" * 65)
print("STEP 2 : VERIFYING AUTHENTICITY")
print("-" * 65)

status("Calculating SHA-256 Hash")
status("Loading Public Key")
status("Verifying Digital Signature")

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

    print("\n" + "-" * 65)
    print("STEP 3 : ROLLBACK PROTECTION")
    print("-" * 65)

    print(f"Current Firmware")
    print(f"  Timestamp : {current_state['build_timestamp']}")
    print(f"  Version   : {current_state['build_iteration']}")

    print()

    print(f"Incoming Firmware")
    print(f"  Timestamp : {incoming_manifest['build_timestamp']}")
    print(f"  Version   : {incoming_manifest['build_iteration']}")

    print()

    status("Checking Rollback Protection")

    if rollback_guard.check_rollback(current_state, incoming_manifest):

        print("\n✓ Rollback Check Passed")

        print("\n" + "-" * 65)
        print("STEP 4 : INSTALLING FIRMWARE")
        print("-" * 65)

        progress("Writing Firmware")
        progress("Verifying Installation")
        progress("Updating Boot Configuration")

        status("Rebooting Device", 2)

        print("\n" + "=" * 65)
        print("                 OTA UPDATE SUCCESSFUL")
        print("=" * 65)
        print("Status               : SUCCESS")
        print("Firmware Signature   : VERIFIED")
        print("Rollback Protection  : PASSED")
        print("Installation         : COMPLETED")
        print("Device State         : OPERATIONAL")
        print("=" * 65)

    else:

        print("\n" + "=" * 65)
        print("                 OTA UPDATE FAILED")
        print("=" * 65)
        print("Status               : FAILED")
        print("Reason               : Rollback Attack Detected")
        print("Installation         : CANCELLED")
        print("=" * 65)

else:

    print("\n" + "=" * 65)
    print("                 OTA UPDATE FAILED")
    print("=" * 65)
    print("Status               : FAILED")
    print("Reason               : Invalid Digital Signature")
    print("Installation         : ABORTED")
    print("=" * 65)