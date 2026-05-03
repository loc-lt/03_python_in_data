import numpy as np
import pandas as pd

from src.utils.faker_utils import build_faker


SELLER_TYPES = ["Official", "Marketplace"]


def generate_sellers(row_count: int = 25) -> pd.DataFrame:
    fake = build_faker()
    data = {
        "seller_id": [seller_id for seller_id in range(1, row_count + 1)],
        "seller_name": [f"{fake.company()} VN" for _ in range(row_count)],
        "join_date": [fake.date_between(start_date="-5y", end_date="today") for _ in range(row_count)],
        "seller_type": np.random.choice(SELLER_TYPES, size=row_count, p=[0.3, 0.7]),
        "rating": np.round(np.random.uniform(3.0, 5.0, size=row_count), 1),
        "country": ["Vietnam" for _ in range(row_count)],
    }

    return pd.DataFrame(data)
