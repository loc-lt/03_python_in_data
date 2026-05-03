import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine


VALIDATION_QUERIES = {
    "row_counts": """
        SELECT 'brand' AS table_name, COUNT(*) AS row_count FROM brand
        UNION ALL SELECT 'category', COUNT(*) FROM category
        UNION ALL SELECT 'seller', COUNT(*) FROM seller
        UNION ALL SELECT 'product', COUNT(*) FROM product
        UNION ALL SELECT 'promotion', COUNT(*) FROM promotion
        UNION ALL SELECT 'promotion_product', COUNT(*) FROM promotion_product
        ORDER BY table_name
    """,
    "invalid_product_foreign_keys": """
        SELECT COUNT(*) AS invalid_rows
        FROM product p
        LEFT JOIN brand b ON p.brand_id = b.brand_id
        LEFT JOIN category c ON p.category_id = c.category_id
        LEFT JOIN seller s ON p.seller_id = s.seller_id
        WHERE b.brand_id IS NULL
           OR c.category_id IS NULL
           OR s.seller_id IS NULL
    """,
    "invalid_discount_prices": """
        SELECT COUNT(*) AS invalid_rows
        FROM product
        WHERE discount_price > price
    """,
    "invalid_category_hierarchy": """
        SELECT COUNT(*) AS invalid_rows
        FROM category
        WHERE (level = 1 AND parent_category_id IS NOT NULL)
           OR (level = 2 AND parent_category_id IS NULL)
    """,
    "invalid_promotion_dates": """
        SELECT COUNT(*) AS invalid_rows
        FROM promotion
        WHERE end_date < start_date
    """,
    "duplicate_promotion_products": """
        SELECT COUNT(*) AS duplicate_pairs
        FROM (
            SELECT promotion_id, product_id, COUNT(*) AS pair_count
            FROM promotion_product
            GROUP BY promotion_id, product_id
            HAVING COUNT(*) > 1
        ) duplicates
    """,
}


def run_validations(engine: Engine) -> dict[str, pd.DataFrame]:
    results = {}
    with engine.connect() as connection:
        for name, query in VALIDATION_QUERIES.items():
            results[name] = pd.read_sql(text(query), connection)
    return results


def print_validation_results(results: dict[str, pd.DataFrame]) -> None:
    for name, dataframe in results.items():
        print(f"\n{name}")
        if dataframe.empty:
            print("(no rows)")
            continue

        print(dataframe.to_string(index=False))
