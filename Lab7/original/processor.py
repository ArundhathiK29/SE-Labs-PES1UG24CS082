TOPPINGS = {"cheese": 40, "olives": 30, "onion": 20, "paneer": 50}
SIZES = {"S": 8, "M": 10, "L": 12}

def toppings_price(toppings_csv):
    total = 0
    for t in toppings_csv.split(','):
        total += TOPPINGS[t.strip().lower()]
    return total

def pizza_inches(size):
    return SIZES[size.strip().upper()]

def split_bill(text):
    total, people = text.split('/')
    return round(int(total) / int(people), 2)

def main():
    print("==== Running toppings_price ====")
    user_input = input("Enter toppings as CSV (e.g. cheese,olives): ")
    result = toppings_price(user_input)
    print("Toppings Price:", result)

    print("\n==== Running pizza_inches ====")
    user_input = input("Enter pizza size (S/M/L): ")
    result = pizza_inches(user_input)
    print("Size in Inches:", result)

    print("\n==== Running split_bill ====")
    user_input = input("Enter total and people (e.g. 900/3): ")
    result = split_bill(user_input)
    print("Per Person:", result)

if __name__ == "__main__":
    main()
