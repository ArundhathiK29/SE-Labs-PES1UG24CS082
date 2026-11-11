"""Fuzz input validation and preserve valid pizza order behaviour.

Invalid input returns None; valid zero totals remain distinguishable.
PROCESSOR_MODULE=original.processor replays the same tests on the starter.
"""
import importlib
import os
import re

import pytest
from hypothesis import example, given, settings, strategies as st

processor = importlib.import_module(os.getenv("PROCESSOR_MODULE", "processor"))
settings.register_profile("lab7", max_examples=200, deadline=None,
                          derandomize=True, database=None, report_multiple_bugs=False)
settings.load_profile("lab7")

PRICES = {"cheese": 40, "olives": 30, "onion": 20, "paneer": 50}
SIZES = {"S": 8, "M": 10, "L": 12}
arbitrary_input = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.booleans(),
    st.binary(), st.lists(st.integers(), max_size=10),
    st.dictionaries(st.text(max_size=10), st.integers(), max_size=5),
)


@given(arbitrary_input)
def test_toppings_price_no_crash(value):
    result = processor.toppings_price(value)
    expected = None
    if isinstance(value, str) and len(value) <= 4096:
        tokens = [token.strip().lower() for token in value.split(",")]
        if all(token in PRICES for token in tokens):
            expected = sum(PRICES[token] for token in tokens)
    assert result == expected


@given(arbitrary_input)
def test_pizza_inches_no_crash(value):
    expected = None
    if isinstance(value, str) and len(value) <= 4096:
        expected = SIZES.get(value.strip().upper())
    assert processor.pizza_inches(value) == expected


@given(arbitrary_input)
def test_split_bill_no_crash(value):
    result = processor.split_bill(value)
    expected = None
    if isinstance(value, str) and len(value) <= 4096:
        match = re.fullmatch(r"\s*([0-9]{1,12})\s*/\s*([0-9]{1,12})\s*", value)
        if match and int(match[2]) > 0:
            expected = round(int(match[1]) / int(match[2]), 2)
    assert result == expected


@given(st.lists(st.sampled_from(list(PRICES)), min_size=1, max_size=30))
def test_toppings_valid_sum(names):
    text = ",".join(" " + name.upper() + " " for name in names)
    assert processor.toppings_price(text) == sum(PRICES[name] for name in names)


@given(st.sampled_from(list(SIZES)), st.sampled_from(["", " ", "\t", "\n"]))
def test_size_normalization(size, whitespace):
    assert processor.pizza_inches(whitespace + size.lower() + whitespace) == SIZES[size]


@given(st.integers(0, 999_999_999_999), st.integers(1, 999_999_999_999))
@example(0, 1)
@example(900, 3)
@example(100, 3)
def test_bill_valid_result(total, people):
    assert processor.split_bill(f" {total} / {people} ") == round(total / people, 2)


@given(st.integers(min_value=0, max_value=999_999_999_999))
def test_bill_zero_people_rejected(total):
    assert processor.split_bill(f"{total}/0") is None


@given(st.text())
def test_toppings_text_no_crash(value):
    result = processor.toppings_price(value)
    assert result is None or isinstance(result, int) and result >= 0


@given(st.text())
def test_size_text_no_crash(value):
    assert processor.pizza_inches(value) in (None, 8, 10, 12)


@given(st.text())
def test_bill_text_no_crash(value):
    result = processor.split_bill(value)
    assert result is None or isinstance(result, float) and result >= 0


@pytest.mark.parametrize("length,expected", [(4096, 10), (4097, None)])
def test_size_input_length_boundary(length, expected):
    assert processor.pizza_inches(" " * (length - 1) + "M") == expected


@pytest.mark.parametrize("text", ["", ",", "cheese,", "cheese,,onion", "tomato"])
def test_toppings_invalid_tokens(text):
    assert processor.toppings_price(text) is None


@pytest.mark.parametrize("text", ["-1/2", "10/-2", "1.5/2", "10/2/3", "10", "/", "+1/2",
                                       "nan/2", "inf/2", "1_000/2", "9" * 13 + "/1"])
def test_bill_invalid_format(text):
    assert processor.split_bill(text) is None


@pytest.mark.parametrize("function,text", [
    ("toppings_price", "cheese," * 1000),
    ("pizza_inches", "M" * 5000),
    ("split_bill", "9" * 5000 + "/1"),
], ids=["oversized-toppings", "oversized-size", "oversized-bill"])
def test_oversized_input_rejected(function, text):
    assert getattr(processor, function)(text) is None
