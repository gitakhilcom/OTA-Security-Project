# Verification/verify_signature.py
import subprocess

def verify_signature(file, signature, public_key):
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
        exit(1)

verify_signature("firmware.bin", "firmware.sig", "public_key.pem")
