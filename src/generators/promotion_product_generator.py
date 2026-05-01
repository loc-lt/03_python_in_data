import random

from src.utils.faker_utils import build_faker


def generate_promotion_products(
    promotions: list[dict],
    products: list[dict],
    row_count: int = 100,
) -> list[dict]:
    fake = build_faker()
    promotion_ids = [row["promotion_id"] for row in promotions]
    product_ids = [row["product_id"] for row in products]
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

    return rows
