"""
Account Generator

Business Rules:
- Every account belongs to one customer.
- Every account belongs to one branch.
- Every customer gets at least one account.
- A customer can have multiple accounts.
"""

import random

import pandas as pd

ACCOUNT_TYPES = {
    "Savings": (5000, 500000),
    "Current": (10000, 5000000),
    "Salary": (0, 300000),
    "Fixed Deposit": (50000, 10000000),
}

ACCOUNT_STATUS = [
    "Active",
    "Dormant",
    "Closed",
]


def generate_accounts(config):

    customers = pd.read_csv("output/clean/customers.csv")
    branches = pd.read_csv("output/clean/branches.csv")

    total_accounts = config["dataset"]["accounts"]

    accounts = []
    account_id = 1

    # Every customer gets one account
    for _, customer in customers.iterrows():

        branch = branches.sample(1).iloc[0]

        account_type = random.choices(
            ["Savings", "Salary", "Current"],
            weights=[70, 20, 10],
            k=1,
        )[0]

        opening_date = random.choice(
            pd.date_range(
                pd.to_datetime(customer["date_of_birth"]) + pd.DateOffset(years=18),
                pd.Timestamp.today(),
            )
        ).date()

        accounts.append(
            {
                "account_id": f"ACC{account_id:08d}",
                "customer_id": customer["customer_id"],
                "branch_id": branch["branch_id"],
                "account_type": account_type,
                "account_status": random.choices(
                    ACCOUNT_STATUS,
                    weights=[90, 8, 2],
                    k=1,
                )[0],
                "opening_date": opening_date,
                "current_balance": random.randint(
                    *ACCOUNT_TYPES[account_type]
                ),
            }
        )

        account_id += 1

    # Generate additional accounts
    remaining_accounts = total_accounts - len(customers)

    for _ in range(remaining_accounts):

        customer = customers.sample(1).iloc[0]
        branch = branches.sample(1).iloc[0]

        account_type = random.choices(
            ["Savings", "Current", "Fixed Deposit"],
            weights=[60, 15, 25],
            k=1,
        )[0]

        opening_date = random.choice(
            pd.date_range(
                pd.to_datetime(customer["date_of_birth"]) + pd.DateOffset(years=18),
                pd.Timestamp.today(),
            )
        ).date()

        accounts.append(
            {
                "account_id": f"ACC{account_id:08d}",
                "customer_id": customer["customer_id"],
                "branch_id": branch["branch_id"],
                "account_type": account_type,
                "account_status": random.choices(
                    ACCOUNT_STATUS,
                    weights=[90, 8, 2],
                    k=1,
                )[0],
                "opening_date": opening_date,
                "current_balance": random.randint(
                    *ACCOUNT_TYPES[account_type]
                ),
            }
        )

        account_id += 1

    return pd.DataFrame(accounts)