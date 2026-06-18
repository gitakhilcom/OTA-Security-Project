<<<<<<< HEAD
# DIGITAL SIGNATUREls - Member 3

Signs firmware binaries using RSA-2048 PSS and SHA-256 for secure OTA updates.

## Features

* RSA-2048 digital signatures
* RSA-PSS padding
* SHA-256 hashing
* Input validation for key and firmware files
* Automated unit tests using pytest

## Prerequisites

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

Create a `requirements.txt` file with:

```text
cryptography==42.0.8
pytest==7.4.3
```

## Generate Test Keys

Generate an RSA private key:

```bash
created using generate_keys.py 
```

Create a sample firmware file:

```bash
echo "firmware v1.0 test data" > firmware.bin
```

## Sign Firmware

Run the signer:

```bash
python sign_firmware.py --key private_key.pem --firmware firmware.bin 
```

## Output

After successful signing, the signature file will be created:

```text
dist/
└── firmware.sig
```

## Run Tests
----------
Execute all unit tests:

```bash
pytest test_signer.py -v
```

Expected output:

```text
======================== 3 passed ========================
```

# Test verification
-----------------
 # #Run Test
```
python verify_firmware.py --public-key public_key.pem --firmware firmware.bin --signature dist/firmware.sig
```
=======

# OTA-Security-Project

## Week 2 Progress

### Verification Automation
- Added automated signature verification workflow.
- Verification runs after firmware signing.
- Prepared verification process for deployment testing.

### Current Status
Work in progress for Week 2 deployment and verification tasks.

## Deployment Workflow

1. Firmware is built.
2. Firmware is digitally signed.
3. Signature is automatically verified.
4. Signed firmware is uploaded to the distribution server.
5. Release testing is performed.

