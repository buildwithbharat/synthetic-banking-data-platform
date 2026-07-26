def validate_not_null(
    validator,
    df,
    table_name,
):

    null_columns = []

    for column in df.columns:

        if df[column].isnull().sum() > 0:
            null_columns.append(column)

    if not null_columns:
        validator.success(
            f"{table_name} has no NULL values"
        )
    else:
        validator.failure(
            f"{table_name}: {', '.join(null_columns)}"
        )