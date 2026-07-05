import hashlib
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class HashVerificationResult:
    firmware_path: str
    expected_hash: str
    computed_hash: str
    match: bool

    def __str__(self) -> str:
        status = "PASS ✓" if self.match else "FAIL ✗"
        return (
            f"[{status}] Firmware Integrity Check\n"
            f"  File    : {self.firmware_path}\n"
            f"  Expected: {self.expected_hash}\n"
            f"  Computed: {self.computed_hash}\n"
            f"  Result  : {'Hashes match – firmware is intact.' if self.match else 'Hash mismatch – firmware may be tampered!'}"
        )


def compute_sha256(firmware_path: str, chunk_size: int = 8192) -> str:
    path = Path(firmware_path)
    if not path.exists():
        raise FileNotFoundError(f"Firmware file not found: {firmware_path}")
    if not path.is_file():
        raise IOError(f"Path is not a regular file: {firmware_path}")

    hasher = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def load_expected_hash(hash_source: str) -> str:
    candidate = hash_source.strip()

    is_file = (
        candidate.endswith(".txt")
        or (os.sep in candidate and Path(candidate).exists())
    )

    if is_file:
        path = Path(candidate)
        if not path.exists():
            raise FileNotFoundError(f"Hash file not found: {candidate}")
        lines = path.read_text(encoding="utf-8").splitlines()
        non_blank = [ln.strip() for ln in lines if ln.strip()]
        if not non_blank:
            raise ValueError(f"Hash file is empty: {candidate}")
        candidate = non_blank[0].split()[0]

    if len(candidate) != 64 or not all(c in "0123456789abcdefABCDEF" for c in candidate):
        raise ValueError(
            f"Invalid SHA-256 hash (expected 64 hex chars): '{candidate}'"
        )
    return candidate.lower()


def verify_firmware(firmware_path: str, hash_source: str) -> HashVerificationResult:
    expected = load_expected_hash(hash_source)
    computed = compute_sha256(firmware_path)
    return HashVerificationResult(
        firmware_path=str(firmware_path),
        expected_hash=expected,
        computed_hash=computed,
        match=(expected == computed),
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Verify SHA-256 integrity of firmware.")
    parser.add_argument("firmware", nargs="?", default="firmware.bin")
    parser.add_argument("hash_source", nargs="?", default="firmware_hash.txt")
    args = parser.parse_args()
    result = verify_firmware(args.firmware, args.hash_source)
    print(result)
    raise SystemExit(0 if result.match else 1)
