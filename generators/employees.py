"""
Employee Generator

Business Rules:
- Every employee belongs to exactly one branch.
- Every branch has exactly one Branch Manager.
"""

import random

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

DESIGNATIONS = {
    "Branch Manager": (900000, 1500000),
    "Assistant Manager": (600000, 900000),
    "Relationship Manager": (450000, 700000),
    "Operations Executive": (350000, 550000),
    "Customer Service Executive": (300000, 500000),
    "Cashier": (250000, 450000),
}


def generate_employees(config, branches):
    total_employees = config["dataset"]["employees"]

    employees = []
    employee_id = 1

    # One Branch Manager per branch
    for _, branch in branches.iterrows():

        first_name = fake.first_name()
        last_name = fake.last_name()

        employees.append(
            {
                "employee_id": f"EMP{employee_id:06d}",
                "first_name": first_name,
                "last_name": last_name,
                "designation": "Branch Manager",
                "salary": random.randint(*DESIGNATIONS["Branch Manager"]),
                "joining_date": fake.date_between(
                    start_date=pd.to_datetime(branch["opened_date"]).date(),
                    end_date="today",
                ).isoformat(),
                "branch_id": branch["branch_id"],
            }
        )

        employee_id += 1

    # Remaining employees
    for _ in range(total_employees - len(branches)):

        branch = branches.sample(1).iloc[0]

        designation = random.choice(
            [d for d in DESIGNATIONS if d != "Branch Manager"]
        )

        first_name = fake.first_name()
        last_name = fake.last_name()

        employees.append(
            {
                "employee_id": f"EMP{employee_id:06d}",
                "first_name": first_name,
                "last_name": last_name,
                "designation": designation,
                "salary": random.randint(*DESIGNATIONS[designation]),
                "joining_date": fake.date_between(
                    start_date=pd.to_datetime(branch["opened_date"]).date(),
                    end_date="today",
                ).isoformat(),
                "branch_id": branch["branch_id"],
            }
        )

        employee_id += 1

    return pd.DataFrame(employees)