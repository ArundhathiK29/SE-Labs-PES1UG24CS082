"""Pizza order input processing; invalid input returns None."""
import re

TOPPINGS = {"cheese": 40, "olives": 30, "onion": 20, "paneer": 50}
SIZES = {"S": 8, "M": 10, "L": 12}
MAX_INPUT_LENGTH = 4096
BILL_PATTERN = re.compile(r"\s*([0-9]{1,12})\s*/\s*([0-9]{1,12})\s*")


def toppings_price(toppings_csv):
    """Sum a nonempty CSV of known toppings; reject empty/unknown tokens."""
    if not isinstance(toppings_csv, str) or len(toppings_csv) > MAX_INPUT_LENGTH:
        return None
    tokens = [token.strip().lower() for token in toppings_csv.split(",")]
    if any(token not in TOPPINGS for token in tokens):
        return None
    return sum(TOPPINGS[token] for token in tokens)


def pizza_inches(size):
    """Accept S/M/L with case and surrounding whitespace normalization."""
    if not isinstance(size, str) or len(size) > MAX_INPUT_LENGTH:
        return None
    return SIZES.get(size.strip().upper())


def split_bill(text):
    """Split a nonnegative integer total among a positive integer count.

    Each field accepts 1-12 ASCII digits. The bounds prevent huge integer
    conversions and float overflow; rounding follows the original application.
    """
    if not isinstance(text, str) or len(text) > MAX_INPUT_LENGTH:
        return None
    match = BILL_PATTERN.fullmatch(text)
    if match is None:
        return None
    total, people = int(match[1]), int(match[2])
    if people == 0:
        return None
    return round(total / people, 2)


def main():
    operations = [
        ("toppings_price", "Enter toppings as CSV (e.g. cheese,olives): ",
         toppings_price, "Toppings Price:", "use known, nonempty topping names"),
        ("pizza_inches", "Enter pizza size (S/M/L): ",
         pizza_inches, "Size in Inches:", "choose S, M, or L"),
        ("split_bill", "Enter total and people (e.g. 900/3): ",
         split_bill, "Per Person:", "use total/people with people greater than zero"),
    ]
    for name, prompt, function, label, hint in operations:
        print(f"==== Running {name} ====")
        try:
            value = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled.")
            return
        result = function(value)
        if result is None:
            print(f"Invalid input: {hint}.")
        else:
            print(label, result)
        print()


if __name__ == "__main__":
    main()
