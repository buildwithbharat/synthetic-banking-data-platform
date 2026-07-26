"""
Customer Generator

Business Rules:
- Customer age is between 18 and 80 years.
- PAN is unique.
- Aadhaar is unique.
- Mobile numbers follow Indian format.
- Income depends on occupation.
"""

import random
import string

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

OCCUPATIONS = {
    "Salaried": (300000, 2500000),
    "Business": (500000, 5000000),
    "Self-Employed": (400000, 4000000),
    "Farmer": (150000, 1000000),
    "Retired": (180000, 1200000),
    "Student": (0, 150000),
}


def generate_pan():
    letters = "".join(random.choices(string.ascii_uppercase, k=5))
    numbers = "".join(random.choices(string.digits, k=4))
    last_letter = random.choice(string.ascii_uppercase)
    return f"{letters}{numbers}{last_letter}"


def generate_aadhaar():
    return "".join(random.choices(string.digits, k=12))


def generate_mobile():
    return f"+91{random.randint(6000000000, 9999999999)}"


def generate_customers(config):

    locations = pd.read_csv("config/indian_locations.csv")
    locations = locations.sample(frac=1).reset_index(drop=True)

    total_customers = config["dataset"]["customers"]

    used_pans = set()
    used_aadhaars = set()

    customers = []

    for i in range(1, total_customers + 1):

        first_name = fake.first_name()
        last_name = fake.last_name()

        dob = fake.date_of_birth(
            minimum_age=18,
            maximum_age=80,
        )

        occupation = random.choice(list(OCCUPATIONS.keys()))
        income = random.randint(*OCCUPATIONS[occupation])

        location = locations.iloc[(i - 1) % len(locations)]

        while True:
            pan = generate_pan()
            if pan not in used_pans:
                used_pans.add(pan)
                break

        while True:
            aadhaar = generate_aadhaar()
            if aadhaar not in used_aadhaars:
                used_aadhaars.add(aadhaar)
                break

        customers.append(
            {
                "customer_id": f"CUST{i:06d}",
                "first_name": first_name,
                "last_name": last_name,
                "gender": random.choice(["Male", "Female"]),
                "date_of_birth": dob.isoformat(),
                "pan_number": pan,
                "aadhaar_number": aadhaar,
                "mobile_number": generate_mobile(),
                "email": f"{first_name}.{last_name}{i}@syntheticbank.demo".lower(),
                "occupation": occupation,
                "annual_income": income,
                "city": location["city"],
                "state": location["state"],
                "kyc_status": random.choices(
                    ["Completed", "Pending"],
                    weights=[95, 5],
                )[0],
            }
        )

    return pd.DataFrame(customers)