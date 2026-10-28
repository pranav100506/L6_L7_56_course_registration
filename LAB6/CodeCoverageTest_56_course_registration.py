"""Tests aimed at high line coverage for course_registration.py."""
import pytest
from course_registration import can_register, waitlist_position, late_fee


# can_register: normal registrations and all rejection outcomes

def test_registered_at_credit_limit():
    assert can_register("regular", 20, 4, True) == "registered"


def test_unknown_student_status_raises():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("guest", 0, 3, True)


def test_zero_course_credits_raise():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 0, 0, True)


def test_negative_course_credits_raise():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 0, -1, True)


def test_missing_prerequisites():
    assert can_register("regular", 0, 3, False) == "prerequisites missing"


def test_credit_limit_exceeded_for_probation_status():
    assert can_register("probation", 15, 2, True) == "credit limit exceeded"


def test_honors_status_can_register_within_limit():
    assert can_register("honors", 24, 4, True) == "registered"


# waitlist_position: invalid capacity, open seats, full list and ordinary queue

def test_invalid_zero_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)


def test_invalid_negative_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, -1, 0)


def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0


def test_exactly_capacity_is_waitlisted():
    assert waitlist_position(40, 40, 0) == 1


def test_waitlist_position_increments():
    assert waitlist_position(40, 40, 4) == 5


def test_full_waitlist_is_closed():
    assert waitlist_position(40, 40, 10) == -1


def test_waitlist_over_limit_is_closed():
    assert waitlist_position(40, 40, 12) == -1


# late_fee: early returns, waiver, fee brackets, credit surcharge and cap

def test_no_late_fee_when_not_late():
    assert late_fee(0, 10, False) == 0


def test_negative_lateness_has_no_fee():
    assert late_fee(-2, 10, False) == 0


def test_waiver_removes_fee():
    assert late_fee(5, 24, True) == 0


def test_seven_days_late_base_fee():
    assert late_fee(7, 10, False) == 500


def test_more_than_seven_days_adds_daily_fee():
    assert late_fee(8, 10, False) == 600


def test_more_than_twenty_credits_adds_surcharge():
    assert late_fee(7, 21, False) == 750


def test_fee_is_capped_at_two_thousand():
    assert late_fee(30, 25, False) == 2000
