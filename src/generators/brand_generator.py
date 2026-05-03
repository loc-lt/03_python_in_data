import pandas as pd

from src.utils.faker_utils import build_faker


def generate_brands(row_count: int = 20) -> pd.DataFrame:
    fake = build_faker()
    data = {
        "brand_id": [brand_id for brand_id in range(1, row_count + 1)],
        "brand_name": [fake.unique.company() for _ in range(row_count)],
        "country": [fake.country() for _ in range(row_count)],
        "created_at": [fake.date_time_this_decade() for _ in range(row_count)],
    }

    fake.unique.clear()
    return pd.DataFrame(data)
