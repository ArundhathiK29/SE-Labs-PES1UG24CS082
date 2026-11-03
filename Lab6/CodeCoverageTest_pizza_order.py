"""Statement coverage: execute every executable line in the assigned module."""
import pytest
from pizza_order import pizza_price, order_discount, delivery_status


@pytest.mark.parametrize("size,toppings,cheese,expected", [
    ("medium", 0, False, 350),
    ("small", 3, False, 320),
    ("large", 4, True, 750),
])
def test_pizza_prices(size, toppings, cheese, expected):
    assert pizza_price(size, toppings, cheese) == expected


@pytest.mark.parametrize("size,toppings,cheese,message", [
    ("extra-large", 0, False, "unknown size"),
    ("medium", -1, False, "invalid toppings"),
    ("small", 0, True, "cheese burst not available for small"),
])
def test_invalid_pizza_orders(size, toppings, cheese, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        pizza_price(size, toppings, cheese)


@pytest.mark.parametrize("total,day,student,expected", [
    (299, "tuesday", True, 0),
    (600, "tuesday", True, 350),
    (600, "saturday", False, 0),
    (600, "monday", False, 60),
])
def test_discount_statements(total, day, student, expected):
    assert order_discount(total, day, student) == expected


@pytest.mark.parametrize("minutes,distance,expected", [
    (20, 11, "not deliverable"),
    (30, 10, "on time"),
    (45, 5, "late"),
    (46, 5, "free pizza"),
])
def test_delivery_returns(minutes, distance, expected):
    assert delivery_status(minutes, distance) == expected
