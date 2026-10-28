"""Tests that exercise both outcomes of each decision in course_registration.py."""
import pytest
from course_registration import can_register, waitlist_position, late_fee


@pytest.mark.parametrize("status,current,course,prereq,expected", [
    ("regular", 20, 4, True, "registered"),       # exact credit limit
    ("regular", 20, 5, True, "credit limit exceeded"),
    ("probation", 15, 2, True, "credit limit exceeded"),
    ("honors", 24, 4, True, "registered"),
    ("regular", 0, 3, False, "prerequisites missing"),
])
def test_can_register_decision_outcomes(status, current, course, prereq, expected):
    assert can_register(status, current, course, prereq) == expected


@pytest.mark.parametrize("status,credits,expected_message", [
    ("unknown", 3, "unknown status"),
    ("regular", 0, "invalid course credits"),
    ("regular", -1, "invalid course credits"),
])
def test_can_register_validation_errors(status, credits, expected_message):
    with pytest.raises(ValueError, match=expected_message):
        can_register(status, 0, credits, True)


@pytest.mark.parametrize("enrolled,capacity,length,expected", [
    (30, 40, 0, 0),       # enrolled < capacity
    (40, 40, 0, 1),       # queue begins at capacity
    (45, 40, 4, 5),       # ordinary waitlist position
    (40, 40, 9, 10),      # last accepted position
    (40, 40, 10, -1),     # closed waitlist
    (40, 40, 11, -1),     # beyond closed waitlist
])
def test_waitlist_decision_outcomes(enrolled, capacity, length, expected):
    assert waitlist_position(enrolled, capacity, length) == expected


@pytest.mark.parametrize("capacity", [0, -1])
def test_waitlist_invalid_capacity(capacity):
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, capacity, 0)


@pytest.mark.parametrize("days,credits,waiver,expected", [
    (0, 10, False, 0),       # days_late <= 0
    (-1, 10, False, 0),
    (5, 10, True, 0),        # waiver branch
    (1, 10, False, 500),     # <= 7 branch
    (7, 10, False, 500),
    (8, 10, False, 600),     # > 7 branch
    (7, 20, False, 500),     # credits > 20 is false
    (7, 21, False, 750),     # credits > 20 is true
    (30, 25, False, 2000),   # cap branch true
])
def test_late_fee_decision_outcomes(days, credits, waiver, expected):
    assert late_fee(days, credits, waiver) == expected
