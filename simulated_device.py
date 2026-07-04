import time
import sys
import download_firmware
import verify_firmware
import rollback_guard


def spinner(message, seconds=2):
    """Loading spinner"""
    symbols = ["|", "/", "-", "\\"]
    end_time = time.time() + seconds

    while time.time() < end_time:
        for s in symbols:
            sys.stdout.write(f"\r{message} {s}")
            sys.stdout.flush()
            time.sleep(0.12)

    sys.stdout.write(f"\r{message} ✓\n")


def progress(message, total=30):
    """Progress bar"""
    print(message)
    for i in range(total + 1):
        percent = int((i / total) * 100)
        bar = "█" * i + "-" * (total - i)
        sys.stdout.write(f"\r[{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(0.08)
    print("\n")


print("=" * 55)
print("          SECURE OTA FIRMWARE UPDATE")
print("=" * 55)

spinner("Powering On IoT Device", 2)
spinner("Initializing Security Modules", 2)
spinner("Connecting to Update Server", 2)

print("\n[1/4] Downloading Firmware Files")
progress("Downloading firmware.bin")
progress("Downloading firmware.sig")

download_firmware.download_firmware()

firmware_file = "downloads/firmware.bin"
signature_file = "downloads/firmware.sig"
public_key_file = "public_key.pem"

print("[2/4] Security Verification")
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

    print("\n[3/4] Rollback Protection")
    spinner("Checking Firmware Version", 2)

    if rollback_guard.check_rollback(current_state, incoming_manifest):

        print("[4/4] Installing Update")
        progress("Writing Firmware")
        progress("Updating Bootloader")
        progress("Finalizing Installation")

        spinner("Rebooting Device", 3)

        print("=" * 55)
        print("✅ Firmware Installed Successfully")
        print("✅ Secure Boot Verified")
        print("🟢 Device Running Latest Firmware")
        print("=" * 55)

    else:
        print("\n❌ Rollback Attack Detected!")
        print("🚫 Installation Cancelled.")

else:
    print("\n❌ Invalid Digital Signature!")
    print("🚫 Firmware Installation Aborted.")