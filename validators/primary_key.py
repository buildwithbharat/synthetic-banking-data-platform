def validate_primary_key(
    validator,
    df,
    column,
):

    if df[column].isnull().any():
        validator.failure(f"{column} contains NULL values")
        return

    duplicates = df[column].duplicated().sum()

    if duplicates == 0:
        validator.success(column)
    else:
        validator.failure(
            f"{column} has {duplicates} duplicate values"
        )