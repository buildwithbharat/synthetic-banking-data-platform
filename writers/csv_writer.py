import pandas as pd


def write_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    Writes a DataFrame to a CSV file.
    """
    df.to_csv(output_path, index=False)