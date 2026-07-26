"""
Card Generator

Business Rules:
- An account can have:
    - 0 or 1 Debit Card
    - 0 or 1 Credit Card
"""

import random
from dateutil.relativedelta import relativedelta
import pandas as pd

CARD_NETWORKS = [
    "RuPay",
    "Visa",
    "Mastercard",
]

CARD_STATUS = [
    "Active",
    "Blocked",
    "Expired",
]


def create_card(card_id, account, card_type):

    issue_date = random.choice(
        pd.date_range(
            pd.to_datetime(account["opening_date"]),
            pd.Timestamp.today(),
        )
    ).date()

    expiry_date = issue_date + relativedelta(years=5)

    return {
        "card_id": f"CARD{card_id:08d}",
        "account_id": account["account_id"],
        "card_type": card_type,
        "card_network": random.choices(
            CARD_NETWORKS,
            weights=[45, 35, 20],
            k=1,
        )[0],
        "card_status": random.choices(
            CARD_STATUS,
            weights=[92, 5, 3],
            k=1,
        )[0],
        "issue_date": issue_date,
        "expiry_date": expiry_date,
    }


def generate_cards(config):

    accounts = pd.read_csv("output/clean/accounts.csv")

    cards = []

    card_id = 1

    for _, account in accounts.iterrows():

        # 90% accounts receive a Debit Card
        if random.random() <= 0.90:

            cards.append(
                create_card(
                    card_id,
                    account,
                    "Debit",
                )
            )

            card_id += 1

            # 25% of debit card holders also receive a Credit Card
            if random.random() <= 0.25:

                cards.append(
                    create_card(
                        card_id,
                        account,
                        "Credit",
                    )
                )

                card_id += 1

    return pd.DataFrame(cards)