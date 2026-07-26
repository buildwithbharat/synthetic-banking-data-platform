import pandas as pd


def validate_branch_managers(validator, employees):

    managers = employees[
        employees["designation"] == "Branch Manager"
    ]

    counts = managers.groupby("branch_id").size()

    invalid = counts[counts != 1]

    if invalid.empty:
        validator.success(
            "Exactly one Branch Manager per branch"
        )
    else:
        validator.failure(
            f"{len(invalid)} branches have incorrect manager count"
        )


def validate_customer_accounts(
    validator,
    customers,
    accounts,
):

    missing = customers[
        ~customers["customer_id"].isin(
            accounts["customer_id"]
        )
    ]

    if missing.empty:
        validator.success(
            "Every customer has at least one account"
        )
    else:
        validator.failure(
            f"{len(missing)} customers have no account"
        )


def validate_transactions_per_account(
    validator,
    transactions,
):

    counts = transactions.groupby("account_id").size()

    invalid = counts[counts < 5]

    if invalid.empty:
        validator.success(
            "Minimum 5 transactions per account"
        )
    else:
        validator.failure(
            f"{len(invalid)} accounts have fewer than 5 transactions"
        )


def validate_cards(
    validator,
    cards,
):

    duplicates = (
        cards.groupby(
            ["account_id", "card_type"]
        )
        .size()
        .reset_index(name="count")
    )

    invalid = duplicates[
        duplicates["count"] > 1
    ]

    if invalid.empty:
        validator.success(
            "Maximum one Debit and one Credit card per account"
        )
    else:
        validator.failure(
            f"{len(invalid)} duplicate card assignments"
        )


def validate_loans(
    validator,
    loans,
):

    duplicates = (
        loans.groupby(
            ["customer_id", "loan_type"]
        )
        .size()
        .reset_index(name="count")
    )

    invalid = duplicates[
        duplicates["count"] > 1
    ]

    if invalid.empty:
        validator.success(
            "Loan types unique per customer"
        )
    else:
        validator.failure(
            f"{len(invalid)} duplicate loan types"
        )