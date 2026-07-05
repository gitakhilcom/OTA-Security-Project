# CI/CD Pipeline Documentation

## Overview
This document describes the automated firmware signing pipeline built using GitHub Actions for the OTA Security Project.

## Pipeline Architecture
When a release tag (e.g. v1.0) is pushed to the repository, the GitHub Actions workflow automatically triggers and signs the firmware binary using RSA-2048 cryptographic signing.

## Workflow File
Location: `.github/workflows/sign.yml`

## Pipeline Flow
1. Developer pushes a release tag (v*)
2. GitHub Actions workflow triggers automatically
3. Repository code is checked out
4. Python 3.11 environment is set up
5. Required dependencies are installed (cryptography library)
6. Private key is securely loaded from GitHub Secrets
7. Firmware binary is hashed using SHA-256
8. Hash is signed using RSA-PSS with the private key
9. Signature is saved as firmware.sig

## Security Practices
- Private key is never stored in the repository
- Key is injected at runtime via GitHub Secrets (PRIVATE_KEY)
- SHA-256 used for firmware integrity verification
- RSA-PSS used for digital signature generation

## Tools Used
- GitHub Actions
- Python 3.11
- cryptography library (RSA-2048, SHA-256, PSS padding)

## Week 2 Deliverables
- GitHub Actions workflow file (sign.yml)
- Workflow trigger on release tags
- Firmware signing script (signing/sign_firmware.py)
- CI/CD pipeline documentation
