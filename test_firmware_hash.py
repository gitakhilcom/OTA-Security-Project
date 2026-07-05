import hashlib
import os
from pathlib import Path
import unittest

from firmware_hash import compute_sha256, load_expected_hash, verify_firmware


KNOWN_CONTENT = b"Device: Secure OTA Tracker\nFirmware Version: 1.0.0\nStatus: Base Payload\n"
KNOWN_HASH = hashlib.sha256(KNOWN_CONTENT).hexdigest()


def write_temp_file(content, suffix=".bin"):
    path = Path("temp_test_file" + suffix)
    with open(path, "wb") as f:
        f.write(content if isinstance(content, bytes) else content.encode())
    return path


class TestFirmwareHash(unittest.TestCase):

    def test_correct_hash_computation(self):
        fw = write_temp_file(KNOWN_CONTENT)
        self.assertEqual(compute_sha256(fw), KNOWN_HASH)
        os.remove(fw)

    def test_clean_firmware_passes_verification(self):
        fw = write_temp_file(KNOWN_CONTENT)
        result = verify_firmware(fw, KNOWN_HASH)
        self.assertTrue(result.match)
        os.remove(fw)

    def test_tampered_firmware_fails_verification(self):
        tampered = b"Device: HACKED Tracker\nFirmware Version: 9.9.9\n"
        fw = write_temp_file(tampered)
        result = verify_firmware(fw, KNOWN_HASH)
        self.assertFalse(result.match)
        os.remove(fw)

    def test_missing_firmware_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            compute_sha256("no_such_file.bin")

    def test_wrong_expected_hash_fails(self):
        fw = write_temp_file(KNOWN_CONTENT)
        wrong_hash = "a" * 64
        result = verify_firmware(fw, wrong_hash)
        self.assertFalse(result.match)
        os.remove(fw)


if __name__ == "__main__":
    unittest.main()
