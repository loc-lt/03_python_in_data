# Project 03 - Python In Data

Generate synthetic data for an E-commerce OLTP system using Python, Faker, pandas, and numpy. The pipeline exports data to CSV and can optionally load it into PostgreSQL.

## Project Structure

```text
project03/
├── src/
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   ├── schema.sql
│   ├── generators/
│   ├── loaders/
│   └── utils/
├── output/
├── requirements.txt
├── .env
└── README.md
```

## Data Volume

The default generator creates:

| Table | Rows |
| --- | ---: |
| brand | 20 |
| category | 10 |
| seller | 25 |
| product | 2,000 |
| promotion | 10 |
| promotion_product | 100 |

`orders` and `order_item` are included in `src/schema.sql`, but this project does not generate their very large datasets yet because the assignment notes that they belong to the next SQL project.

## Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you also want to load data into PostgreSQL, install the database dependencies:

```bash
pip install -r requirements-db.txt
```

Create PostgreSQL database:

```sql
CREATE DATABASE ecommerce_project03;
```

Update `.env` if your PostgreSQL username or password is different:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_project03
DB_USER=postgres
DB_PASSWORD=postgres
RANDOM_SEED=42
```

## Usage

Generate CSV files only:

```bash
python3 -m src.main
```

Generate CSV files, recreate PostgreSQL tables, load data, and run validations:

```bash
python3 -m src.main --load --reset-db
```

Reuse existing CSV files and load them into PostgreSQL:

```bash
python3 -m src.main --skip-generate --load --reset-db
```

## Validation Checks

After loading, the script prints:

- row count for each generated table
- invalid product foreign keys
- invalid discount prices
- invalid category hierarchy
- invalid promotion date ranges
- duplicate promotion-product mappings

All invalid checks should return `0`.
