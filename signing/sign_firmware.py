import os
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def load_private_key():
    """Load the private key from an environment variable (set via GitHub Secrets)."""
    private_key_pem = os.environ.get("PRIVATE_KEY")
    if not private_key_pem:
        raise ValueError("PRIVATE_KEY environment variable not set.")
    
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
    )
    return private_key