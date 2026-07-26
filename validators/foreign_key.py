def validate_foreign_key(
    validator,
    child_df,
    child_column,
    parent_df,
    parent_column,
    relationship,
):

    invalid = ~child_df[child_column].isin(
        parent_df[parent_column]
    )

    if invalid.sum() == 0:
        validator.success(relationship)
    else:
        validator.failure(
            f"{relationship} ({invalid.sum()} invalid references)"
        )