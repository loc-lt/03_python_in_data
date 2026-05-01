import csv
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.db import TABLE_LOAD_ORDER, sync_serial_sequences


INTEGER_COLUMNS = {
    "brand": ["brand_id"],
    "category": ["category_id", "parent_category_id", "level"],
    "seller": ["seller_id"],
    "product": ["product_id", "category_id", "brand_id", "seller_id", "stock_qty"],
    "promotion": ["promotion_id"],
    "promotion_product": ["promo_product_id", "promotion_id", "product_id"],
}

FLOAT_COLUMNS = {
    "seller": ["rating"],
    "product": ["price", "discount_price", "rating"],
    "promotion": ["discount_value"],
}

BOOLEAN_COLUMNS = {
    "product": ["is_active"],
}


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes"}


def _prepare_rows(table_name: str, csv_path: Path) -> list[dict]:
    with csv_path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    for row in rows:
        for column, value in row.items():
            if value == "":
                row[column] = None

        for column in INTEGER_COLUMNS.get(table_name, []):
            if row.get(column) is not None:
                row[column] = int(float(row[column]))

        for column in FLOAT_COLUMNS.get(table_name, []):
            if row.get(column) is not None:
                row[column] = float(row[column])

        for column in BOOLEAN_COLUMNS.get(table_name, []):
            if row.get(column) is not None:
                row[column] = _to_bool(row[column])

    return rows


def _insert_rows(engine: Engine, table_name: str, rows: list[dict]) -> None:
    if not rows:
        return

    columns = list(rows[0].keys())
    column_names = ", ".join(columns)
    placeholders = ", ".join(f":{column}" for column in columns)
    statement = text(f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})")

    with engine.begin() as connection:
        connection.execute(statement, rows)


def load_csv_files(engine: Engine, output_dir: Path) -> None:
    for table_name in TABLE_LOAD_ORDER:
        csv_path = output_dir / f"{table_name}.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing CSV file: {csv_path}")

        rows = _prepare_rows(table_name, csv_path)
        _insert_rows(engine, table_name, rows)
        print(f"Loaded {len(rows):,} rows into {table_name}")

    sync_serial_sequences(engine)
