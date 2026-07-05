import hashlib
import os
import sys
from typing import Tuple
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.backends import default_backend
import argparse
from pathlib import Path


def load_private_key(key_path: str) -> RSAPrivateKey:
    """Load RSA private key from PEM file. Raises ValueError on failure."""
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Key not found: {key_path}")

    try:
        with open(key_path, "rb") as f:
            return serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
    except ValueError:
        raise ValueError(f"Key format error: {key_path} is not a valid PEM key")


def compute_sha256(file_path: str) -> Tuple[bytes, str]:
    """Compute SHA-256 digest of firmware file. Returns (digest_bytes, hex_string)."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Firmware not found: {file_path}")

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    return sha256.digest(), sha256.hexdigest()


def sign_digest(private_key: RSAPrivateKey, digest: bytes) -> bytes:
    """Sign SHA-256 digest using RSA-PSS + SHA-256. Returns signature bytes."""
    return private_key.sign(
        digest,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Sign firmware using RSA-PSS")
    parser.add_argument("--key", required=True, help="Path to private key PEM")
    parser.add_argument("--firmware", required=True, help="Path to firmware binary")
    parser.add_argument("--out", default="dist", help="Output directory")
    args = parser.parse_args()

    try:
        print(f"Loading key: {args.key}")
        private_key = load_private_key(args.key)

        print(f"Computing SHA-256: {args.firmware}")
        digest, digest_hex = compute_sha256(args.firmware)
        print(f"SHA-256: {digest_hex}")

        print("Signing digest with RSA-PSS...")
        signature = sign_digest(private_key, digest)

        out_dir = Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)

        sig_path = out_dir / "firmware.sig"

        with open(sig_path, "wb") as f:
            f.write(signature)

        print(f"Signing complete. Signature saved to {sig_path}")
        print(f"Signature size: {len(signature)} bytes")
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()