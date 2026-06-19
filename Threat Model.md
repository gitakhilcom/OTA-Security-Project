# OTA Firmware Signing Threat Model

## Version: 1.0
## Owner: Member 3 - Digital Signature Developer
## Date: June 7

### 1. Private Key Exposure Vectors

#### 1.1 Key in Git Repository
**Threat**: Developer accidentally commits `private_key.pem` to repo.  
**Impact**: Critical. Attacker can sign malicious firmware.  
**Mitigation**: `.gitignore` contains `*.pem`. CI uses `PRIVATE_KEY_B64` secret. Key never touches disk in CI.  

#### 1.2 Key in Logs / Console Output  
**Threat**: Script prints key content or base64 during debug.  
**Impact**: Critical. Key leaked in CI logs, accessible to all repo members.  
**Mitigation**: Never `print()` key bytes. Only log `key_size` and `public_exponent`. CI secret masking enabled.  

#### 1.3 Environment Variable Dump
**Threat**: Compromised CI runner dumps all env vars, exposing `PRIVATE_KEY_B64`.  
**Impact**: Critical. Full key compromise.  
**Mitigation**: Use GitHub Actions secrets. Rotate key quarterly. Principle of least privilege on repo access.

### 2. Signature Bypass Vectors
*To be expanded June 30 & July 1*

### 3. Cryptographic Algorithm Rationale  
*To be completed July 4*