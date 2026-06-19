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
