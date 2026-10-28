import duckdb
import os

os.makedirs('data/processed', exist_ok=True)

# Connect to a DuckDB database file
con = duckdb.connect(database='data/processed/enterprise_dw.duckdb')

# Read and execute the SQL file
with open('sql/01_star_schema.sql', 'r') as file:
    sql_script = file.read()

con.execute(sql_script)

# Export processed dimensional tables to CSV for Power BI / Tableau import
tables = ['Dim_Date', 'Dim_Customer', 'Dim_Product', 'Fact_Transactions']
for tbl in tables:
    con.execute(f"COPY {tbl} TO 'data/processed/{tbl}.csv' (HEADER, DELIMITER ',')")

print("SUCCESS: DuckDB Data Warehouse created and Star Schema CSVs exported to data/processed/")
con.close()