import random

from src.utils.faker_utils import build_faker


SELLER_TYPES = ["Official", "Marketplace"]


def generate_sellers(row_count: int = 25) -> list[dict]:
    fake = build_faker()
    rows = []

    for seller_id in range(1, row_count + 1):
        rows.append(
            {
                "seller_id": seller_id,
                "seller_name": f"{fake.company()} VN",
                "join_date": fake.date_between(start_date="-5y", end_date="today"),
                "seller_type": random.choices(SELLER_TYPES, weights=[0.3, 0.7], k=1)[0],
                "rating": round(random.uniform(3.0, 5.0), 1),
                "country": "Vietnam",
            }
        )

    return rows
