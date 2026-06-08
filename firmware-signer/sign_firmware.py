import argparse
import sys
import os
from pathlib import Path

def validate_inputs(key_path, fw_path):
    """Check that key and firmware files exist before we do anything."""
    if not Path(key_path).is_file():
        sys.exit(f"[-] Key not found: {key_path}")
    if not Path(fw_path).is_file():
        sys.exit(f"[-] Firmware not found: {fw_path}")

