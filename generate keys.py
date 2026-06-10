 from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate RSA 2048-bit private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,