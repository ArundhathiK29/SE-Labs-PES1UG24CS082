SIZE_PRICE = {"small": 200, "medium": 350, "large": 500}


def pizza_price(size, toppings, is_cheese_burst):
    if size not in SIZE_PRICE:
        raise ValueError("unknown size")
    if toppings < 0:
        raise ValueError("invalid toppings")
    price = SIZE_PRICE[size]
    if toppings > 3:
        price += 3 * 40 + (toppings - 3) * 30
    else:
        price += toppings * 40
    if is_cheese_burst:
        if size == "small":
            raise ValueError("cheese burst not available for small")
        price += 100
    return price


def order_discount(order_total, day, is_student):
    if order_total < 300:
        return 0
    if day == "tuesday":
        discount = order_total // 2
    elif day in ("saturday", "sunday"):
        discount = 0
    else:
        discount = order_total // 10
    if is_student:
        discount += 50
    return discount


def delivery_status(minutes_taken, distance_km):
    if distance_km > 10:
        return "not deliverable"
    if minutes_taken <= 30:
        return "on time"
    elif minutes_taken <= 45:
        return "late"
    return "free pizza"
