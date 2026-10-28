import os
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

# 1. Load Star Schema Data
print("Loading data from data/processed...")
df_trans = pd.read_csv('data/processed/Fact_Transactions.csv')
df_cust = pd.read_csv('data/processed/Dim_Customer.csv')
df_date = pd.read_csv('data/processed/Dim_Date.csv')

# Merge date for transaction timestamps
df_trans = df_trans.merge(df_date[['date_key', 'full_date']], on='date_key', how='left')
df_trans['full_date'] = pd.to_datetime(df_trans['full_date'])
snapshot_date = df_trans['full_date'].max()

# 2. RFM Feature Engineering
rfm = df_trans.groupby('customer_key').agg(
    recency_days=('full_date', lambda x: (snapshot_date - x.max()).days),
    frequency_orders=('order_id', 'nunique'),
    monetary_margin=('net_margin', 'sum')
).reset_index()

# Merge customer metadata
rfm = rfm.merge(df_cust[['customer_key', 'customer_id', 'segment', 'tenure_months', 'region']], on='customer_key')

# 3. K-Means Customer Clustering
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['recency_days', 'frequency_orders', 'monetary_margin']])

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm['cluster_id'] = kmeans.fit_predict(rfm_scaled)

# Assign meaningful segment personas based on metrics
cluster_summary = rfm.groupby('cluster_id')[['recency_days', 'frequency_orders', 'monetary_margin']].mean()

# Map cluster IDs logically
sorted_by_monetary = cluster_summary.sort_values(by='monetary_margin', ascending=False).index.tolist()
persona_map = {
    sorted_by_monetary[0]: 'Tier 1: Champions',
    sorted_by_monetary[1]: 'Tier 2: High Potential',
    sorted_by_monetary[2]: 'Tier 3: At-Risk Frequenters',
    sorted_by_monetary[3]: 'Tier 4: Low-Engagement'
}
rfm['customer_segment'] = rfm['cluster_id'].map(persona_map)

# 4. Churn Risk Classification (Predictive Modeling)
# Define churn proxy: no purchase in the last 180 days
rfm['is_churned'] = (rfm['recency_days'] > 180).astype(int)

# Feature matrix
X = rfm[['recency_days', 'frequency_orders', 'monetary_margin', 'tenure_months']]
y = rfm['is_churned']

model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
model.fit(X, y)

# Churn Probability Score (0.00 to 1.00)
rfm['churn_probability'] = np.round(model.predict_proba(X)[:, 1], 3)

# 5. Prescriptive Decision Intelligence Engine
def determine_recommended_action(row):
    churn_prob = row['churn_probability']
    margin = row['monetary_margin']
    segment = row['customer_segment']

    if churn_prob >= 0.70 and margin > 1500:
        return 'Executive Intervention: Dedicated Account Manager Call'
    elif churn_prob >= 0.70 and margin <= 1500:
        return 'Automated Retention: 15% Re-engagement Discount'
    elif 'Champions' in segment:
        return 'Upsell / Expansion: Offer Annual Enterprise Contract'
    elif 'High Potential' in segment:
        return 'Nurture Campaign: Feature Adoption Webinar'
    else:
        return 'Standard Engagement: Bi-weekly Newsletter'

rfm['recommended_action'] = rfm.apply(determine_recommended_action, axis=1)

# 6. Save Analytical Table for Power BI / Tableau
output_cols = [
    'customer_key', 'customer_id', 'customer_segment', 'recency_days',
    'frequency_orders', 'monetary_margin', 'churn_probability', 'recommended_action'
]
fact_customer_insights = rfm[output_cols]
fact_customer_insights.to_csv('data/processed/Fact_Customer_Insights.csv', index=False)

print("SUCCESS: Fact_Customer_Insights.csv generated with ML predictions & prescriptive actions.")
print(fact_customer_insights.head())