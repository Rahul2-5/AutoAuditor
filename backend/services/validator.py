import pandas as pd

REQUIRED_COLUMNS = ["date", "amount", "category", "description"]

def validate_csv(df: pd.DataFrame):
    errors = []
    df_test = df.copy()

    # 1. Check missing columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df_test.columns]
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")
        return False, errors

    # 2. Check empty dataframe
    if df_test.empty:
        errors.append("CSV file is empty")
        return False, errors

    # 3. Check null values
    if df_test.isnull().values.any():
        null_info = df_test.isnull().sum()
        errors.append(f"CSV contains missing/null values: {null_info.to_dict()}")

    # 4. Check amount column type
    if "amount" in df_test.columns:
        try:
            test_amount = pd.to_numeric(df_test["amount"])
        except:
            errors.append("Amount column must be numeric")
            return False, errors

    # 5. Check negative values
    if "amount" in df_test.columns:
        if (pd.to_numeric(df_test["amount"], errors="coerce") < 0).any():
            errors.append("Amount cannot be negative")

    if errors:
        return False, errors

    return True, ["CSV is valid"]