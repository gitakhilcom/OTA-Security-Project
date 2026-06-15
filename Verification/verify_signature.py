"""
Edge Device Verification Agent - Signature Verification Script
Part of: OTA Firmware Update Security Pipeline
Member 4 - Deployment & Verification

This script simulates the edge device's verification process:
1. Calculates SHA-256 hash of the firmware binary
2. Verifies the digital signature using the stored public key
3. Returns PASS/FAIL based on integrity and authenticity checks

NOTE: This script currently uses RSA-PSS padding for signature
verification. Padding scheme to be confirmed with Member 1's
signing implementation (Week 1 signing script) — update the
padding.PSS(...) block below to padding.PKCS1v15() if the
signing pipeline uses PKCS#1 v1.5 instead.
"""

import sys
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature


def calculate_sha256(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def load_public_key(public_key_path):
    """Load an RSA public key from a PEM file."""
    with open(public_key_path, "rb") as key_file:
        public_key = load_pem_public_key(key_file.read())
    return public_key


def verify_signature(firmware_path, signature_path, public_key_path):
    """
    Verify the digital signature of the firmware binary.
    Returns True if verification passes, False otherwise.
    """
    try:
        firmware_hash = calculate_sha256(firmware_path)
        print(f"[INFO] SHA-256 hash of firmware: {firmware_hash}")

        public_key = load_public_key(public_key_path)
        print(f"[INFO] Public key loaded from: {public_key_path}")

        with open(signature_path, "rb") as sig_file:
            signature = sig_file.read()

        with open(firmware_path, "rb") as fw_file:
            firmware_data = fw_file.read()

        # PADDING SCHEME: RSA-PSS (to be confirmed against signing script)
        public_key.verify(
            signature,
            firmware_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print("[SUCCESS] Signature verification PASSED.")
        print("[SUCCESS] Firmware integrity and authenticity confirmed.")
        return True

    except InvalidSignature:
        print("[CRITICAL] Signature verification FAILED.")
        print("[CRITICAL] Firmware may be tampered with or from an untrusted source.")
        print("[ALERT] Dropping payload. Installation aborted.")
        return False

    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        return False

    except Exception as e:
        print(f"[ERROR] Unexpected error during verification: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python verify_signature.py <firmware.bin> <firmware.sig> <public_key.pem>")
        sys.exit(1)

    firmware_file = sys.argv[1]
    signature_file = sys.argv[2]
    public_key_file = sys.argv[3]

    result = verify_signature(firmware_file, signature_file, public_key_file)

    if result:
        print("\n[STATUS] Edge agent proceeding with mock reboot and installation...")
        sys.exit(0)
    else:
        print("\n[STATUS] Edge agent halted. Security alert logged.")
        sys.exit(1)
