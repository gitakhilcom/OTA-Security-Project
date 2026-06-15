import argparse
import hashlib
from pathlib import Path

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


def verify_signature(public_key, firmware_path, signature_path):
    digest = compute_sha256(firmware_path)

    signature = Path(signature_path).read_bytes()

    try:
        public_key.verify(
            signature,
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print("Signature valid: True")

    except Exception:
        print("Signature valid: False")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify firmware signature"
    )

    parser.add_argument(
        "--public-key",
        required=True,
        help="Path to RSA public key"
    )

    parser.add_argument(
        "--firmware",
        required=True,
        help="Path to firmware file"
    )

    parser.add_argument(
        "--signature",
        required=True,
        help="Path to signature file"
    )

    args = parser.parse_args()

    public_key = load_public_key(args.public_key)

    verify_signature(
        public_key,
        args.firmware,
        args.signature
    )