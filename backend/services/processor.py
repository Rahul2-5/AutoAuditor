import pandas as pd

def clean_data(df: pd.DataFrame):
    df = df.copy()

    # 1. Remove duplicates
    df = df.drop_duplicates()

    # 2. Trim column names (important)
    df.columns = df.columns.str.strip().str.lower()

    # 3. Handle missing values
    df = df.dropna()

    # 4. Convert amount to numeric safely
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Remove rows where conversion failed
    df = df.dropna(subset=["amount"])

    # 5. Standardize categories
    df["category"] = df["category"].str.lower().str.strip()

    # 6. Convert date format
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop invalid dates
    df = df.dropna(subset=["date"])

    # 7. Reset index
    df = df.reset_index(drop=True)

    return df