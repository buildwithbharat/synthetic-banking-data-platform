# 🏦 Synthetic Banking Data Platform

A modular Python-based synthetic banking data generator that creates realistic banking datasets with built-in data quality validation.

The project simulates a banking ecosystem by generating interconnected datasets such as customers, branches, accounts, transactions, cards, and loans while enforcing realistic business rules and relational integrity.

---

## Features

- Generate realistic synthetic banking datasets
- Relational data modelling using primary and foreign keys
- Configurable dataset sizes
- Modular dataset generators
- Automated data validation
- Business rule validation
- Clean CSV output for analytics and Data Engineering projects

---

## Datasets Generated

| Dataset | Description |
|----------|-------------|
| Branches | Bank branch information |
| Employees | Branch employees |
| Customers | Customer master data |
| Accounts | Customer bank accounts |
| Transactions | Banking transactions |
| Cards | Debit and Credit cards |
| Loans | Customer loans |

---

## Project Structure

```text
synthetic-banking-data-platform/

├── config/
├── common/
├── generators/
├── validators/
├── writers/
├── output/
│   └── clean/
├── tests/

├── main.py
├── validate.py
├── requirements.txt
└── README.md
```

---

## Validation Framework

The project includes a modular validation framework that verifies dataset integrity after generation.

Validation includes:

- Primary Key Validation
- Foreign Key Validation
- NULL Validation
- Business Rule Validation
- Date Validation

---

## Business Rules

### Customers

- Every customer owns at least one account.

### Accounts

- Linked to valid customers and branches.

### Transactions

- Minimum five transactions per account.

### Cards

- Maximum one Debit Card per account.
- Maximum one Credit Card per account.

### Loans

- Customers may own multiple loans.
- Duplicate loan types are not allowed.

### Employees

- Every branch has exactly one Branch Manager.

---

## Getting Started

Clone the repository

```bash
git clone https://github.com/buildwithbharat/synthetic-banking-data-platform.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Generate the dataset

```bash
python main.py
```

Validate the generated dataset

```bash
python validate.py
```

---

## Tech Stack

- Python
- Pandas
- Faker
- YAML

---

## Future Improvements

- Dirty data generation
- Parquet output
- PySpark pipeline
- Airflow orchestration
- AWS deployment
- Medallion Architecture
- dbt transformations

---

## License

MIT License