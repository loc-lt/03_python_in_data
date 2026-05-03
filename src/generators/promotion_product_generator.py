import random

import pandas as pd

from src.utils.faker_utils import build_faker


def generate_promotion_products(
    promotions: pd.DataFrame,
    products: pd.DataFrame,
    row_count: int = 100,
) -> pd.DataFrame:
    fake = build_faker()
    promotion_ids = promotions["promotion_id"].to_list()
    product_ids = products["product_id"].to_list()
    max_unique_pairs = len(promotion_ids) * len(product_ids)

    if row_count > max_unique_pairs:
        raise ValueError(f"Cannot create {row_count} unique promotion-product pairs")

    pairs: set[tuple[int, int]] = set()
    while len(pairs) < row_count:
        pairs.add((random.choice(promotion_ids), random.choice(product_ids)))

    rows = [
        {
            "promo_product_id": promo_product_id,
            "promotion_id": promotion_id,
            "product_id": product_id,
            "created_at": fake.date_time_this_year(),
        }
        for promo_product_id, (promotion_id, product_id) in enumerate(sorted(pairs), start=1)
    ]

    return pd.DataFrame(rows)
