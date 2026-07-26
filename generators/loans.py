"""
Loan Generator

Business Rules:
- A customer can have multiple loans.
- Most customers have no loans.
- A customer cannot have two loans of the same type.
- Every loan is linked to one account.
"""

import random

import pandas as pd

LOAN_TYPES = {
    "Home": {
        "amount": (1000000, 10000000),
        "interest": 8.5,
        "tenure": [120, 180, 240, 300, 360],
    },
    "Personal": {
        "amount": (50000, 2000000),
        "interest": 12.5,
        "tenure": [12, 24, 36, 48, 60],
    },
    "Vehicle": {
        "amount": (200000, 3000000),
        "interest": 9.5,
        "tenure": [36, 48, 60, 84],
    },
    "Education": {
        "amount": (100000, 5000000),
        "interest": 8.0,
        "tenure": [36, 60, 84, 120],
    },
    "Gold": {
        "amount": (25000, 1000000),
        "interest": 10.0,
        "tenure": [12, 24, 36],
    },
}


def generate_loans(config):

    customers = pd.read_csv("output/clean/customers.csv")
    accounts = pd.read_csv("output/clean/accounts.csv")

    loans = []

    loan_id = 1

    for _, customer in customers.iterrows():

        customer_accounts = accounts[
            accounts["customer_id"] == customer["customer_id"]
        ]

        if customer_accounts.empty:
            continue

        loan_count = random.choices(
            [0, 1, 2, 3],
            weights=[80, 16, 3, 1],
            k=1,
        )[0]

        available_loan_types = list(LOAN_TYPES.keys())
        random.shuffle(available_loan_types)

        for loan_type in available_loan_types[:loan_count]:

            details = LOAN_TYPES[loan_type]

            account = customer_accounts.sample(1).iloc[0]

            loan_amount = random.randint(*details["amount"])

            outstanding_balance = random.randint(
                int(loan_amount * 0.2),
                loan_amount,
            )

            start_date = random.choice(
                pd.date_range(
                    pd.to_datetime(account["opening_date"]),
                    pd.Timestamp.today(),
                )
            ).date()

            loans.append(
                {
                    "loan_id": f"LOAN{loan_id:08d}",
                    "customer_id": customer["customer_id"],
                    "account_id": account["account_id"],
                    "loan_type": loan_type,
                    "loan_amount": loan_amount,
                    "interest_rate": details["interest"],
                    "loan_status": random.choices(
                        ["Active", "Closed", "Defaulted"],
                        weights=[85, 10, 5],
                        k=1,
                    )[0],
                    "start_date": start_date,
                    "tenure_months": random.choice(
                        details["tenure"]
                    ),
                    "outstanding_balance": outstanding_balance,
                }
            )

            loan_id += 1

    return pd.DataFrame(loans)