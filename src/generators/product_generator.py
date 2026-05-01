import random

from src.utils.faker_utils import build_faker


CATEGORY_PRICE_RANGES = {
    "Electronics": (1_000_000, 30_000_000),
    "Fashion": (100_000, 3_000_000),
    "Home & Living": (150_000, 8_000_000),
    "Beauty": (50_000, 2_000_000),
    "Mobile Phones": (3_000_000, 50_000_000),
    "Laptops": (7_000_000, 60_000_000),
    "Men Clothing": (120_000, 4_000_000),
    "Women Clothing": (120_000, 4_000_000),
    "Kitchen": (100_000, 10_000_000),
    "Skincare": (80_000, 2_500_000),
}

def _money(value: float) -> float:
    return round(value, 2)


def generate_products(
    brands: list[dict],
    categories: list[dict],
    sellers: list[dict],
    row_count: int = 2_000,
) -> list[dict]:
    fake = build_faker()
    rows = []

    category_records = [
        {"category_id": row["category_id"], "category_name": row["category_name"]} for row in categories
    ]
    brand_ids = [row["brand_id"] for row in brands]
    seller_ids = [row["seller_id"] for row in sellers]

    for product_id in range(1, row_count + 1):
        category = random.choice(category_records)
        category_name = category["category_name"]
        min_price, max_price = CATEGORY_PRICE_RANGES[category_name]
        price = _money(random.uniform(min_price, max_price))
        discount_price = _money(price * random.uniform(0.7, 1.0))

        rows.append(
            {
                "product_id": product_id,
                "product_name": fake.catch_phrase(),
                "category_id": category["category_id"],
                "brand_id": random.choice(brand_ids),
                "seller_id": random.choice(seller_ids),
                "price": price,
                "discount_price": discount_price,
                "stock_qty": random.randint(0, 500),
                "rating": round(random.uniform(3.0, 5.0), 1),
                "created_at": fake.date_time_between(start_date="-3y", end_date="now"),
                "is_active": random.choices([True, False], weights=[0.9, 0.1], k=1)[0],
            }
        )

    return rows
