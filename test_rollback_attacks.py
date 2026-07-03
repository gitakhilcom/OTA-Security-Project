
"""
test_rollback_attacks.py
Member 3 — Rollback Attack Simulation & Testing Lead

Covers three categories required by the project brief:
  1. Rollback attacks (older firmware presented as an "update")
  2. Edge cases: identical version numbers / replay attempts
  3. Edge cases: corrupted or malformed version data

Run with:  pytest -v test_rollback_attacks.py
"""

import pytest
from rollback_guard import check_rollback, RollbackError, validate_manifest_fields


# ---------------------------------------------------------------------------
# Fixtures — a "currently installed" device state used as the baseline
# ---------------------------------------------------------------------------

@pytest.fixture
def installed_state():
    return {"build_timestamp": 1_751_385_600, "build_iteration": 42}


# ---------------------------------------------------------------------------
# 1. ROLLBACK ATTACK SIMULATIONS
# ---------------------------------------------------------------------------

class TestRollbackAttacks:

    def test_older_timestamp_is_blocked(self, installed_state):
        """Classic rollback: attacker pushes an older, signed firmware."""
        attack_manifest = {"build_timestamp": 1_751_300_000, "build_iteration": 41}
        assert check_rollback(installed_state, attack_manifest) is False

    def test_older_timestamp_far_in_past_is_blocked(self, installed_state):
        """Attacker tries a very old firmware (e.g. v1.0.0 from a year ago)."""
        attack_manifest = {"build_timestamp": 1_700_000_000, "build_iteration": 1}
        assert check_rollback(installed_state, attack_manifest) is False

    def test_older_timestamp_but_higher_iteration_is_still_blocked(self, installed_state):
        """
        Attacker tries to game the system by inflating build_iteration
        while keeping an old timestamp. Timestamp must win — this must
        still be blocked, since iteration alone isn't trustworthy without
        a consistent timestamp.
        """
        attack_manifest = {"build_timestamp": 1_700_000_000, "build_iteration": 9999}
        assert check_rollback(installed_state, attack_manifest) is False

    def test_valid_forward_update_is_allowed(self, installed_state):
        """Sanity check: a legitimate newer firmware must NOT be blocked."""
        good_manifest = {"build_timestamp": 1_751_400_000, "build_iteration": 43}
        assert check_rollback(installed_state, good_manifest) is True

    def test_replayed_old_valid_signature_is_blocked(self, installed_state):
        """
        Simulates a captured/replayed old (but validly signed at the time)
        manifest being re-served to the device — must still be rejected
        purely on version grounds, independent of signature validity.
        """
        replayed_manifest = {"build_timestamp": 1_751_000_000, "build_iteration": 30}
        assert check_rollback(installed_state, replayed_manifest) is False


# ---------------------------------------------------------------------------
# 2. IDENTICAL VERSION / REPLAY EDGE CASES
# ---------------------------------------------------------------------------

class TestIdenticalVersions:

    def test_identical_timestamp_and_iteration_is_blocked(self, installed_state):
        """Exact duplicate of the currently installed manifest — must be rejected."""
        same_manifest = dict(installed_state)
        assert check_rollback(installed_state, same_manifest) is False

    def test_identical_timestamp_lower_iteration_is_blocked(self, installed_state):
        attack_manifest = {"build_timestamp": installed_state["build_timestamp"], "build_iteration": 10}
        assert check_rollback(installed_state, attack_manifest) is False

    def test_identical_timestamp_higher_iteration_is_allowed(self, installed_state):
        """
        Edge case: same build day, but a genuine patch iteration bump.
        Should be ALLOWED since iteration strictly increased.
        """
        good_manifest = {"build_timestamp": installed_state["build_timestamp"], "build_iteration": 43}
        assert check_rollback(installed_state, good_manifest) is True

    def test_new_timestamp_without_iteration_bump_is_blocked(self, installed_state):
        """
        Inconsistent manifest: timestamp moved forward but iteration didn't
        increase. This shouldn't happen in a legitimate build pipeline —
        treat as suspicious and fail safe.
        """
        suspicious_manifest = {"build_timestamp": 1_751_500_000, "build_iteration": 42}
        assert check_rollback(installed_state, suspicious_manifest) is False


# ---------------------------------------------------------------------------
# 3. CORRUPTED / MALFORMED VERSION DATA
# ---------------------------------------------------------------------------

class TestCorruptedVersionData:

    def test_missing_timestamp_field_is_blocked(self, installed_state):
        corrupt_manifest = {"build_iteration": 43}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_missing_iteration_field_is_blocked(self, installed_state):
        corrupt_manifest = {"build_timestamp": 1_751_400_000}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_empty_manifest_is_blocked(self, installed_state):
        assert check_rollback(installed_state, {}) is False

    def test_negative_timestamp_is_blocked(self, installed_state):
        corrupt_manifest = {"build_timestamp": -1, "build_iteration": 43}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_negative_iteration_is_blocked(self, installed_state):
        corrupt_manifest = {"build_timestamp": 1_751_400_000, "build_iteration": -5}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_string_instead_of_number_is_blocked(self, installed_state):
        """e.g. a manifest field corrupted to 'null' or 'N/A' as a string."""
        corrupt_manifest = {"build_timestamp": "not_a_number", "build_iteration": 43}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_none_value_is_blocked(self, installed_state):
        corrupt_manifest = {"build_timestamp": None, "build_iteration": 43}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_boolean_value_is_blocked(self, installed_state):
        """
        Python quirk: True/False are technically instances of int.
        A corrupted or maliciously crafted manifest might smuggle a bool in
        (e.g. JSON 'true' misparsed) — must not be silently accepted as 1/0.
        """
        corrupt_manifest = {"build_timestamp": True, "build_iteration": 43}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_float_timestamp_is_still_valid(self, installed_state):
        """Floats are legitimate (some systems emit epoch time with decimals)."""
        good_manifest = {"build_timestamp": 1_751_400_000.5, "build_iteration": 43}
        assert check_rollback(installed_state, good_manifest) is True

    def test_corrupted_installed_state_fails_safe(self):
        """
        If the DEVICE's own stored state is corrupted (e.g. flash corruption),
        the system must fail safe and block the update rather than assume
        anything is newer than corrupted data.
        """
        corrupted_state = {"build_timestamp": "garbage", "build_iteration": 42}
        good_manifest = {"build_timestamp": 1_751_400_000, "build_iteration": 43}
        assert check_rollback(corrupted_state, good_manifest) is False

    def test_validate_manifest_fields_raises_on_missing_field(self):
        with pytest.raises(RollbackError):
            validate_manifest_fields({"build_iteration": 1})

    def test_validate_manifest_fields_raises_on_negative(self):
        with pytest.raises(RollbackError):
            validate_manifest_fields({"build_timestamp": -100, "build_iteration": 1})

    def test_validate_manifest_fields_passes_on_valid_data(self):
        assert validate_manifest_fields({"build_timestamp": 100, "build_iteration": 1}) is True


# ---------------------------------------------------------------------------
# 4. Optional: parametrized sweep for quick regression coverage
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "incoming_ts,incoming_iter,expected",
    [
        (1_751_385_600, 43, True),    # same ts, iter bump -> allowed
        (1_751_385_600, 42, False),   # identical -> blocked
        (1_751_385_600, 41, False),   # same ts, lower iter -> blocked
        (1_751_400_000, 43, True),    # forward, consistent -> allowed
        (1_751_300_000, 100, False),  # older ts, inflated iter -> blocked
        (1_751_400_000, 42, False),   # forward ts, stale iter -> blocked (suspicious)
    ],
)
def test_rollback_matrix(installed_state, incoming_ts, incoming_iter, expected):
    manifest = {"build_timestamp": incoming_ts, "build_iteration": incoming_iter}
    assert check_rollback(installed_state, manifest) is expected
=======
"""
test_rollback_attacks.py
Member 3 — Rollback Attack Simulation & Testing Lead

Covers three categories required by the project brief:
  1. Rollback attacks (older firmware presented as an "update")
  2. Edge cases: identical version numbers / replay attempts
  3. Edge cases: corrupted or malformed version data

Run with:  pytest -v test_rollback_attacks.py
"""

import pytest
from rollback_guard import check_rollback, RollbackError, validate_manifest_fields


# ---------------------------------------------------------------------------
# Fixtures — a "currently installed" device state used as the baseline
# ---------------------------------------------------------------------------

@pytest.fixture
def installed_state():
    return {"build_timestamp": 1_751_385_600, "build_iteration": 42}


# ---------------------------------------------------------------------------
# 1. ROLLBACK ATTACK SIMULATIONS
# ---------------------------------------------------------------------------

class TestRollbackAttacks:

    def test_older_timestamp_is_blocked(self, installed_state):
        """Classic rollback: attacker pushes an older, signed firmware."""
        attack_manifest = {"build_timestamp": 1_751_300_000, "build_iteration": 41}
        assert check_rollback(installed_state, attack_manifest) is False

    def test_older_timestamp_far_in_past_is_blocked(self, installed_state):
        """Attacker tries a very old firmware (e.g. v1.0.0 from a year ago)."""
        attack_manifest = {"build_timestamp": 1_700_000_000, "build_iteration": 1}
        assert check_rollback(installed_state, attack_manifest) is False

    def test_older_timestamp_but_higher_iteration_is_still_blocked(self, installed_state):
        """
        Attacker tries to game the system by inflating build_iteration
        while keeping an old timestamp. Timestamp must win — this must
        still be blocked, since iteration alone isn't trustworthy without
        a consistent timestamp.
        """
        attack_manifest = {"build_timestamp": 1_700_000_000, "build_iteration": 9999}
        assert check_rollback(installed_state, attack_manifest) is False

    def test_valid_forward_update_is_allowed(self, installed_state):
        """Sanity check: a legitimate newer firmware must NOT be blocked."""
        good_manifest = {"build_timestamp": 1_751_400_000, "build_iteration": 43}
        assert check_rollback(installed_state, good_manifest) is True

    def test_replayed_old_valid_signature_is_blocked(self, installed_state):
        """
        Simulates a captured/replayed old (but validly signed at the time)
        manifest being re-served to the device — must still be rejected
        purely on version grounds, independent of signature validity.
        """
        replayed_manifest = {"build_timestamp": 1_751_000_000, "build_iteration": 30}
        assert check_rollback(installed_state, replayed_manifest) is False


# ---------------------------------------------------------------------------
# 2. IDENTICAL VERSION / REPLAY EDGE CASES
# ---------------------------------------------------------------------------

class TestIdenticalVersions:

    def test_identical_timestamp_and_iteration_is_blocked(self, installed_state):
        """Exact duplicate of the currently installed manifest — must be rejected."""
        same_manifest = dict(installed_state)
        assert check_rollback(installed_state, same_manifest) is False

    def test_identical_timestamp_lower_iteration_is_blocked(self, installed_state):
        attack_manifest = {"build_timestamp": installed_state["build_timestamp"], "build_iteration": 10}
        assert check_rollback(installed_state, attack_manifest) is False

    def test_identical_timestamp_higher_iteration_is_allowed(self, installed_state):
        """
        Edge case: same build day, but a genuine patch iteration bump.
        Should be ALLOWED since iteration strictly increased.
        """
        good_manifest = {"build_timestamp": installed_state["build_timestamp"], "build_iteration": 43}
        assert check_rollback(installed_state, good_manifest) is True

    def test_new_timestamp_without_iteration_bump_is_blocked(self, installed_state):
        """
        Inconsistent manifest: timestamp moved forward but iteration didn't
        increase. This shouldn't happen in a legitimate build pipeline —
        treat as suspicious and fail safe.
        """
        suspicious_manifest = {"build_timestamp": 1_751_500_000, "build_iteration": 42}
        assert check_rollback(installed_state, suspicious_manifest) is False


# ---------------------------------------------------------------------------
# 3. CORRUPTED / MALFORMED VERSION DATA
# ---------------------------------------------------------------------------

class TestCorruptedVersionData:

    def test_missing_timestamp_field_is_blocked(self, installed_state):
        corrupt_manifest = {"build_iteration": 43}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_missing_iteration_field_is_blocked(self, installed_state):
        corrupt_manifest = {"build_timestamp": 1_751_400_000}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_empty_manifest_is_blocked(self, installed_state):
        assert check_rollback(installed_state, {}) is False

    def test_negative_timestamp_is_blocked(self, installed_state):
        corrupt_manifest = {"build_timestamp": -1, "build_iteration": 43}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_negative_iteration_is_blocked(self, installed_state):
        corrupt_manifest = {"build_timestamp": 1_751_400_000, "build_iteration": -5}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_string_instead_of_number_is_blocked(self, installed_state):
        """e.g. a manifest field corrupted to 'null' or 'N/A' as a string."""
        corrupt_manifest = {"build_timestamp": "not_a_number", "build_iteration": 43}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_none_value_is_blocked(self, installed_state):
        corrupt_manifest = {"build_timestamp": None, "build_iteration": 43}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_boolean_value_is_blocked(self, installed_state):
        """
        Python quirk: True/False are technically instances of int.
        A corrupted or maliciously crafted manifest might smuggle a bool in
        (e.g. JSON 'true' misparsed) — must not be silently accepted as 1/0.
        """
        corrupt_manifest = {"build_timestamp": True, "build_iteration": 43}
        assert check_rollback(installed_state, corrupt_manifest) is False

    def test_float_timestamp_is_still_valid(self, installed_state):
        """Floats are legitimate (some systems emit epoch time with decimals)."""
        good_manifest = {"build_timestamp": 1_751_400_000.5, "build_iteration": 43}
        assert check_rollback(installed_state, good_manifest) is True

    def test_corrupted_installed_state_fails_safe(self):
        """
        If the DEVICE's own stored state is corrupted (e.g. flash corruption),
        the system must fail safe and block the update rather than assume
        anything is newer than corrupted data.
        """
        corrupted_state = {"build_timestamp": "garbage", "build_iteration": 42}
        good_manifest = {"build_timestamp": 1_751_400_000, "build_iteration": 43}
        assert check_rollback(corrupted_state, good_manifest) is False

    def test_validate_manifest_fields_raises_on_missing_field(self):
        with pytest.raises(RollbackError):
            validate_manifest_fields({"build_iteration": 1})

    def test_validate_manifest_fields_raises_on_negative(self):
        with pytest.raises(RollbackError):
            validate_manifest_fields({"build_timestamp": -100, "build_iteration": 1})

    def test_validate_manifest_fields_passes_on_valid_data(self):
        assert validate_manifest_fields({"build_timestamp": 100, "build_iteration": 1}) is True


# ---------------------------------------------------------------------------
# 4. Optional: parametrized sweep for quick regression coverage
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "incoming_ts,incoming_iter,expected",
    [
        (1_751_385_600, 43, True),    # same ts, iter bump -> allowed
        (1_751_385_600, 42, False),   # identical -> blocked
        (1_751_385_600, 41, False),   # same ts, lower iter -> blocked
        (1_751_400_000, 43, True),    # forward, consistent -> allowed
        (1_751_300_000, 100, False),  # older ts, inflated iter -> blocked
        (1_751_400_000, 42, False),   # forward ts, stale iter -> blocked (suspicious)
    ],
)
def test_rollback_matrix(installed_state, incoming_ts, incoming_iter, expected):
    manifest = {"build_timestamp": incoming_ts, "build_iteration": incoming_iter}
    assert check_rollback(installed_state, manifest) is expected
