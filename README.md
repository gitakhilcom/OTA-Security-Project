# OTA-Security-Project
# PKI & Key Generation – OTA Security Project

## Overview
This branch contains the Public Key Infrastructure (PKI) setup for the Secure OTA Firmware Update project. It handles RSA 2048-bit key pair generation and secure key storage practices.

## Role
Member 1 – PKI & Key Generation Lead

## Files
- `generate_keys.py` – Generates RSA 2048-bit key pair
- `public_key.pem` – Public key (safe to commit)
- `.gitignore` – Blocks private key from being committed

## How to Run
pip install cryptography
python generate_keys.py

## Security Notes
- Private key is generated locally only
- Never commit private_key.pem to GitHub
- Public key is used by the edge device to verify firmware signatures

## Week 1 Deliverables
- RSA 2048-bit key pair generation
- Secure key storage
- PKI documentation