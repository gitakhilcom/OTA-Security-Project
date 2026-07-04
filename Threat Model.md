# Threat Model

**Project:** OTA Security Project using Digital Signatures

**Owner:** Member 3 – Digital Signature Developer

---

# Overview

This document identifies potential security threats to the OTA firmware update system and describes the mitigation strategies implemented in this project.

The goal is to ensure that firmware updates are authentic, untampered, and protected against unauthorized installation.

---

# 1. Private Key Exposure Vectors

## 1.1 Key Stored in Git Repository

**Threat**

A developer accidentally commits `private_key.pem` to the GitHub repository.

**Impact**

Critical

An attacker who obtains the private key can generate valid signatures for malicious firmware.

**Mitigation**

- Add `*.pem` to `.gitignore`
- Store the private key using GitHub Actions Secrets (`PRIVATE_KEY_B64`)
- Never commit private keys to version control
- Restrict repository access

---

## 1.2 Key Printed in Logs

**Threat**

Debug statements expose private key contents in terminal or CI logs.

**Impact**

Critical

Anyone with access to CI logs can recover the private key.

**Mitigation**

- Never print private key contents
- Log only metadata such as key size and algorithm
- Enable GitHub secret masking
- Disable verbose debugging in production

---

## 1.3 Environment Variable Leakage

**Threat**

Compromised CI runner exposes environment variables containing secrets.

**Impact**

Critical

Private key compromise allows attackers to sign malicious firmware.

**Mitigation**

- Store keys as encrypted GitHub Secrets
- Rotate keys periodically
- Limit repository permissions
- Use least-privilege access controls

---

# 2. Signature Bypass Vectors

## 2.1 Modified Firmware

**Threat**

An attacker modifies the firmware after it has been signed.

**Impact**

High

Tampered firmware may contain malicious code.

**Mitigation**

- Verify SHA-256 hash
- Validate RSA digital signature before installation
- Reject firmware if verification fails

---

## 2.2 Fake Signature

**Threat**

An attacker creates a fake signature without possessing the private key.

**Impact**

High

Could lead to unauthorized firmware installation.

**Mitigation**

- Verify signatures using the trusted public key
- Reject invalid signatures
- Use secure RSA cryptography

---

## 2.3 Public Key Replacement

**Threat**

An attacker replaces the trusted public key on the device.

**Impact**

Critical

The device could accept malicious firmware signed by an attacker.

**Mitigation**

- Protect the public key from modification
- Store the public key securely
- Verify device integrity before updates

---

# 3. Rollback Attack

## Threat

An attacker installs an older but validly signed firmware containing known vulnerabilities.

## Impact

High

Older firmware may reintroduce security flaws.

## Mitigation

- Compare firmware versions
- Reject outdated firmware
- Implement rollback protection using version validation

---

# 4. OTA Communication Threats

## Threat

Firmware download is intercepted or modified during transmission.

## Impact

High

Device may receive corrupted or malicious firmware.

## Mitigation

- Verify firmware signature after download
- Validate SHA-256 hash
- Use secure communication (HTTPS) in production

---

# 5. CI/CD Pipeline Risks

## Threat

Unauthorized modification of the build pipeline.

## Impact

High

Malicious firmware could be signed automatically.

## Mitigation

- Protect GitHub Actions workflows
- Require pull request reviews
- Restrict repository write access
- Enable branch protection rules

---

# Cryptographic Algorithm Rationale

This project uses RSA public-key cryptography together with the SHA-256 hashing algorithm.

### RSA

RSA provides secure digital signatures using a public/private key pair.

Benefits:

- Strong authentication
- Industry standard
- Widely supported
- Prevents unauthorized firmware signing

### SHA-256

SHA-256 generates a unique cryptographic hash for firmware.

Benefits:

- Detects firmware tampering
- Collision resistant
- Fast and secure

---

# Security Summary

This project protects against:

- Unauthorized firmware signing
- Firmware tampering
- Signature forgery
- Rollback attacks
- Private key leakage
- CI/CD compromise
- OTA communication attacks

---

# Conclusion

The OTA Security Project demonstrates a secure firmware update workflow using RSA digital signatures, SHA-256 hashing, firmware verification, rollback protection, and GitHub Actions automation. These controls help ensure that only authentic firmware is accepted and installed on simulated IoT devices.