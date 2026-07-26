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
        "branches": pd.read_csv("output/clean/branches.csv"),
        "employees": pd.read_csv("output/clean/employees.csv"),
        "customers": pd.read_csv("output/clean/customers.csv"),
        "accounts": pd.read_csv("output/clean/accounts.csv"),
        "transactions": pd.read_csv("output/clean/transactions.csv"),
        "cards": pd.read_csv("output/clean/cards.csv"),
        "loans": pd.read_csv("output/clean/loans.csv"),
    }


def main():

    validator = Validator()

    data = load_data()

    branches = data["branches"]
    employees = data["employees"]
    customers = data["customers"]
    accounts = data["accounts"]
    transactions = data["transactions"]
    cards = data["cards"]
    loans = data["loans"]

    validator.section("PRIMARY KEY CHECKS")

    validate_primary_key(validator, branches, "branch_id")
    validate_primary_key(validator, employees, "employee_id")
    validate_primary_key(validator, customers, "customer_id")
    validate_primary_key(validator, accounts, "account_id")
    validate_primary_key(validator, transactions, "transaction_id")
    validate_primary_key(validator, cards, "card_id")
    validate_primary_key(validator, loans, "loan_id")

    validator.section("FOREIGN KEY CHECKS")

    validate_foreign_key(
        validator,
        employees,
        "branch_id",
        branches,
        "branch_id",
        "employees.branch_id → branches.branch_id",
    )

    validate_foreign_key(
        validator,
        accounts,
        "customer_id",
        customers,
        "customer_id",
        "accounts.customer_id → customers.customer_id",
    )

    validate_foreign_key(
        validator,
        accounts,
        "branch_id",
        branches,
        "branch_id",
        "accounts.branch_id → branches.branch_id",
    )

    validate_foreign_key(
        validator,
        transactions,
        "account_id",
        accounts,
        "account_id",
        "transactions.account_id → accounts.account_id",
    )

    validate_foreign_key(
        validator,
        cards,
        "account_id",
        accounts,
        "account_id",
        "cards.account_id → accounts.account_id",
    )

    validate_foreign_key(
        validator,
        loans,
        "customer_id",
        customers,
        "customer_id",
        "loans.customer_id → customers.customer_id",
    )

    validate_foreign_key(
        validator,
        loans,
        "account_id",
        accounts,
        "account_id",
        "loans.account_id → accounts.account_id",
    )

    validator.section("NOT NULL CHECKS")

    validate_not_null(
        validator,
        branches,
        "branches",
    )

    validate_not_null(
        validator,
        employees,
        "employees",
    )

    validate_not_null(
        validator,
        customers,
        "customers",
    )

    validate_not_null(
        validator,
        accounts,
        "accounts",
    )

    validate_not_null(
        validator,
        transactions,
        "transactions",
    )

    validate_not_null(
        validator,
        cards,
        "cards",
    )

    validate_not_null(
        validator,
        loans,
        "loans",
    )

    validator.section("BUSINESS RULES")

    validate_branch_managers(
        validator,
        employees,
    )

    validate_customer_accounts(
        validator,
        customers,
        accounts,
    )

    validate_transactions_per_account(
        validator,
        transactions,
    )

    validate_cards(
        validator,
        cards,
    )

    validate_loans(
        validator,
        loans,
    )

    validator.section("DATE VALIDATIONS")

    validate_account_dates(
        validator,
        accounts,
    )

    validate_transaction_dates(
        validator,
        accounts,
        transactions,
    )

    validate_card_dates(
        validator,
        cards,
    )

    validate_loan_dates(
        validator,
        accounts,
        loans,
    )

    validator.summary()


if __name__ == "__main__":
    main()