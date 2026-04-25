def normalize_columns(columns):
    return [col.strip().lower() for col in columns]

# Normalize column names
def normalize_columns(columns):
    return [col.strip().lower() for col in columns]


# Column aliases (dynamic mapping)
COLUMN_ALIASES = {
    "date": ["date", "transaction_date", "dt"],
    "employee": ["employee", "emp", "user", "name"],
    "amount": ["amount", "amt", "price", "value"],
    "category": ["category", "type"],
    "vendor": ["vendor", "merchant", "shop"],
    "description": ["description", "desc", "details"]
}


# Map incoming columns → standard schema
def map_columns(df):
    col_map = {}
    normalized_cols = {col.lower(): col for col in df.columns}

    for standard_col, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in normalized_cols:
                col_map[standard_col] = normalized_cols[alias]
                break

    return col_map


# Standardize dataframe
def standardize_dataframe(df):
    col_map = map_columns(df)

    required = ["date", "employee", "amount", "category", "vendor", "description"]
    missing = [col for col in required if col not in col_map]

    if missing:
        return None, f"Missing required fields: {missing}"

    new_df = df.rename(columns={
        col_map["date"]: "date",
        col_map["employee"]: "employee",
        col_map["amount"]: "amount",
        col_map["category"]: "category",
        col_map["vendor"]: "vendor",
        col_map["description"]: "description"
    })

    return new_df, None