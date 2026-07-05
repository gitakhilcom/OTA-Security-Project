# Secure OTA Firmware Update and Code Signing Infrastructure

## Project Overview

This project demonstrates a secure Over-the-Air (OTA) firmware update system for IoT devices using Digital Signatures. It ensures secure firmware delivery by signing firmware with a private RSA key and verifying it using a public key before installation.

The project simulates a complete OTA firmware update workflow, including firmware signing, secure download, signature verification, rollback attack prevention, and automated testing through GitHub Actions.

---

## Objectives

- Ensure firmware authenticity
- Prevent unauthorized firmware installation
- Verify firmware using public-key cryptography
- Protect against firmware tampering
- Prevent rollback attacks
- Automate verification using GitHub Actions CI/CD

---

## Features

- RSA key generation
- Digital firmware signing
- Firmware signature verification
- SHA-256 hashing for integrity checking
- OTA firmware download module
- Simulated IoT device
- Rollback attack protection
- GitHub Actions CI/CD automation
- Unit testing
- Project documentation

---

## Technologies Used

- Python 3
- RSA Cryptography
- SHA-256
- Git
- GitHub
- GitHub Actions
- Cryptography Library

---

## Team Members

| Member | Responsibility |
|---------|----------------|
| Member 1 | Firmware Development |
| Member 2 | Key Management |
| Member 3 | Update Server Development |
| Member 4 | Verification & GitHub Management |

---

# Repository Structure

```text
OTA-Security-Project/
│
├── .github/
│   └── workflows/
│
├── Signing/
│
├── Verification/
│
├── deployment/
│
├── docs/
│
├── downloads/
│
├── release/
│
├── tests/
│
├── firmware.bin
├── firmware.sig
├── private_key.pem
├── public_key.pem
│
├── generate_keys.py
├── sign_firmware.py
├── verify_firmware.py
├── download_firmware.py
├── rollback_guard.py
├── simulated_device.py
│
├── test_signer.py
├── test_rollback_attacks.py
│
├── requirements.txt
├── README.md
└── ThreatModel.md
```

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/your-username/OTA-Security-Project.git

cd OTA-Security-Project
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

## 1. Generate RSA Keys

```bash
python generate_keys.py
```

Creates:

- private_key.pem
- public_key.pem

---

## 2. Sign Firmware

```bash
python sign_firmware.py
```

Generates:

- firmware.sig

---

## 3. Verify Firmware

```bash
python verify_firmware.py
```

If the signature is valid, the firmware is accepted.

---

## 4. Download Firmware

```bash
python download_firmware.py
```

Or download from a custom URL:

```bash
python download_firmware.py --url <custom-url> --out custom_folder
```

---

## 5. Simulate IoT Device

```bash
python simulated_device.py
```

The simulated device:

- Downloads firmware
- Verifies digital signature
- Checks firmware version
- Blocks rollback attacks
- Installs only authentic firmware

---

## OTA Firmware Download Module 

### Purpose

Download firmware updates from a remote source before performing signature verification.

### Files

- `download_firmware.py` – Downloads firmware from a configurable URL.
- `downloads/` – Stores downloaded firmware files.

### Usage

Default download:

```bash
python download_firmware.py
```

Custom download:

```bash
python download_firmware.py --url <custom-url> --out custom_folder
```

### Configuration

Update the firmware download source by modifying:

```python
FIRMWARE_URL = "https://your-github-release-url/firmware.bin"
```

Set this URL to your GitHub Release asset.

---

# Rollback Protection

The project prevents rollback attacks by checking firmware version numbers before installation.

If an older firmware version is detected, installation is rejected.

---

# Running Tests

Run all tests:

```bash
python -m unittest
```

Or run individual tests:

```bash
python test_signer.py
```

```bash
python test_rollback_attacks.py
```

---

# GitHub Actions CI/CD

The project includes GitHub Actions for automated testing.

On every push or pull request, the workflow automatically:

- Installs dependencies
- Generates RSA keys
- Signs firmware
- Verifies firmware
- Runs unit tests

---

## Four-Week Engineering Progress

### Week 1: PKI Setup and Cryptographic Hashing

#### Objectives
- Establish Public Key Infrastructure (PKI)
- Generate RSA key pairs
- Create firmware binary
- Implement SHA-256 hashing

#### Completed Tasks
- Developed `generate_keys.py`
- Generated public and private RSA keys
- Created sample `firmware.bin`
- Implemented SHA-256 hashing for firmware integrity verification

#### Deliverables
- RSA Key Pair
- Firmware Binary
- Hash Generation System

---

### Week 2: CI/CD Automated Code Signing

#### Objectives
- Automate firmware signing
- Integrate signing process with GitHub Actions
- Generate digital signatures

#### Completed Tasks
- Developed `sign_firmware.py`
- Implemented RSA-based digital signature generation
- Created `firmware.sig`
- Configured GitHub Actions workflow
- Automated signing and validation process

#### Deliverables
- Signed Firmware Package
- CI/CD Pipeline
- Automated Build Workflow

---

### Week 3: Edge Device Verification Logic

#### Objectives
- Verify firmware authenticity on the device
- Validate firmware before installation
- Simulate IoT device behavior

#### Completed Tasks
- Developed `verify_firmware.py`
- Implemented signature verification using public key
- Developed `download_firmware.py`
- Created `simulated_device.py`
- Added logging and verification checks

#### Deliverables
- Firmware Verification Module
- Simulated IoT Device
- OTA Download Simulation

---

### Week 4: Version Control and Rollback Protection

#### Objectives
- Prevent installation of outdated firmware
- Implement rollback attack detection
- Perform testing and documentation

#### Completed Tasks
- Developed `rollback_guard.py`
- Implemented firmware version validation
- Added rollback attack test cases
- Created `test_rollback_attacks.py`
- Updated project documentation and threat model

#### Deliverables
- Rollback Protection System
- Security Testing Reports
- Final Documentation

---

## Project Outcome

Successfully developed a secure OTA firmware update system that:

- Generates and manages cryptographic keys
- Digitally signs firmware updates
- Verifies firmware authenticity before installation
- Simulates an IoT edge device workflow
- Prevents rollback attacks
- Automates processes through GitHub Actions CI/CD

The project demonstrates secure firmware delivery and verification techniques commonly used in modern IoT and embedded systems.

---


---

# License

This project is developed for educational and academic purposes.

Secure OTA Firmware Update and Code Signing Infrastructure Project
