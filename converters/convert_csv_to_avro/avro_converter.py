#!/usr/bin/env python3
# avro_converter.py
# Converts a .csv file into an Avro file with compression support

from pathlib import Path
from utils.data_utils import read_csv_file, write_avro_file


# Root of the repo
REPO_ROOT = Path(__file__).resolve().parents[2]

# Data folder
DATA_DIR = REPO_ROOT / "dataset"

# Script folder (current converter)
SCRIPT_DIR = Path(__file__).resolve().parent

# Input CSV
in_file = DATA_DIR / "IKEA_product_catalog.csv"

# Output Avro
out_file = SCRIPT_DIR / "IKEA.avro"


def main():

    # Call the function to read the CSV file
    df = read_csv_file(in_file)

    if df is None:
        print("Conversion aborted.")
        return

    # Call the function to write the Avro file
    avro = write_avro_file(
        df,
        out_file,
    )

    if avro:
        print("\nConversion completed successfully!")
    else:
        print("\nConversion failed.")


if __name__ == "__main__":
    main()
