import subprocess
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
    else:
        print("❌ Signature INVALID")

verify_signature("firmware.bin", "firmware.sig", "public_key.pem")
