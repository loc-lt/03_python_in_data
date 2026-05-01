from src.utils.faker_utils import build_faker


def generate_brands(row_count: int = 20) -> list[dict]:
    fake = build_faker()
    rows = []

    for brand_id in range(1, row_count + 1):
        brand_name = fake.unique.company()
        rows.append(
            {
                "brand_id": brand_id,
                "brand_name": brand_name,
                "country": fake.country(),
                "created_at": fake.date_time_this_decade(),
            }
        )

    fake.unique.clear()
    return rows
