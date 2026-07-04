# OTA-Security-Project

## Overview
This branch documents the step-by-step progress, implementation details, and security configurations handled by Member 2 throughout the OTA Security Project.

---

## WEEK 1: Firmware Creation & Cryptographic Hashing

### Role
Member 2 – Firmware Hashing Lead

### Files Created
* firmware.bin – Dummy firmware file representing the system binary.
* firmware_hash.txt – File containing the secure SHA-256 hash value of the firmware.
* hash_documentation.md – Detailed documentation outlining the cryptographic hash generation process.

### How to Run
To calculate the SHA-256 hash using Git Bash:
```bash
sha256sum firmware.bin > firmware_hash.txt

### Week 1 Deliverables
* Successfully generated the dummy firmware binary file.
* Calculated and logged the cryptographic SHA-256 hash.
* Authored and committed the official hash generation documentation (hash_documentation.md).

---

## WEEK 2: Secrets & Key Management

### Role
Member 2 – Secrets & Key Management Lead

### Security Notes
* Never hardcode private keys or store them in plaintext within repository branches.
* Sensitive cryptographic credentials must be managed securely using GitHub Secrets.
* Configured workflow runtime to inject repository secrets into transient environments safely.

### Week 2 Deliverables
* Configured GitHub Secrets securely with the production private key.
* Formulated and committed comprehensive security implementation documentation.
* Audited team CI/CD pipelines to ensure safe environment protection rules.

---

## WEEK 3: Firmware Integrity & Hashing

### Role
Member 2 – Firmware Integrity & Hashing Lead

### Files Created
* `firmware_hash.py` – SHA-256 hashing module that reads firmware.bin, computes its hash, compares it against the expected hash value, and catches tampering before signature verification runs.
* `test_firmware_hash.py` – Unit tests to confirm tampered firmware gets detected and rejected.
* `.github/workflows/test.yml` – GitHub Actions workflow for automated firmware integrity unit testing.

### How to Run
To verify firmware integrity:
```bash
python firmware_hash.py firmware.bin firmware_hash.txt

To run unit tests:
```bash
python -m unittest test_firmware_hash -v

### Security Notes
* SHA-256 hash verification runs before signature verification as the first line of defence.
* Any single byte change in firmware.bin will produce a completely different hash and get rejected immediately.
* Unit tests simulate real tamper attacks including byte flipping, appending, prepending, and full payload replacement.

### Week 3 Deliverables
* Successfully implemented SHA-256 firmware integrity verification module.
* Built tamper detection logic that catches any modification to firmware binary.
* Authored unit tests confirming tampered firmware is correctly blocked.
* added a GitHub Actions Workflow to automatically run firmware integrity unit tests.

---

## WEEK 4: Build Metadata & Version Storage

### Role
Member 2 – Build Metadata & Version Storage Lead

### Files Created
* `version.json` – Stores the current firmware version, build number, firmware file, and SHA-256 hash.
* `version_store.py` – Reads, updates, and compares firmware versions to help prevent rollback attacks.
* `.github/workflows/version_check.yml` – GitHub Actions workflow that automatically runs version checks on every push to the `Member-2` branch.

### How to Run
To check the current firmware version:
```bash
python version_store.py

### Security Notes
* Rejects firmware versions older than the currently installed version.
* Prevents rollback attacks by comparing firmware versions.
* Stores firmware metadata for version tracking and validation.

### Week 4 Deliverables
* Created firmware version metadata storage.
* Implemented firmware version management module.
* Added version comparison for rollback protection.
* Configured GitHub Actions for automated version checks.
