import yaml

from generators.employees import generate_employees
from writers.csv_writer import write_csv


with open("config/small.yaml", "r") as file:
    config = yaml.safe_load(file)

employees = generate_employees(config)

write_csv(
    employees,
    "output/clean/employees.csv",
)
print("Employees generated successfully!")