from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Engine

from src.db import TABLE_LOAD_ORDER, sync_serial_sequences


def load_csv_files(engine: Engine, output_dir: Path) -> None:
    for table_name in TABLE_LOAD_ORDER:
        csv_path = output_dir / f"{table_name}.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing CSV file: {csv_path}")

        dataframe = pd.read_csv(csv_path)
        dataframe = dataframe.where(pd.notna(dataframe), None)
        dataframe.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1_000,
        )
        print(f"Loaded {len(dataframe):,} rows into {table_name}")

    sync_serial_sequences(engine)
