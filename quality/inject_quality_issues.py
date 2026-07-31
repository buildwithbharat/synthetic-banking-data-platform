"""
Quality Issue Injector

Reads a clean dataset, injects quality issues, and writes the corrupted dataset.

Supports:
- CSV
- Parquet
"""

from pathlib import Path

import numpy as np
import pandas as pd


NULL_RATE = 0.08
DUPLICATE_RATE = 0.05
OUTLIER_RATE = 0.05
TEXT_CORRUPTION_RATE = 0.10


def read_dataset(input_file):
    extension = Path(input_file).suffix.lower()

    if extension == ".csv":
        return pd.read_csv(input_file)

    if extension == ".parquet":
        return pd.read_parquet(input_file)

    raise ValueError(f"Unsupported file format: {extension}")


def write_dataset(dataframe, output_file):
    extension = Path(output_file).suffix.lower()

    if extension == ".csv":
        dataframe.to_csv(output_file, index=False)

    elif extension == ".parquet":
        dataframe.to_parquet(output_file, index=False)

    else:
        raise ValueError(f"Unsupported file format: {extension}")


def is_key_column(column_name):
    """
    Primary keys / foreign keys should never be corrupted.
    """

    column = column_name.lower()

    return (
        column == "id"
        or column.endswith("_id")
        or column.startswith("id_")
    )


def is_datetime_column(column_name):
    """
    Detect date/time columns by name.
    """

    column = column_name.lower()

    keywords = [
        "date",
        "time",
        "timestamp",
        "created_at",
        "updated_at",
    ]

    return any(keyword in column for keyword in keywords)


def inject_quality_issues(
    input_file,
    output_file,
    null_rate=NULL_RATE,
    duplicate_rate=DUPLICATE_RATE,
):
    df = read_dataset(input_file)

    # ---------------------------------------------------------
    # Inject Missing Values
    # ---------------------------------------------------------

    for column in df.columns:

        if is_key_column(column):
            continue

        mask = np.random.rand(len(df)) < null_rate

        df.loc[mask, column] = np.nan

    # ---------------------------------------------------------
    # Inject Duplicate Rows
    # ---------------------------------------------------------

    if len(df) > 0:

        duplicates = df.sample(
            frac=duplicate_rate,
            replace=True,
        )

        df = pd.concat(
            [df, duplicates],
            ignore_index=True,
        )

    # ---------------------------------------------------------
    # Inject Numeric Outliers
    # ---------------------------------------------------------

    numeric_columns = df.select_dtypes(include=[np.number]).columns

    for column in numeric_columns:

        if is_key_column(column):
            continue

        mask = np.random.rand(len(df)) < OUTLIER_RATE

        df.loc[mask, column] *= 100

    # ---------------------------------------------------------
    # Inject Text Formatting Issues
    # ---------------------------------------------------------

    for column in df.columns:

        if is_key_column(column):
            continue

        if is_datetime_column(column):
            continue

        if not pd.api.types.is_string_dtype(df[column]):
            continue

        mask = np.random.rand(len(df)) < TEXT_CORRUPTION_RATE

        df.loc[mask, column] = (
            df.loc[mask, column]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.upper()
        )

    write_dataset(df, output_file)

    print(f"✓ Corrupted dataset saved to {output_file}")


if __name__ == "__main__":

    input_path = "output/clean/medium_dataset/accounts.parquet"
    output_path = "output/dirty/medium_dataset/dirty_accounts.parquet"

    inject_quality_issues(input_path,output_path)