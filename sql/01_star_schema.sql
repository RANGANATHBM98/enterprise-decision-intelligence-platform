-- 1. Date Dimension Table
CREATE OR REPLACE TABLE Dim_Date AS
WITH date_series AS (
    SELECT UNNEST(generate_series(DATE '2023-01-01', DATE '2024-12-31', INTERVAL 1 DAY))::DATE AS full_date
)
SELECT 
    CAST(strftime(full_date, '%Y%m%d') AS INTEGER) AS date_key,
    full_date,
    YEAR(full_date) AS year,
    'Q' || QUARTER(full_date) AS fiscal_quarter,
    MONTHNAME(full_date) AS month_name,
    DAYOFWEEK(full_date) IN (0, 6) AS is_weekend
FROM date_series;

-- 2. Customer Dimension Table
CREATE OR REPLACE TABLE Dim_Customer AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY customer_id) AS customer_key,
    customer_id,
    region,
    segment,
    tenure_months
FROM read_csv_auto('data/raw/raw_customers.csv');

-- 3. Product Dimension Table
CREATE OR REPLACE TABLE Dim_Product AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY product_id) AS product_key,
    product_id,
    product_name,
    category,
    unit_cost,
    unit_price
FROM read_csv_auto('data/raw/raw_products.csv');

-- 4. Transactions Fact Table (with Foreign Key mappings)
CREATE OR REPLACE TABLE Fact_Transactions AS
SELECT 
    t.order_id,
    CAST(strftime(t.order_date::DATE, '%Y%m%d') AS INTEGER) AS date_key,
    c.customer_key,
    p.product_key,
    t.units_sold,
    t.discount_pct,
    ROUND(t.gross_revenue, 2) AS gross_revenue,
    ROUND(t.net_margin, 2) AS net_margin
FROM read_csv_auto('data/raw/raw_transactions.csv') t
JOIN Dim_Customer c ON t.customer_id = c.customer_id
JOIN Dim_Product p ON t.product_id = p.product_id;