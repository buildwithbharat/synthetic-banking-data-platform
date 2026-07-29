import os
import yaml

from generators.accounts import generate_accounts
from generators.branches import generate_branches
from generators.cards import generate_cards
from generators.customers import generate_customers
from generators.employees import generate_employees
from generators.loans import generate_loans
from generators.transactions import generate_transactions

from writers.csv_writer import write_csv
from writers.parquet_writer import write_parquet


def write_dataset(dataframe, dataset_name, config):
    output_format = config["output"]["format"]
    output_directory = config["output"]["clean_directory"]

    os.makedirs(output_directory, exist_ok=True)

    if output_format == "csv":
        write_csv(
            dataframe,
            f"{output_directory}/{dataset_name}.csv",
        )

    elif output_format == "parquet":
        write_parquet(
            dataframe,
            f"{output_directory}/{dataset_name}.parquet",
        )

    else:
        raise ValueError(f"Unsupported output format: {output_format}")


def main():

    with open("config/medium.yaml", "r") as file:
        config = yaml.safe_load(file)

    # Branches
    branches = generate_branches(config)
    write_dataset(branches, "branches", config)

    # Employees
    employees = generate_employees(config, branches)
    write_dataset(employees, "employees", config)

    # Customers
    customers = generate_customers(config)
    write_dataset(customers, "customers", config)

    # Accounts
    accounts = generate_accounts(config, customers, branches)
    write_dataset(accounts, "accounts", config)

    # Transactions
    transactions = generate_transactions(config, accounts)
    write_dataset(transactions, "transactions", config)

    # Cards
    cards = generate_cards(config)
    write_dataset(cards, "cards", config)

    # Loans
    loans = generate_loans(config)
    write_dataset(loans, "loans", config)

    print("Synthetic banking dataset generated successfully!")


if __name__ == "__main__":
    main()