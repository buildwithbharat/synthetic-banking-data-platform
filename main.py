import yaml

from generators.branches import generate_branches
from writers.csv_writer import write_csv


def main():
    with open("config/small.yaml", "r") as file:
        config = yaml.safe_load(file)

    branches = generate_branches(config)

    write_csv(branches, "output/clean/branches.csv")

    print("Branches generated successfully!")


if __name__ == "__main__":
    main()