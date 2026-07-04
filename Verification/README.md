# Signature Verification

Member4-verification
This module is responsible for verifying firmware signatures using a public key before installation.


## Week 3 Day 1

### Security Alert Logging

The system records every firmware verification attempt with:
- Timestamp
- Firmware filename
- Verification status (PASS/FAIL)
- Failure reason

## Objective
Verify the authenticity of firmware updates using a public key.

## Process
1. Obtain the firmware file.
2. Obtain the digital signature.
3. Load the public key.
4. Verify the signature using the public key.
5. Accept the firmware only if verification succeeds.

## Purpose
Verify the firmware signature using the public key.

## Steps
1. Receive firmware file.
2. Load public key.
3. Verify digital signature.
4. Accept valid firmware and reject invalid firmware.

## Expected Result
Valid signatures are accepted and invalid signatures are rejected.
main
