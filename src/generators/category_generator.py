from src.utils.faker_utils import build_faker


CATEGORY_ROWS = [
    {"category_id": 1, "category_name": "Electronics", "parent_category_id": None, "level": 1},
    {"category_id": 2, "category_name": "Fashion", "parent_category_id": None, "level": 1},
    {"category_id": 3, "category_name": "Home & Living", "parent_category_id": None, "level": 1},
    {"category_id": 4, "category_name": "Beauty", "parent_category_id": None, "level": 1},
    {"category_id": 5, "category_name": "Mobile Phones", "parent_category_id": 1, "level": 2},
    {"category_id": 6, "category_name": "Laptops", "parent_category_id": 1, "level": 2},
    {"category_id": 7, "category_name": "Men Clothing", "parent_category_id": 2, "level": 2},
    {"category_id": 8, "category_name": "Women Clothing", "parent_category_id": 2, "level": 2},
    {"category_id": 9, "category_name": "Kitchen", "parent_category_id": 3, "level": 2},
    {"category_id": 10, "category_name": "Skincare", "parent_category_id": 4, "level": 2},
]


def generate_categories(row_count: int = 10) -> list[dict]:
    fake = build_faker()
    rows = []

    for category in CATEGORY_ROWS[:row_count]:
        rows.append(
            {
                **category,
                "created_at": fake.date_time_this_year(),
            }
        )

    return rows
