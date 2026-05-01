from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.config import DATABASE_URL


TABLE_LOAD_ORDER = [
    "brand",
    "category",
    "seller",
    "product",
    "promotion",
    "promotion_product",
]

TABLE_DROP_ORDER = [
    "order_item",
    "orders",
    "promotion_product",
    "promotion",
    "product",
    "seller",
    "category",
    "brand",
]


def get_engine() -> Engine:
    return create_engine(DATABASE_URL)


def reset_database(engine: Engine) -> None:
    with engine.begin() as connection:
        for table_name in TABLE_DROP_ORDER:
            connection.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))


def run_schema(engine: Engine, schema_path: Path) -> None:
    schema_sql = schema_path.read_text(encoding="utf-8")
    with engine.begin() as connection:
        for statement in schema_sql.split(";"):
            if statement.strip():
                connection.execute(text(statement))


def sync_serial_sequences(engine: Engine) -> None:
    sequence_statements = [
        ("brand", "brand_id"),
        ("category", "category_id"),
        ("seller", "seller_id"),
        ("product", "product_id"),
        ("promotion", "promotion_id"),
        ("promotion_product", "promo_product_id"),
    ]

    with engine.begin() as connection:
        for table_name, id_column in sequence_statements:
            connection.execute(
                text(
                    """
                    SELECT setval(
                        pg_get_serial_sequence(:table_name, :id_column),
                        COALESCE((SELECT MAX(id_value) FROM (
                            SELECT {id_column} AS id_value FROM {table_name}
                        ) ids), 1),
                        true
                    )
                    """.format(table_name=table_name, id_column=id_column)
                ),
                {"table_name": table_name, "id_column": id_column},
            )
