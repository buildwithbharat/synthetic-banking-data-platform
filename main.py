import yaml

from generators.branches import generate_branches
from generators.employees import generate_employees
from generators.customers import generate_customers
from generators.accounts import generate_accounts
from generators.transactions import generate_transactions

from writers.csv_writer import write_csv


with open("config/small.yaml", "r") as file:
    config = yaml.safe_load(file)

# Branches
branches = generate_branches(config)
write_csv(branches, "output/clean/branches.csv")

# Employees
employees = generate_employees(config)
write_csv(employees, "output/clean/employees.csv")

# Customers
customers = generate_customers(config)
write_csv(customers, "output/clean/customers.csv")

# Accounts
accounts = generate_accounts(config)
write_csv(accounts, "output/clean/accounts.csv")

# Transactions
transactions = generate_transactions(config)
write_csv(transactions, "output/clean/transactions.csv")