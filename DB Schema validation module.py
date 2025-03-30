#DB Schema validation module
import pandas as pd

'''
SQL query to get list of tables from UAT:
select CONCAT('''',TABLE_NAME,'''', ',') AS FormattedColumn from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA='dbo' order by TABLE_NAME

SQL query to get table details from dev and uat to be pasted in excel sheets.

select TABLE_NAME,DATA_TYPE,COLUMN_NAME,COLUMN_DEFAULT,IS_NULLABLE,NUMERIC_PRECISION,NUMERIC_SCALE
from INFORMATION_SCHEMA.COLUMNS where TABLE_SCHEMA='DBO'  
and TABLE_NAME in 
(
--replace table list from above query
)
order by TABLE_NAME
'''


# Load the Excel file
file_path = r"C:\Users\S.Munuswamy\OneDrive - Shell\Documents\MCSP SSE project\MVP1\CI\schema_validation.xlsx"
excel_data = pd.ExcelFile(file_path)

# Read the DEV and UAT sheets into DataFrames
dev_data = pd.read_excel(excel_data, sheet_name="DEV")
uat_data = pd.read_excel(excel_data, sheet_name="UAT")

# Function to find discrepancies and display mismatched rows
def find_discrepancies(dev, uat):
    mismatched_tables = {}
    dev_tables = set(dev['TABLE_NAME'].unique())
    uat_tables = set(uat['TABLE_NAME'].unique())

    # Find missing tables
    missing_in_uat = dev_tables - uat_tables
    missing_in_dev = uat_tables - dev_tables

    for table_name in dev_tables.intersection(uat_tables):
        dev_rows = dev[dev['TABLE_NAME'] == table_name].reset_index(drop=True)
        uat_rows = uat[uat['TABLE_NAME'] == table_name].reset_index(drop=True)

        # Compare rows and find mismatches
        if not dev_rows.equals(uat_rows):
            mismatched = pd.concat([dev_rows, uat_rows]).drop_duplicates(keep=False)
            mismatched_tables[table_name] = mismatched

    return mismatched_tables, missing_in_uat, missing_in_dev

# Find discrepancies and print results
mismatched, missing_in_uat, missing_in_dev = find_discrepancies(dev_data, uat_data)

if mismatched or missing_in_uat or missing_in_dev:
    print("Discrepancies found:")
    if mismatched:
        print("Tables with mismatched column data:")
        for table, rows in mismatched.items():
            print(f"- {table}")
            print(rows)  # Print the mismatched rows
    if missing_in_uat:
        print("Tables missing in UAT:")
        for table in missing_in_uat:
            print(f"- {table}")
    if missing_in_dev:
        print("Tables missing in DEV:")
        for table in missing_in_dev:
            print(f"- {table}")
else:
    print("No discrepancies found.")