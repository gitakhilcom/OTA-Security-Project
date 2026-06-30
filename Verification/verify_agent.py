# verify_agent.py
# Edge Verification Agent - OTA Security Project
# Member 1 - Week 3: Edge Verification Core Developer

import os
import sys
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def load_public_key(public_key_path):
    """Load the public key from a PEM file."""
    if not os.path.exists(public_key_path):
        print(f"[ERROR] Public key not found: {public_key_path}")
        sys.exit(1)
    
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    
    print(f"[INFO] Public key loaded from {public_key_path}")
    return public_key

def load_files(firmware_path, signature_path):
    """Load firmware binary and signature file."""
    if not os.path.exists(firmware_path):
        print(f"[ERROR] Firmware file not found: {firmware_path}")
        sys.exit(1)
    
    if not os.path.exists(signature_path):
        print(f"[ERROR] Signature file not found: {signature_path}")
        sys.exit(1)

    with open(firmware_path, "rb") as f:
        firmware_data = f.read()

    with open(signature_path, "rb") as f:
        signature = f.read()

    print(f"[INFO] Firmware and signature loaded successfully")
    return firmware_data, signature

def verify_signature(firmware_data, signature, public_key):
    """Verify the RSA signature of the firmware."""
    try:
        firmware_hash = hashlib.sha256(firmware_data).digest()
        public_key.verify(
            signature,
            firmware_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("[SUCCESS] Signature verified. Firmware is authentic.")
        return True
    except Exception as e:
        print(f"[CRITICAL] Signature verification FAILED: {e}")
        print("[ALERT] Firmware rejected. Possible tampering detected.")
        return False

if __name__ == "__main__":
    firmware_path = "firmware.bin"
    signature_path = "firmware.sig"
    public_key_path = "public_key.pem"

    public_key = load_public_key(public_key_path)
    firmware_data, signature = load_files(firmware_path, signature_path)
    
    result = verify_signature(firmware_data, signature, public_key)
    
    if result:
        print("[INFO] Initiating mock firmware installation...")
        print("[INFO] Mock reboot complete. Device updated successfully.")
    else:
        print("[INFO] Installation blocked. Security alert logged.")
