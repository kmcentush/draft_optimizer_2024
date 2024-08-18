import os.path
from pathlib import Path

import polars as pl

# Specify directories
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))

# Maybe make directories
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)


def file_exists(file: str) -> bool:
    return os.path.isfile(os.path.join(DATA_DIR, file))


def write_parquet(df: pl.DataFrame, file: str):
    df.write_parquet(os.path.join(DATA_DIR, file))


def read_parquet(file: str) -> pl.DataFrame:
    return pl.read_parquet(os.path.join(DATA_DIR, file))
