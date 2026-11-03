import pytest
from pizza_order import pizza_price, order_discount, delivery_status

#Example test cases:
def test_plain_medium_pizza():
    assert pizza_price("medium", 0, False) == 350

def test_on_time_delivery():
    assert delivery_status(20, 3) == "on time"

#Write the rest of the test cases so that the code is 90- 100% covered.
