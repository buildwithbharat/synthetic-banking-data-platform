import pandas as pd
import numpy as np

def inject_quality_issues(input_file, output_file, null_rate=0.08, dupe_rate=0.05):
    # Load dataset from custom path
    df = pd.read_csv(input_file)
    
    # 1. Inject missing values (NaN)
    for col in df.columns:
        mask = np.random.rand(len(df)) < null_rate
        df.loc[mask, col] = np.nan
        
    # 2. Inject duplicate rows
    if len(df) > 0:
        dupes = df.sample(frac=dupe_rate, replace=True)
        df = pd.concat([df, dupes], ignore_index=True)
        
    # 3. Inject extreme numeric outliers (multiply numeric columns by 100)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        mask = np.random.rand(len(df)) < 0.05
        df.loc[mask, col] = df.loc[mask, col] * 100

    # 4. Inject random whitespace/casing inconsistencies in text columns
    text_cols = df.select_dtypes(include=[object]).columns
    for col in text_cols:
        mask = np.random.rand(len(df)) < 0.10
        df.loc[mask, col] = df.loc[mask, col].astype(str).str.strip().str.upper()

    # Save result to custom output path
    df.to_csv(output_file, index=False)
    print(f"Saved heavily corrupted data to {output_file}")

if __name__ == "__main__":
    input_path = "C:\\Users\\asus\\Documents\\GitHub\\synthetic-banking-data-platform\\output\\clean\\small_dataset\\customers.csv"
    output_path = "C:\\Users\\asus\\Documents\\GitHub\\synthetic-banking-data-platform\\output\\dirty\\corrupted_customers.csv"

    inject_quality_issues(input_path, output_path)