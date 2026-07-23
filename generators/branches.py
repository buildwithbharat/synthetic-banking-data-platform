import pandas as pd
from faker import Faker

fake = Faker("en_IN")


def generate_branches(config: dict) -> pd.DataFrame:
    locations = pd.read_csv("config/indian_locations.csv")
    num_branches = config["dataset"]["branches"]

    branches = []

    for i in range(1, num_branches + 1):
        location = locations.sample(n=1).iloc[0]

        branch = {
            "branch_id": f"BR{i:06d}",
            "branch_name": f"{location['city']} Branch",
            "city": location["city"],
            "state": location["state"],
            "region": location["region"],
            "ifsc_code": f"SYNB{i:06d}",
            "opened_date": fake.date_between(
                start_date="-25y",
                end_date="today"
            ),
        }

        branches.append(branch)

    return pd.DataFrame(branches)