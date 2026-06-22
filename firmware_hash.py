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

    def _str_(self):
        status = "PASS ✓" if self.match else "FAIL ✗"
        return (
            f"[{status}] Firmware Integrity Check\n"
            f"File      : {self.firmware_path}\n"
            f"Expected  : {self.expected_hash}\n"
            f"Computed  : {self.computed_hash}\n"
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
