# OTA-Security-Project

## Deployment Pipeline

### Overview
This project uses an automated OTA (Over-The-Air) firmware 
update pipeline with signature verification.

### Pipeline Steps

1. **Build** – Firmware is compiled and packaged
2. **Sign** – Firmware is signed using private key (see /Signing)
3. **Verify** – Signature is automatically verified (see /Verification)
4. **Upload** – Signed firmware uploaded to secure server/AWS S3
5. **Release** – Final release packaged and published (see /release)
6. **Test** – Release tested before distribution (see /Tests)

### Folder Structure
- `/Signing` – Signing scripts and keys
- `/Verification` – Automated verification scripts
- `/deployment` – Deployment configuration files
- `/release` – Final release artifacts
- `/Tests` – Test scripts and reports
- `/docs` – Project documentation

### How to Deploy
1. Place firmware binary in `/deployment` folder
2. Run signing script from `/Signing`
3. Verification runs automatically
4. Upload artifact to release server
5. Tag release version and publish

### Member 4 – Deployment & Verification Manager
- Automated signature verification ✅
- Artifact upload configured ✅
- GitHub documentation updated ✅
- Release testing report ✅
