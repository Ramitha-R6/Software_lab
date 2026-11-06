import pytest
from course_registration import can_register, waitlist_position, late_fee

# --- Starter test cases (retained) ---
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"

def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0

# --- Additional test cases for Code (Line) Coverage ---

# Tests for can_register
def test_can_register_unknown_status_raises_error():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("guest", 10, 3, True)

def test_can_register_invalid_course_credits_raises_error():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)

def test_can_register_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"

def test_can_register_credit_limit_exceeded():
    assert can_register("regular", 22, 4, True) == "credit limit exceeded"

def test_can_register_probation_success():
    assert can_register("probation", 12, 4, True) == "registered"

def test_can_register_honors_success():
    assert can_register("honors", 24, 4, True) == "registered"

# Tests for waitlist_position
def test_waitlist_position_invalid_capacity_raises_error():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)

def test_waitlist_position_full_waitlist():
    assert waitlist_position(40, 40, 10) == -1

def test_waitlist_position_added_to_waitlist():
    assert waitlist_position(40, 40, 4) == 5

# Tests for late_fee
def test_late_fee_not_late():
    assert late_fee(0, 15, False) == 0

def test_late_fee_with_waiver():
    assert late_fee(5, 15, True) == 0

def test_late_fee_within_one_week():
    assert late_fee(5, 15, False) == 500

def test_late_fee_more_than_one_week():
    # 500 + (10 - 7) * 100 = 800
    assert late_fee(10, 15, False) == 800

def test_late_fee_heavy_credit_surcharge():
    # credits > 20 adds 250 surcharge: 500 + 250 = 750
    assert late_fee(5, 22, False) == 750

def test_late_fee_capped_at_maximum():
    # 500 + (25 - 7) * 100 + 250 = 2550 -> capped at 2000
    assert late_fee(25, 25, False) == 2000
