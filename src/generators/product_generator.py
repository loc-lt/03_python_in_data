import numpy as np
import pandas as pd

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
    brands: pd.DataFrame,
    categories: pd.DataFrame,
    sellers: pd.DataFrame,
    row_count: int = 2_000,
) -> pd.DataFrame:
    fake = build_faker()
    rows = []

    category_records = categories[["category_id", "category_name"]].to_dict("records")
    brand_ids = brands["brand_id"].to_list()
    seller_ids = sellers["seller_id"].to_list()

    for product_id in range(1, row_count + 1):
        category = fake.random_element(elements=category_records)
        category_name = category["category_name"]
        min_price, max_price = CATEGORY_PRICE_RANGES[category_name]
        price = _money(np.random.uniform(min_price, max_price))
        discount_price = _money(price * np.random.uniform(0.7, 1.0))

        rows.append(
            {
                "product_id": product_id,
                "product_name": fake.catch_phrase(),
                "category_id": category["category_id"],
                "brand_id": fake.random_element(elements=brand_ids),
                "seller_id": fake.random_element(elements=seller_ids),
                "price": price,
                "discount_price": discount_price,
                "stock_qty": fake.random_int(min=0, max=500),
                "rating": round(np.random.uniform(3.0, 5.0), 1),
                "created_at": fake.date_time_between(start_date="-3y", end_date="now"),
                "is_active": bool(np.random.choice([True, False], p=[0.9, 0.1])),
            }
        )

    return pd.DataFrame(rows)
