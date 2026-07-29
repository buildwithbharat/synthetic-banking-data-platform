"""
Card Generator

Business Rules:
- An account can have:
    - 0 or 1 Debit Card
    - 0 or 1 Credit Card
"""

import random

import pandas as pd
from dateutil.relativedelta import relativedelta

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


def random_issue_date(opening_date, current_time):
    """
    Generate a random issue date between
    account opening and today.
    """

    start = pd.Timestamp(opening_date)

    start_seconds = int(start.timestamp())
    end_seconds = int(current_time.timestamp())

    random_seconds = random.randint(
        start_seconds,
        end_seconds,
    )

    return pd.Timestamp(
        random_seconds,
        unit="s",
    ).date()


def create_card(
    card_id,
    account,
    card_type,
    current_time,
):

    issue_date = random_issue_date(
        account["opening_date"],
        current_time,
    )

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


def generate_cards(config, accounts):

    cards = []

    card_id = 1

    current_time = pd.Timestamp.now()

    account_records = accounts.to_dict("records")

    for account in account_records:

        # 90% accounts receive a Debit Card
        if random.random() <= 0.90:

            cards.append(
                create_card(
                    card_id,
                    account,
                    "Debit",
                    current_time,
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
                        current_time,
                    )
                )

                card_id += 1

    return pd.DataFrame(cards)