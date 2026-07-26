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


def generate_transactions(config):

    accounts = pd.read_csv("output/clean/accounts.csv")

    total_transactions = config["dataset"]["transactions"]

    transactions = []

    transaction_id = 1

    # Every account gets at least 5 transactions
    for _, account in accounts.iterrows():

        for _ in range(5):

            mode = random.choices(
                list(TRANSACTION_MODES.keys()),
                weights=[45, 10, 15, 10, 2, 13, 5],
                k=1,
            )[0]

            transactions.append(
                {
                    "transaction_id": f"TXN{transaction_id:010d}",
                    "account_id": account["account_id"],
                    "transaction_timestamp": random.choice(
                        pd.date_range(
                            pd.to_datetime(account["opening_date"]),
                            pd.Timestamp.now(),
                            freq="h",
                        )
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
            )

            transaction_id += 1

    remaining = total_transactions - (len(accounts) * 5)

    for _ in range(remaining):

        account = accounts.sample(1).iloc[0]

        mode = random.choices(
            list(TRANSACTION_MODES.keys()),
            weights=[45, 10, 15, 10, 2, 13, 5],
            k=1,
        )[0]

        transactions.append(
            {
                "transaction_id": f"TXN{transaction_id:010d}",
                "account_id": account["account_id"],
                "transaction_timestamp": random.choice(
                    pd.date_range(
                        pd.to_datetime(account["opening_date"]),
                        pd.Timestamp.now(),
                        freq="h",
                    )
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
        )

        transaction_id += 1

    return pd.DataFrame(transactions)