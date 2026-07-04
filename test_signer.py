import subprocess
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

SCRIPT = Path(__file__).parent / "sign_firmware.py"
KEY = Path(__file__).parent / "test_key.pem"
FW = Path(__file__).parent / "test_firmware.bin"
BAD_KEY = Path(__file__).parent / "bad_key.pem"

print("OTA Security Project")
def setup_module():
    # Generate a test RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    with open(KEY, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Create test firmware
    FW.write_bytes(b"test firmware data v1.0")

    # Create corrupted key file
    BAD_KEY.write_text("this is not a PEM key")


def teardown_module():
    for f in [KEY, FW, BAD_KEY]:
        if f.exists():
            f.unlink()

    sig_file = Path("dist/firmware.sig")
    if sig_file.exists():
        sig_file.unlink()


def test_missing_firmware():
    result = subprocess.run(
        ["python", str(SCRIPT), "--key", str(KEY), "--firmware", "missing.bin"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1
    assert "Firmware not found" in (result.stdout + result.stderr)


def test_corrupted_key():
    result = subprocess.run(
        ["python", str(SCRIPT), "--key", str(BAD_KEY), "--firmware", str(FW)],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1


def test_successful_sign():
    result = subprocess.run(
        ["python", str(SCRIPT), "--key", str(KEY), "--firmware", str(FW)],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert Path("dist/firmware.sig").exists()