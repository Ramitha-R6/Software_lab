import pytest
from course_registration import can_register, waitlist_position, late_fee

# ============================================================================
# Starter test cases (retained from test_course_registration.py)
# ============================================================================
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"

def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0


# ============================================================================
# Branch Coverage Tests: can_register
# Decisions:
# 1. student_status not in MAX_CREDITS (True / False)
# 2. course_credits <= 0 (True / False; boundary <= 0 vs > 0)
# 3. not prerequisites_met (True / False)
# 4. current_credits + course_credits > MAX_CREDITS[status] (True / False; exact boundaries)
# ============================================================================

def test_can_register_invalid_status_raises_error():
    # Branch 1 True
    with pytest.raises(ValueError, match="unknown status"):
        can_register("alumni", 10, 3, True)

def test_can_register_empty_status_raises_error():
    # Branch 1 True (edge case: empty string)
    with pytest.raises(ValueError, match="unknown status"):
        can_register("", 10, 3, True)

def test_can_register_zero_course_credits_raises_error():
    # Branch 2 True (boundary: course_credits == 0)
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)

def test_can_register_negative_course_credits_raises_error():
    # Branch 2 True (course_credits < 0)
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, -3, True)

def test_can_register_prerequisites_not_met():
    # Branch 3 True
    assert can_register("regular", 10, 4, False) == "prerequisites missing"

def test_can_register_regular_limit_exceeded():
    # Branch 4 True (regular: 21 + 4 = 25 > 24)
    assert can_register("regular", 21, 4, True) == "credit limit exceeded"

def test_can_register_regular_at_exact_limit():
    # Branch 4 False (boundary: 20 + 4 = 24 <= 24)
    assert can_register("regular", 20, 4, True) == "registered"

def test_can_register_probation_limit_exceeded():
    # Branch 4 True for probation (limit 16: 14 + 3 = 17 > 16)
    assert can_register("probation", 14, 3, True) == "credit limit exceeded"

def test_can_register_probation_at_exact_limit():
    # Branch 4 False for probation (boundary: 12 + 4 = 16 <= 16)
    assert can_register("probation", 12, 4, True) == "registered"

def test_can_register_honors_limit_exceeded():
    # Branch 4 True for honors (limit 28: 26 + 3 = 29 > 28)
    assert can_register("honors", 26, 3, True) == "credit limit exceeded"

def test_can_register_honors_at_exact_limit():
    # Branch 4 False for honors (boundary: 24 + 4 = 28 <= 28)
    assert can_register("honors", 24, 4, True) == "registered"


# ============================================================================
# Branch Coverage Tests: waitlist_position
# Decisions:
# 1. capacity <= 0 (True / False; boundary <= 0 vs > 0)
# 2. enrolled < capacity (True / False; enrolled < capacity vs enrolled >= capacity)
# 3. waitlist_length >= 10 (True / False; boundary 9, 10, 11)
# ============================================================================

def test_waitlist_position_zero_capacity_raises_error():
    # Branch 1 True (boundary: capacity == 0)
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)

def test_waitlist_position_negative_capacity_raises_error():
    # Branch 1 True (capacity < 0)
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, -5, 0)

def test_waitlist_position_enrolled_less_than_capacity():
    # Branch 2 True
    assert waitlist_position(25, 30, 0) == 0

def test_waitlist_position_enrolled_exactly_equals_capacity():
    # Branch 2 False (boundary: enrolled == capacity), waitlist_length < 10
    assert waitlist_position(30, 30, 0) == 1

def test_waitlist_position_enrolled_exceeds_capacity():
    # Branch 2 False (enrolled > capacity)
    assert waitlist_position(35, 30, 3) == 4

def test_waitlist_position_waitlist_at_boundary_nine():
    # Branch 3 False (boundary: waitlist_length == 9 < 10)
    assert waitlist_position(30, 30, 9) == 10

def test_waitlist_position_waitlist_at_boundary_ten_full():
    # Branch 3 True (boundary: waitlist_length == 10 >= 10)
    assert waitlist_position(30, 30, 10) == -1

def test_waitlist_position_waitlist_exceeds_ten():
    # Branch 3 True (waitlist_length > 10)
    assert waitlist_position(30, 30, 12) == -1


# ============================================================================
# Branch Coverage Tests: late_fee
# Decisions:
# 1. days_late <= 0 (True / False; boundary 0 vs negative vs positive)
# 2. has_waiver (True / False)
# 3. days_late <= 7 (True / False; boundary 7 vs 8)
# 4. credits > 20 (True / False; boundary 20 vs 21)
# 5. fee > 2000 (True / False; boundary 2000 vs 2001+)
# ============================================================================

def test_late_fee_zero_days_late():
    # Branch 1 True (boundary: days_late == 0)
    assert late_fee(0, 15, False) == 0

def test_late_fee_negative_days_late():
    # Branch 1 True (days_late < 0)
    assert late_fee(-3, 15, False) == 0

def test_late_fee_with_waiver():
    # Branch 2 True
    assert late_fee(5, 15, True) == 0

def test_late_fee_days_late_within_seven_boundary():
    # Branch 3 True (boundary: days_late == 7 <= 7), credits <= 20 (boundary: 20)
    assert late_fee(7, 20, False) == 500

def test_late_fee_days_late_one_day():
    # Branch 3 True (days_late == 1), credits < 20
    assert late_fee(1, 10, False) == 500

def test_late_fee_days_late_eight_boundary():
    # Branch 3 False (boundary: days_late == 8 > 7): 500 + (8 - 7)*100 = 600, credits <= 20
    assert late_fee(8, 15, False) == 600

def test_late_fee_credits_exceed_twenty_boundary():
    # Branch 4 True (boundary: credits == 21 > 20): 500 + 250 = 750
    assert late_fee(5, 21, False) == 750

def test_late_fee_credits_exactly_twenty_boundary():
    # Branch 4 False (boundary: credits == 20 <= 20): no surcharge
    assert late_fee(5, 20, False) == 500

def test_late_fee_fee_exceeds_two_thousand_cap():
    # Branch 5 True: fee > 2000 -> capped at 2000
    # days_late = 25, credits = 25 -> 500 + 1800 + 250 = 2550 -> 2000
    assert late_fee(25, 25, False) == 2000

def test_late_fee_fee_exactly_two_thousand_boundary():
    # Branch 5 False (boundary: fee == 2000 <= 2000)
    # days_late = 22, credits = 15 -> 500 + (22 - 7)*100 = 2000, credits <= 20 -> no cap needed
    assert late_fee(22, 15, False) == 2000
