import argparse
import sys
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def validate_inputs(key_path, fw_path):
    """Check that key and firmware files exist before we do anything."""
    if not Path(key_path).is_file():
        sys.exit(f"[-] Key not found: {key_path}")
    if not Path(fw_path).is_file():
        sys.exit(f"[-] Firmware not found: {fw_path}")

def load_private_key(key_path):
    """Load RSA private key from PEM file. No password support for CI."""
    try:
        with open(key_path, "rb") as f:
            key_data = f.read()
        return serialization.load_pem_private_key(key_data, password=None)
    except Exception as e:
        sys.exit(f"[-] Failed to load private key: {e}")

def hash_file(file_path):
    """SHA-256 hash of file using 8KB chunks. Never loads full file into RAM."""
    sha256 = hashes.Hash(hashes.SHA256())
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):  # 8KB chunks = audit requirement
                sha256.update(chunk)
        return sha256.finalize()
    except IOError as e:
        sys.exit(f"[-] Failed to read firmware: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sign firmware with RSA-PSS")
    parser.add_argument("--key", required=True, help="Path to private_key.pem")
    parser.add_argument("--firmware", required=True, help="Path to firmware.bin")
    parser.add_argument("--out", default="dist", help="Output directory")
    args = parser.parse_args()
    
    validate_inputs(args.key, args.firmware)
    Path(args.out).mkdir(exist_ok=True)
    print("[+] OTA Security Project")
    print(f"[+] Environment validated.")
    print(f"[+] Output directory ready: {args.out}")
    
    print("[+] Loading private key...")
    private_key = load_private_key(args.key)
    print(f"[+] Key loaded: {private_key.key_size} bit RSA")
    
    print("[+] Hashing firmware...")
    fw_digest = hash_file(args.firmware)
    print(f"[+] SHA-256: {fw_digest.hex()}")
    
    print("[+] Ready to sign.")
