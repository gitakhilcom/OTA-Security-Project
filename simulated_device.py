import download_firmware
import verify_firmware
import rollback_guard

print("===== IoT Device Started =====")

# Download firmware and signature
download_firmware.download_firmware()

firmware_file = "downloads/firmware.bin"
signature_file = "downloads/firmware.sig"
public_key_file = "public_key.pem"

if verify_firmware.verify_signature(
    firmware_file,
    signature_file,
    public_key_file,
):
    print("✅ Signature Verified")

    current_state = {
        "build_timestamp": 100,
        "build_iteration": 1
    }

    incoming_manifest = {
        "build_timestamp": 101,
        "build_iteration": 2
    }

    if rollback_guard.check_rollback(current_state, incoming_manifest):
        print("✅ Firmware Installed Successfully")
    else:
        print("❌ Rollback Attack Detected!")

else:
    print("❌ Invalid Signature. Installation Cancelled.")