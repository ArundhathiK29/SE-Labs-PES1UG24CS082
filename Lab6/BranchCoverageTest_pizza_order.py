"""Decision coverage with threshold pairs and independent expected values."""
import pytest
from pizza_order import pizza_price, order_discount, delivery_status


@pytest.mark.parametrize("size,toppings,cheese,expected", [
    ("small", 0, False, 200),
    ("medium", 0, False, 350),
    ("large", 0, False, 500),
    ("medium", 3, False, 470),  # Last full-price topping.
    ("medium", 4, False, 500),  # First reduced-price topping.
    ("large", 6, False, 710),
    ("medium", 0, True, 450),
    ("large", 4, True, 750),
])
def test_valid_price_branches(size, toppings, cheese, expected):
    assert pizza_price(size, toppings, cheese) == expected


@pytest.mark.parametrize("size,toppings,cheese,message", [
    ("invalid", 0, False, "unknown size"),
    ("medium", -1, False, "invalid toppings"),
    ("small", 0, True, "cheese burst not available for small"),
])
def test_validation_branches(size, toppings, cheese, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        pizza_price(size, toppings, cheese)


@pytest.mark.parametrize("total,day,student,expected", [
    (0, "monday", False, 0),
    (299, "tuesday", True, 0),
    (300, "tuesday", False, 150),
    (300, "tuesday", True, 200),
    (301, "tuesday", False, 150),  # Integer division floors.
    (300, "saturday", False, 0),
    (300, "saturday", True, 50),
    (300, "sunday", False, 0),
    (300, "sunday", True, 50),
    (300, "monday", False, 30),
    (300, "monday", True, 80),
    (309, "friday", False, 30),
    (310, "friday", False, 31),
])
def test_discount_decisions(total, day, student, expected):
    assert order_discount(total, day, student) == expected


@pytest.mark.parametrize("minutes,distance,expected", [
    (0, 0, "on time"),
    (30, 10, "on time"),
    (31, 10, "late"),
    (45, 10, "late"),
    (46, 10, "free pizza"),
    (20, 10.01, "not deliverable"),
    (46, 11, "not deliverable"),  # Distance decision takes priority.
])
def test_delivery_decisions(minutes, distance, expected):
    assert delivery_status(minutes, distance) == expected
