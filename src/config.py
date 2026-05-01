from pathlib import Path

import os

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs) -> bool:
        return False


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
SCHEMA_PATH = BASE_DIR / "src" / "schema.sql"

load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ecommerce_project03")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

ROW_COUNTS = {
    "brand": 20,
    "category": 10,
    "seller": 25,
    "product": 2_000,
    "promotion": 10,
    "promotion_product": 100,
}

RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))
