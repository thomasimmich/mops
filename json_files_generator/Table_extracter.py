from tabula import read_pdf
import pandas as pd
import os

# Path to your PDF file
pdf_path = "./temp/tables.pdf"

try:
    # Extract tables from all pages
    tables = read_pdf(pdf_path, pages="all", multiple_tables=True, lattice=True)

    # Process and display extracted tables
    if tables:
        print(f"Found {len(tables)} table(s) in the PDF.")
        for i, table in enumerate(tables, 1):
            print(f"\nTable {i}:")
            # Display the table as a pandas DataFrame
            print(table)

            file = f"table_{i}.json"
            file = os.path.join("./temp", file)
            # Save the table to a JSON file
            table.to_json(file, orient="records", lines=True)
    else:
        print("No tables found in the PDF.")

except Exception as e:
    print(f"An error occurred: {e}")