import pandas as pd


def validate_account_dates(
    validator,
    accounts,
):

    today = pd.Timestamp.today().normalize()

    opening_dates = pd.to_datetime(
        accounts["opening_date"]
    )

    invalid = (opening_dates > today).sum()

    if invalid == 0:
        validator.success(
            "Account opening dates"
        )
    else:
        validator.failure(
            f"{invalid} future account opening dates"
        )


def validate_transaction_dates(
    validator,
    accounts,
    transactions,
):

    merged = transactions.merge(
        accounts[
            ["account_id", "opening_date"]
        ],
        on="account_id",
    )

    invalid = (
        pd.to_datetime(
            merged["transaction_timestamp"]
        )
        <
        pd.to_datetime(
            merged["opening_date"]
        )
    ).sum()

    if invalid == 0:
        validator.success(
            "Transaction dates"
        )
    else:
        validator.failure(
            f"{invalid} transactions before account opening"
        )


def validate_card_dates(
    validator,
    cards,
):

    invalid = (
        pd.to_datetime(cards["expiry_date"])
        <=
        pd.to_datetime(cards["issue_date"])
    ).sum()

    if invalid == 0:
        validator.success(
            "Card expiry dates"
        )
    else:
        validator.failure(
            f"{invalid} invalid card expiry dates"
        )


def validate_loan_dates(
    validator,
    accounts,
    loans,
):

    merged = loans.merge(
        accounts[
            ["account_id", "opening_date"]
        ],
        on="account_id",
    )

    invalid = (
        pd.to_datetime(
            merged["start_date"]
        )
        <
        pd.to_datetime(
            merged["opening_date"]
        )
    ).sum()

    if invalid == 0:
        validator.success(
            "Loan start dates"
        )
    else:
        validator.failure(
            f"{invalid} loans before account opening"
        )