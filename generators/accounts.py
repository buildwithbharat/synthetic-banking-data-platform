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


def random_opening_date(date_of_birth):
    start_date = (
        pd.to_datetime(date_of_birth)
        + pd.DateOffset(years=18)
    )

    end_date = pd.Timestamp.today()

    random_days = random.randint(
        0,
        (end_date - start_date).days,
    )

    return (
        start_date + pd.Timedelta(days=random_days)
    ).date()


def generate_accounts(config, customers, branches):

    total_accounts = config["dataset"]["accounts"]

    customer_records = customers.to_dict("records")
    branch_records = branches.to_dict("records")

    accounts = []
    account_id = 1

    # Every customer gets one account
    for customer in customer_records:

        branch = random.choice(branch_records)

        account_type = random.choices(
            ["Savings", "Salary", "Current"],
            weights=[70, 20, 10],
            k=1,
        )[0]

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
                "opening_date": random_opening_date(
                    customer["date_of_birth"]
                ),
                "current_balance": random.randint(
                    *ACCOUNT_TYPES[account_type]
                ),
            }
        )

        account_id += 1

    # Generate additional accounts
    remaining_accounts = total_accounts - len(customer_records)

    for _ in range(remaining_accounts):

        customer = random.choice(customer_records)
        branch = random.choice(branch_records)

        account_type = random.choices(
            ["Savings", "Current", "Fixed Deposit"],
            weights=[60, 15, 25],
            k=1,
        )[0]

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
                "opening_date": random_opening_date(
                    customer["date_of_birth"]
                ),
                "current_balance": random.randint(
                    *ACCOUNT_TYPES[account_type]
                ),
            }
        )

        account_id += 1

    return pd.DataFrame(accounts)