import os
import time
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

    print("=" * 60)
    print("Synthetic Banking Data Generator")
    print("=" * 60)

    # ------------------------------------------------------------------
    print("\n[1/7] Generating Branches...")
    start = time.perf_counter()

    branches = generate_branches(config)
    write_dataset(branches, "branches", config)

    print(
        f"✓ Branches generated ({len(branches):,} rows) "
        f"in {time.perf_counter() - start:.2f}s"
    )

    # ------------------------------------------------------------------
    print("\n[2/7] Generating Employees...")
    start = time.perf_counter()

    employees = generate_employees(config, branches)
    write_dataset(employees, "employees", config)

    print(
        f"✓ Employees generated ({len(employees):,} rows) "
        f"in {time.perf_counter() - start:.2f}s"
    )

    # ------------------------------------------------------------------
    print("\n[3/7] Generating Customers...")
    start = time.perf_counter()

    customers = generate_customers(config)
    write_dataset(customers, "customers", config)

    print(
        f"✓ Customers generated ({len(customers):,} rows) "
        f"in {time.perf_counter() - start:.2f}s"
    )

    # ------------------------------------------------------------------
    print("\n[4/7] Generating Accounts...")
    start = time.perf_counter()

    accounts = generate_accounts(config, customers, branches)
    write_dataset(accounts, "accounts", config)

    print(
        f"✓ Accounts generated ({len(accounts):,} rows) "
        f"in {time.perf_counter() - start:.2f}s"
    )

    # ------------------------------------------------------------------
    print("\n[5/7] Generating Transactions...")
    start = time.perf_counter()

    transactions = generate_transactions(config, accounts)
    write_dataset(transactions, "transactions", config)

    print(
        f"✓ Transactions generated ({len(transactions):,} rows) "
        f"in {time.perf_counter() - start:.2f}s"
    )

    # ------------------------------------------------------------------
    print("\n[6/7] Generating Cards...")
    start = time.perf_counter()

    cards = cards = generate_cards(config,accounts)
    write_dataset(cards, "cards", config)

    print(
        f"✓ Cards generated ({len(cards):,} rows) "
        f"in {time.perf_counter() - start:.2f}s"
    )

    # ------------------------------------------------------------------
    print("\n[7/7] Generating Loans...")
    start = time.perf_counter()

    loans = generate_loans(config, customers, accounts)
    write_dataset(loans, "loans", config)

    print(
        f"✓ Loans generated ({len(loans):,} rows) "
        f"in {time.perf_counter() - start:.2f}s"
    )

    print("\n" + "=" * 60)
    print("✓ Synthetic banking dataset generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()