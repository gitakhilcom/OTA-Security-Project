# Signature Verification

## Objective
Verify the authenticity of firmware updates using a public key.

## Process
1. Obtain the firmware file.
2. Obtain the digital signature.
3. Load the public key.
4. Verify the signature using the public key.
5. Accept the firmware only if verification succeeds.

## Expected Result
Valid signatures are accepted and invalid signatures are rejected.
