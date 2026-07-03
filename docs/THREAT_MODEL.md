# Threat Model

## 1. Project Overview

This project secures firmware by using RSA digital signatures to ensure firmware authenticity and integrity before deployment.

## 2. Assets to Protect

- Private signing key
- Firmware binary
- Digital signature
- CI/CD pipeline
- Release artifacts

## 3. Threat Actors

- External attackers
- Malicious insiders
- Attackers targeting the CI/CD pipeline
- Unauthorized users attempting firmware modification

## 4. Attack Vectors

### 4.1 Compromised CI/CD Pipeline

A compromised CI/CD pipeline could allow attackers to inject malicious firmware during the build or deployment process.

Impact:
- Malicious firmware may be signed and distributed.
- Loss of firmware integrity.

Mitigation:
- Protect GitHub branches.
- Require pull request reviews.
- Restrict CI/CD access.
- Verify firmware signatures before deployment.

### 4.2 Private Key Theft

If the private signing key is stolen, attackers can create valid signatures for malicious firmware.

Impact:
- Unauthorized firmware appears legitimate.

Mitigation:
- Store private keys securely.
- Never commit private keys to the repository.
- Limit access to trusted users.
- Rotate keys if compromise is suspected.

### 4.3 Rollback Attacks
An attacker may replace the current firmware with an older but valid signed version containing known vulnerabilities.

Impact:
- Previously fixed security issues may return.

Mitigation:
- Check firmware version numbers.
- Reject firmware versions older than the installed version.


### 4.4 Signature Forgery

Attackers attempt to create fake signatures to bypass firmware verification.

Impact:
- Unauthorized firmware installation.

Mitigation:
- Use RSA digital signatures.
- Verify signatures using the public key.
- Reject any firmware with invalid signatures.

### 4.5 Firmware Tampering

Firmware may be modified after it has been signed.

Impact:
- Device compromise or unexpected behavior.

Mitigation:
- Verify the firmware signature before installation.
- Reject modified firmware immediately.

## 5. Security Controls

The project implements multiple security controls to protect firmware integrity and authenticity.

- RSA digital signatures for firmware authentication.
- Public key verification before firmware installation.
- Secure storage of signing keys.
- Automated signature verification during the build process.
- Logging of firmware verification attempts.
- Test cases covering valid and invalid firmware scenarios.
- GitHub branch protection and pull request reviews to reduce unauthorized changes.

## 6. Risk Summary

Although the implemented security measures significantly reduce the risk of firmware attacks, some residual risks remain.

- Physical access to the device may allow hardware-based attacks.
- Compromise of the private signing key would require immediate key rotation.
- New vulnerabilities may emerge in dependencies or cryptographic libraries.

Regular security reviews, software updates, and secure key management help minimize these risks.

## 7. Conclusion
This threat model identifies the major security threats affecting the OTA firmware update system, including compromised CI/CD pipelines, private key theft, rollback attacks, signature forgery, and firmware tampering. By implementing RSA digital signatures, firmware verification, secure key management, testing, and repository security practices, the project provides strong protection for firmware authenticity and integrity throughout the deployment process.

