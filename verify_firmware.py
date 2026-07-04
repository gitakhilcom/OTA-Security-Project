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
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def compute_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    return sha256.digest()


def load_public_key(key_path):
    with open(key_path, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def verify_signature(firmware_path, signature_path, public_key_path):
    try:
        digest = compute_sha256(firmware_path)

        print(f"[INFO] Firmware SHA-256: {digest.hex()}")

        signature = Path(signature_path).read_bytes()

        public_key = load_public_key(public_key_path)

        public_key.verify(
            signature,
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print("[SUCCESS] Signature verification PASSED.")
        print("[SUCCESS] Firmware integrity confirmed.")
        return True

    except InvalidSignature:
        print("[FAILED] Invalid signature.")
        return False

    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        return False

    except Exception as e:
        print(f"[ERROR] {e}")
        return False


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print(
            "Usage: python verify_firmware.py "
            "<firmware.bin> <firmware.sig> <public.pem>"
        )
        sys.exit(1)

    firmware_file = sys.argv[1]
    signature_file = sys.argv[2]
    public_key_file = sys.argv[3]

    if not Path(firmware_file).is_file():
        sys.exit(f"[-] Firmware not found: {firmware_file}")

    if not Path(signature_file).is_file():
        sys.exit(f"[-] Signature not found: {signature_file}")

    if not Path(public_key_file).is_file():
        sys.exit(f"[-] Public key not found: {public_key_file}")

    if verify_signature(
        firmware_file,
        signature_file,
        public_key_file
    ):
        print("\n[STATUS] Installation approved.")
        sys.exit(0)

    print("\n[STATUS] Installation blocked.")
    sys.exit(1)