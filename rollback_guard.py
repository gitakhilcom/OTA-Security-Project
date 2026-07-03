
"""
Core anti-rollback logic for the Edge Verification Agent.
"""

import json
import logging
import os

logging.basicConfig(
    filename="rollback_security.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


class RollbackError(Exception):
    """Raised when manifest data is malformed enough that rollback status can't be determined."""
    pass


def validate_manifest_fields(manifest: dict):
    """
    Confirms required fields exist and are the correct type.
    Corrupted/missing data must FAIL SAFE (reject), never silently pass.
    """
    required = ["build_timestamp", "build_iteration"]
    for field in required:
        if field not in manifest:
            raise RollbackError(f"Missing required field: {field}")

        value = manifest[field]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise RollbackError(f"Field '{field}' has invalid type: {type(value)}")

        if value < 0:
            raise RollbackError(f"Field '{field}' is negative: {value}")

    return True


def check_rollback(current_state: dict, incoming_manifest: dict) -> bool:
    """
    Returns True if the incoming firmware is safe to install (i.e. NOT a rollback).
    Returns False (and logs a critical alert) if it's a rollback attempt or
    if the data is too corrupted to trust.
    """
    try:
        validate_manifest_fields(incoming_manifest)
        validate_manifest_fields(current_state)
    except RollbackError as e:
        logging.critical(f"REJECTED — corrupted version data: {e}")
        return False

    incoming_ts = incoming_manifest["build_timestamp"]
    incoming_iter = incoming_manifest["build_iteration"]
    current_ts = current_state["build_timestamp"]
    current_iter = current_state["build_iteration"]

    if incoming_ts < current_ts:
        logging.critical(
            f"ROLLBACK BLOCKED: incoming timestamp {incoming_ts} < installed {current_ts}"
        )
        return False

    if incoming_ts == current_ts and incoming_iter <= current_iter:
        logging.critical(
            f"ROLLBACK/REPLAY BLOCKED: identical timestamp, "
            f"incoming iteration {incoming_iter} <= installed {current_iter}"
        )
        return False

    if incoming_ts > current_ts and incoming_iter <= current_iter:
        # Timestamp moved forward but build_iteration didn't — inconsistent manifest.
        # Fail safe: treat as suspicious rather than trusting timestamp alone.
        logging.critical(
            f"REJECTED — inconsistent manifest: newer timestamp but "
            f"iteration {incoming_iter} did not increase from {current_iter}"
        )
        return False

    logging.info(
        f"Version check passed: {current_ts}/{current_iter} -> {incoming_ts}/{incoming_iter}"
    )
    return True

"""
Core anti-rollback logic for the Edge Verification Agent.
"""

import json
import logging
import os

logging.basicConfig(
    filename="rollback_security.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


class RollbackError(Exception):
    """Raised when manifest data is malformed enough that rollback status can't be determined."""
    pass


def validate_manifest_fields(manifest: dict):
    """
    Confirms required fields exist and are the correct type.
    Corrupted/missing data must FAIL SAFE (reject), never silently pass.
    """
    required = ["build_timestamp", "build_iteration"]
    for field in required:
        if field not in manifest:
            raise RollbackError(f"Missing required field: {field}")

        value = manifest[field]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise RollbackError(f"Field '{field}' has invalid type: {type(value)}")

        if value < 0:
            raise RollbackError(f"Field '{field}' is negative: {value}")

    return True


def check_rollback(current_state: dict, incoming_manifest: dict) -> bool:
    """
    Returns True if the incoming firmware is safe to install (i.e. NOT a rollback).
    Returns False (and logs a critical alert) if it's a rollback attempt or
    if the data is too corrupted to trust.
    """
    try:
        validate_manifest_fields(incoming_manifest)
        validate_manifest_fields(current_state)
    except RollbackError as e:
        logging.critical(f"REJECTED — corrupted version data: {e}")
        return False

    incoming_ts = incoming_manifest["build_timestamp"]
    incoming_iter = incoming_manifest["build_iteration"]
    current_ts = current_state["build_timestamp"]
    current_iter = current_state["build_iteration"]

    if incoming_ts < current_ts:
        logging.critical(
            f"ROLLBACK BLOCKED: incoming timestamp {incoming_ts} < installed {current_ts}"
        )
        return False

    if incoming_ts == current_ts and incoming_iter <= current_iter:
        logging.critical(
            f"ROLLBACK/REPLAY BLOCKED: identical timestamp, "
            f"incoming iteration {incoming_iter} <= installed {current_iter}"
        )
        return False

    if incoming_ts > current_ts and incoming_iter <= current_iter:
        # Timestamp moved forward but build_iteration didn't — inconsistent manifest.
        # Fail safe: treat as suspicious rather than trusting timestamp alone.
        logging.critical(
            f"REJECTED — inconsistent manifest: newer timestamp but "
            f"iteration {incoming_iter} did not increase from {current_iter}"
        )
        return False

    logging.info(
        f"Version check passed: {current_ts}/{current_iter} -> {incoming_ts}/{incoming_iter}"
    )
    return True

