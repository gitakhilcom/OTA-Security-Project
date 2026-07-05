# Threat Model - OTA Security Project

## Overview
This document outlines the security threats identified and mitigated 
in the Secure OTA Firmware Update & Code Signing Infrastructure.

## Assets Being Protected
- Firmware binary (firmware.bin)
- Private signing key
- Edge device integrity
- OTA distribution pipeline

## Threat 1: Firmware Tampering
**Attack:** An attacker intercepts the firmware during distribution 
and modifies its contents.

**Mitigation:** SHA-256 hashing detects any modification to the 
firmware binary. The edge device calculates the hash and verifies 
it against the signed hash before installation.

## Threat 2: Signature Forgery
**Attack:** An attacker attempts to create a fake digital signature 
to pass verification on the edge device.

**Mitigation:** RSA-2048 with PSS padding is used for signing. 
Without the private key, it is computationally infeasible to forge 
a valid signature.

## Threat 3: Private Key Theft
**Attack:** An attacker gains access to the private key and uses it 
to sign malicious firmware.

**Mitigation:** The private key is never stored in the repository. 
It is injected at runtime via GitHub Secrets and never written to 
disk in plaintext.

## Threat 4: Rollback Attack
**Attack:** An attacker forces the device to install an older, 
vulnerable firmware version that has known exploits.

**Mitigation:** The anti-rollback system (anti_rollback.py) tracks 
the current installed version using timestamps and build numbers. 
Any firmware with an equal or older version is automatically rejected.

## Threat 5: Compromised CI/CD Pipeline
**Attack:** An attacker gains access to the GitHub Actions pipeline 
and injects malicious code into the signing process.

**Mitigation:** All pipeline steps are version-controlled and 
auditable. Secrets are never exposed in logs. Only release tags 
trigger the signing workflow, limiting the attack surface.

## Threat 6: Man-in-the-Middle Attack
**Attack:** An attacker intercepts the OTA update in transit and 
replaces it with malicious firmware.

**Mitigation:** Digital signature verification on the edge device 
ensures that even if the firmware is replaced in transit, it will 
fail signature verification and be rejected.

## Cryptographic Algorithms Used
- RSA-2048 for asymmetric key pair generation
- SHA-256 for firmware integrity hashing
- RSA-PSS padding for digital signature generation and verification

## Conclusion
The combination of cryptographic signing, hash verification, 
secure secret management, and anti-rollback protection provides 
a robust zero-trust firmware update system that defends against 
the most common OTA attack vectors.
