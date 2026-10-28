import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

os.makedirs('data/raw', exist_ok=True)

# 1. Customers
num_customers = 1000
customer_ids = [f"CUST_{i:04d}" for i in range(1, num_customers + 1)]
regions = np.random.choice(['North America', 'EMEA', 'APAC', 'LATAM'], size=num_customers, p=[0.4, 0.3, 0.2, 0.1])
segments = np.random.choice(['Enterprise', 'Mid-Market', 'SMB'], size=num_customers, p=[0.2, 0.3, 0.5])
tenure_months = np.random.randint(1, 48, size=num_customers)

df_customers = pd.DataFrame({
    'customer_id': customer_ids,
    'region': regions,
    'segment': segments,
    'tenure_months': tenure_months
})
df_customers.to_csv('data/raw/raw_customers.csv', index=False)

# 2. Products
products = [
    ('PROD_01', 'Cloud Storage Tier A', 'Infrastructure', 20.0, 50.0),
    ('PROD_02', 'Cloud Storage Tier B', 'Infrastructure', 45.0, 100.0),
    ('PROD_03', 'Analytics Core License', 'Software', 60.0, 150.0),
    ('PROD_04', 'Analytics Enterprise Add-on', 'Software', 120.0, 300.0),
    ('PROD_05', 'Security Suite Pro', 'Cybersecurity', 80.0, 200.0),
    ('PROD_06', 'Premium 24/7 Support', 'Services', 150.0, 350.0)
]
df_products = pd.DataFrame(products, columns=['product_id', 'product_name', 'category', 'unit_cost', 'unit_price'])
df_products.to_csv('data/raw/raw_products.csv', index=False)

# 3. Transactions
num_transactions = 15000
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range_days = (end_date - start_date).days

order_ids = [f"ORD_{i:06d}" for i in range(1, num_transactions + 1)]
cust_sample = np.random.choice(customer_ids, size=num_transactions)
prod_sample = np.random.choice(df_products['product_id'], size=num_transactions)
date_sample = [start_date + timedelta(days=int(np.random.randint(0, date_range_days))) for _ in range(num_transactions)]
units_sample = np.random.choice([1, 2, 3, 5, 10], size=num_transactions, p=[0.5, 0.25, 0.15, 0.07, 0.03])
discounts = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20], size=num_transactions, p=[0.5, 0.2, 0.15, 0.1, 0.05])

df_orders = pd.DataFrame({
    'order_id': order_ids,
    'customer_id': cust_sample,
    'product_id': prod_sample,
    'order_date': date_sample,
    'units_sold': units_sample,
    'discount_pct': discounts
})

df_orders = df_orders.merge(df_products, on='product_id', how='left')
df_orders['gross_revenue'] = (df_orders['units_sold'] * df_orders['unit_price']) * (1 - df_orders['discount_pct'])
df_orders['total_cost'] = df_orders['units_sold'] * df_orders['unit_cost']
df_orders['net_margin'] = df_orders['gross_revenue'] - df_orders['total_cost']

df_orders = df_orders[['order_id', 'customer_id', 'product_id', 'order_date', 'units_sold', 'discount_pct', 'gross_revenue', 'net_margin']]
df_orders.to_csv('data/raw/raw_transactions.csv', index=False)

print("SUCCESS: 3 CSV files created in data/raw/")