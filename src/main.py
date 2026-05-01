import argparse
import csv

from src.config import OUTPUT_DIR, ROW_COUNTS, SCHEMA_PATH
from src.generators.brand_generator import generate_brands
from src.generators.category_generator import generate_categories
from src.generators.product_generator import generate_products
from src.generators.promotion_generator import generate_promotions
from src.generators.promotion_product_generator import generate_promotion_products
from src.generators.seller_generator import generate_sellers
from src.utils.faker_utils import ensure_directory, seed_everything


def export_rows(rows: list[dict], table_name: str) -> None:
    csv_path = OUTPUT_DIR / f"{table_name}.csv"
    if not rows:
        raise ValueError(f"No rows generated for {table_name}")

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows):,} rows: {csv_path}")


def generate_all_csv_files() -> None:
    seed_everything()
    ensure_directory(OUTPUT_DIR)

    brands = generate_brands(ROW_COUNTS["brand"])
    categories = generate_categories(ROW_COUNTS["category"])
    sellers = generate_sellers(ROW_COUNTS["seller"])
    products = generate_products(brands, categories, sellers, ROW_COUNTS["product"])
    promotions = generate_promotions(ROW_COUNTS["promotion"])
    promotion_products = generate_promotion_products(
        promotions,
        products,
        ROW_COUNTS["promotion_product"],
    )

    export_rows(brands, "brand")
    export_rows(categories, "category")
    export_rows(sellers, "seller")
    export_rows(products, "product")
    export_rows(promotions, "promotion")
    export_rows(promotion_products, "promotion_product")


def load_to_database(reset_db: bool = False) -> None:
    from src.db import get_engine, reset_database, run_schema
    from src.loaders.insert_data import load_csv_files
    from src.utils.validators import print_validation_results, run_validations

    engine = get_engine()

    if reset_db:
        reset_database(engine)

    run_schema(engine, SCHEMA_PATH)
    load_csv_files(engine, OUTPUT_DIR)
    print_validation_results(run_validations(engine))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate and load Project 03 ecommerce data.")
    parser.add_argument(
        "--skip-generate",
        action="store_true",
        help="Skip CSV generation and reuse existing files in output/.",
    )
    parser.add_argument(
        "--load",
        action="store_true",
        help="Create schema and load generated CSV files into PostgreSQL.",
    )
    parser.add_argument(
        "--reset-db",
        action="store_true",
        help="Drop and recreate project tables before loading data.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.skip_generate:
        generate_all_csv_files()

    if args.load:
        load_to_database(reset_db=args.reset_db)


if __name__ == "__main__":
    main()
