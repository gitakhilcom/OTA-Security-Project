import argparse
import sys
import os
from pathlib import Path

def validate_inputs(key_path, fw_path):
    """Check that key and firmware files exist before we do anything."""
    if not Path(key_path).is_file():
        sys.exit(f"[-] Key not found: {key_path}")
    if not Path(fw_path).is_file():
        sys.exit(f"[-] Firmware not found: {fw_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sign firmware with RSA-PSS")
    parser.add_argument("--key", required=True, help="Path to private_key.pem")
    parser.add_argument("--firmware", required=True, help="Path to firmware.bin")
    parser.add_argument("--out", default="dist", help="Output directory")
    args = parser.parse_args()
    
    validate_inputs(args.key, args.firmware)
    Path(args.out).mkdir(exist_ok=True)
    print(f"[+] Environment validated.")
    print(f"[+] Output directory ready: {args.out}")
    print("[+] Ready to sign.")

