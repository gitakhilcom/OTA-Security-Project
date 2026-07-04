import subprocess
import argparse
import sys


def verify_signature(file_path, signature_path, public_key_path):
    result = subprocess.run(
        [
            "openssl",
            "dgst",
            "-sha256",
            "-verify",
            public_key_path,
            "-signature",
            signature_path,
            file_path,
        ],
        capture_output=True,
        text=True,
    )


import os

def verify_signature(file, signature, public_key):
    # Check if all required files exist
    for f in [file, signature, public_key]:
        if not os.path.exists(f):
            print(f"❌ Error: {f} not found")
            return

    result = subprocess.run([
        "openssl", "dgst", "-sha256",
        "-verify", public_key,
        "-signature", signature,
        file
    ], capture_output=True, text=True)


    if result.returncode == 0:
        print("✅ Signature VALID")
        return True
    else:
        print("❌ Signature INVALID")

        print(result.stderr)
        return False




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify firmware signature")
    parser.add_argument("firmware", help="Firmware file")
    parser.add_argument("signature", help="Signature file")
    parser.add_argument("public_key", help="Public key")

    args = parser.parse_args()

    if not verify_signature(args.firmware, args.signature, args.public_key):
        sys.exit(1)