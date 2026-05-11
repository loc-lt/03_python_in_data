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
├── pyproject.toml
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

## Setup (Poetry)

Install dependencies with Poetry:

```bash
poetry install
```

This installs both generation and PostgreSQL loading dependencies.

Update `.env` if your PostgreSQL username or password is different:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_project03
DB_USER=postgres
DB_PASSWORD=postgres
RANDOM_SEED=42
```

When you run with `--load`, the script will connect to the default `postgres` database first and create `ecommerce_project03` automatically if it does not exist.

## Usage

Generate CSV files only:

```bash
poetry run python -m src.main
```

Generate CSV files, recreate PostgreSQL tables, load data, and run validations:

```bash
poetry run python -m src.main --load --reset-db
```

Reuse existing CSV files and load them into PostgreSQL:

```bash
poetry run python -m src.main --skip-generate --load --reset-db
```

## Troubleshooting PostgreSQL (`Connection refused`)

If `--load` fails with `connection to server at "localhost" ... port 5432 failed: Connection refused`, nothing is accepting TCP connections on that host/port. The Python script is fine; PostgreSQL must be running and listening.

**Windows**

1. Start the service (name varies by installer), e.g. in **PowerShell (Admin)**:
   - `Get-Service *postgres*`
   - `Start-Service postgresql-x64-16` (replace with your service name)
2. Or open **Services** (`services.msc`), find **postgresql**, set **Startup type** to Automatic, click **Start**.
3. Confirm the port in `postgresql.conf` is `5432` (or set `DB_PORT` in `.env` to match).
4. If you use **Docker**, PostgreSQL may be on another port (e.g. `5433`); set `DB_HOST` / `DB_PORT` in `.env` accordingly.

Quick port check (PowerShell): `Test-NetConnection -ComputerName 127.0.0.1 -Port 5432` — `TcpTestSucceeded` should be `True` before rerunning `poetry run python -m src.main --load --reset-db`.

## Validation Checks

After loading, the script prints:

- row count for each generated table
- invalid product foreign keys
- invalid discount prices
- invalid category hierarchy
- invalid promotion date ranges
- duplicate promotion-product mappings

All invalid checks should return `0`.
