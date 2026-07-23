import pandas as pd
from faker import Faker

fake = Faker("en_IN")


def generate_branches(config: dict) -> pd.DataFrame:
    locations = pd.read_csv("config/indian_locations.csv")
    locations = locations.sample(frac=1).reset_index(drop=True)

    num_branches = config["dataset"]["branches"]

    branches = []
    city_branch_counter = {}

    for i in range(num_branches):
        location = locations.iloc[i % len(locations)]

        city = location["city"]
        city_code = city.replace(" ", "")[:3].upper()

        city_branch_counter[city] = city_branch_counter.get(city, 0) + 1

        ifsc_code = f"SYNB{city_code}{city_branch_counter[city]:03d}"

        branch = {
            "branch_id": f"BR{i + 1:06d}",
            "branch_name": f"{location['locality']} Branch",
            "city": city,
            "state": location["state"],
            "region": location["region"],
            "tier": location["tier"],
            "ifsc_code": ifsc_code,
            "opened_date": fake.date_between(
                start_date="-25y",
                end_date="today"
            ),
        }

        branches.append(branch)

    return pd.DataFrame(branches)