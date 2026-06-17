import os
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def load_private_key():
    """Load the private key from an environment variable (set via GitHub Secrets)."""
    private_key_pem = os.environ.get("PRIVATE_KEY")
    if not private_key_pem:
        raise ValueError("PRIVATE_KEY environment variable not set.")
    
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
    )
    return private_key

def sign_firmware(firmware_path, signature_path):
    """Calculate SHA-256 hash of firmware and sign it with the private key."""
    
    # Read firmware binary
    with open(firmware_path, "rb") as f:
        firmware_data = f.read()

    # Calculate SHA-256 hash
    firmware_hash = hashlib.sha256(firmware_data).digest()
    print(f"Firmware hash: {firmware_hash.hex()}")

    # Load private key and sign the hash
    private_key = load_private_key()
    signature = private_key.sign(
        firmware_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Save the signature
    with open(signature_path, "wb") as f:
        f.write(signature)

    print(f"Firmware signed successfully. Signature saved to {signature_path}")

if __name__ == "__main__":
    sign_firmware("firmware.bin", "firmware.sig")