from datetime import timedelta

import numpy as np
import pandas as pd

from src.utils.faker_utils import build_faker


PROMOTION_NAMES = [
    "9.9 Mega Sale",
    "10.10 Brand Festival",
    "11.11 Super Sale",
    "12.12 Year End Sale",
    "Black Friday",
    "New Year Deal",
    "Summer Flash Sale",
    "Payday Sale",
    "Back To School",
    "Weekend Voucher Day",
]

PROMOTION_TYPES = ["product", "category", "seller", "flash_sale"]
DISCOUNT_TYPES = ["percentage", "fixed_amount"]


def generate_promotions(row_count: int = 10) -> pd.DataFrame:
    fake = build_faker()
    rows = []

    for promotion_id in range(1, row_count + 1):
        discount_type = fake.random_element(elements=DISCOUNT_TYPES)
        if discount_type == "percentage":
            discount_value = round(np.random.uniform(5, 50), 2)
        else:
            discount_value = fake.random_element(
                elements=[10_000, 20_000, 50_000, 100_000, 200_000, 500_000]
            )

        start_date = fake.date_between(start_date="-1y", end_date="+6m")
        end_date = start_date + timedelta(days=fake.random_int(min=30, max=50))

        rows.append(
            {
                "promotion_id": promotion_id,
                "promotion_name": PROMOTION_NAMES[(promotion_id - 1) % len(PROMOTION_NAMES)],
                "promotion_type": fake.random_element(elements=PROMOTION_TYPES),
                "discount_type": discount_type,
                "discount_value": discount_value,
                "start_date": start_date,
                "end_date": end_date,
            }
        )

    return pd.DataFrame(rows)
