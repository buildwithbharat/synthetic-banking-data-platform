"""
Synthetic Banking Dataset Validator
"""

import pandas as pd

from validators.reporter import Validator

from validators.primary_key import validate_primary_key
from validators.foreign_key import validate_foreign_key
from validators.not_null import validate_not_null

from validators.business_rules import (
    validate_branch_managers,
    validate_customer_accounts,
    validate_transactions_per_account,
    validate_cards,
    validate_loans,
)

from validators.date_rules import (
    validate_account_dates,
    validate_transaction_dates,
    validate_card_dates,
    validate_loan_dates,
)


def load_data():
    return {
        "customers": pd.read_csv("output/dirty/corrupted_customers.csv"),
    }


def main():
    validator = Validator()

    data = load_data()

    # branches = data["branches"]
    # employees = data["employees"]
    customers = data["customers"]
    # accounts = data["accounts"]
    # transactions = data["transactions"]
    # cards = data["cards"]
    # loans = data.get("loans")  # Fixed potential KeyError since loans isn't loaded in load_data()

    validator.section("PRIMARY KEY CHECKS")

    validate_primary_key(validator, customers, "customer_id")

    validator.section("NOT NULL CHECKS")

    validate_not_null(
        validator,
        customers,
        "customers",
    )
    
    validator.summary()


if __name__ == "__main__":
    main()