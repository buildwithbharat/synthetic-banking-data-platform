"""
Transaction Generator

Business Rules:
- Every transaction belongs to one account.
- Transaction date cannot be before account opening.
- Every account gets at least 5 transactions.
"""

import random

import pandas as pd

TRANSACTION_MODES = {
    "UPI": (10, 10000),
    "ATM": (100, 20000),
    "POS": (50, 50000),
    "NEFT": (500, 200000),
    "RTGS": (200000, 1000000),
    "IMPS": (100, 100000),
    "Cash": (100, 50000),
}

MERCHANT_CATEGORIES = [
    "Shopping",
    "Food",
    "Fuel",
    "Bills",
    "Travel",
    "Healthcare",
    "Entertainment",
    "Salary",
    "Transfer",
    "Cash Withdrawal",
]


def random_transaction_timestamp(opening_date, current_time):
    """
    Generate a random timestamp between account opening
    and the current time.
    """

    start = pd.Timestamp(opening_date)

    start_seconds = int(start.timestamp())
    end_seconds = int(current_time.timestamp())

    random_seconds = random.randint(start_seconds, end_seconds)

    return pd.Timestamp(random_seconds, unit="s")


def build_transaction(account, transaction_id, current_time):

    mode = random.choices(
        list(TRANSACTION_MODES.keys()),
        weights=[45, 10, 15, 10, 2, 13, 5],
        k=1,
    )[0]

    return {
        "transaction_id": f"TXN{transaction_id:010d}",
        "account_id": account["account_id"],
        "transaction_timestamp": random_transaction_timestamp(
            account["opening_date"],
            current_time,
        ),
        "transaction_type": random.choice(
            ["Credit", "Debit"]
        ),
        "transaction_mode": mode,
        "amount": random.randint(
            *TRANSACTION_MODES[mode]
        ),
        "merchant_category": random.choice(
            MERCHANT_CATEGORIES
        ),
        "transaction_status": random.choices(
            ["Success", "Failed", "Reversed"],
            weights=[98, 1, 1],
            k=1,
        )[0],
    }


def generate_transactions(config, accounts):

    total_transactions = config["dataset"]["transactions"]

    transactions = []

    transaction_id = 1

    current_time = pd.Timestamp.now()

    account_records = accounts.to_dict("records")

    # Every account gets at least 5 transactions
    for account in account_records:

        for _ in range(5):

            transactions.append(
                build_transaction(
                    account,
                    transaction_id,
                    current_time,
                )
            )

            transaction_id += 1

    remaining = total_transactions - (len(account_records) * 5)

    for _ in range(remaining):

        account = random.choice(account_records)

        transactions.append(
            build_transaction(
                account,
                transaction_id,
                current_time,
            )
        )

        transaction_id += 1

    return pd.DataFrame(transactions)