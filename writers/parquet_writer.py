import pandas as pd


def write_parquet(df: pd.DataFrame, output_path: str) -> None:
    """
    Writes a DataFrame to a Parquet file.
    """
    df.to_parquet(output_path, index=False)