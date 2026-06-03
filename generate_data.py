"""
Generate a realistic Customer Churn dataset for teaching data preprocessing.

The dataset is intentionally messy:
  - Missing values (MCAR + MAR patterns) in age, total_charges, estimated_salary
  - Outliers in monthly_charges and estimated_salary
  - Mixed categorical features (nominal and ordinal)
  - Class imbalance in `churned` (~15% positive class)

Run:  python generate_data.py
Output: data/customer_churn.csv
"""

import os
import numpy as np
import pandas as pd

RNG = np.random.default_rng(seed=42)
N = 5000

os.makedirs("data", exist_ok=True)

# --- core numeric features ---
age = RNG.normal(loc=42, scale=13, size=N).clip(18, 90).round().astype(int)
tenure_months = RNG.integers(0, 73, size=N)
monthly_charges = RNG.normal(loc=65, scale=22, size=N).clip(10, 130).round(2)
estimated_salary = RNG.normal(loc=70_000, scale=22_000, size=N).clip(15_000, 200_000).round(2)

# total_charges roughly tracks tenure * monthly_charges, with noise
total_charges = (tenure_months * monthly_charges + RNG.normal(0, 50, N)).clip(0).round(2)

num_products = RNG.choice([1, 2, 3, 4], size=N, p=[0.55, 0.30, 0.12, 0.03])
has_credit_card = RNG.choice([0, 1], size=N, p=[0.30, 0.70])
is_active_member = RNG.choice([0, 1], size=N, p=[0.45, 0.55])

# --- categorical features ---
gender = RNG.choice(["Male", "Female"], size=N, p=[0.52, 0.48])
city = RNG.choice(
    ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Pune"],
    size=N,
    p=[0.25, 0.22, 0.18, 0.12, 0.13, 0.10],
)
contract_type = RNG.choice(
    ["Month-to-month", "One year", "Two year"], size=N, p=[0.55, 0.25, 0.20]
)
payment_method = RNG.choice(
    ["Electronic check", "Mailed check", "Bank transfer", "Credit card"],
    size=N,
    p=[0.34, 0.20, 0.22, 0.24],
)
education = RNG.choice(
    ["High School", "Bachelors", "Masters", "PhD"], size=N, p=[0.30, 0.45, 0.20, 0.05]
)

# --- target: churn (imbalanced ~15%) driven by a few signals ---
logit = (
    -2.2
    + 0.9 * (contract_type == "Month-to-month").astype(float)
    - 0.5 * (contract_type == "Two year").astype(float)
    + 0.8 * (payment_method == "Electronic check").astype(float)
    - 0.6 * is_active_member
    - 0.02 * tenure_months
    + 0.012 * (monthly_charges - 65)
    + 0.4 * (num_products >= 3).astype(float)
)
prob = 1 / (1 + np.exp(-logit))
churned = (RNG.uniform(size=N) < prob).astype(int)

df = pd.DataFrame(
    {
        "customer_id": np.arange(10_000, 10_000 + N),
        "age": age,
        "gender": gender,
        "city": city,
        "education": education,
        "tenure_months": tenure_months,
        "contract_type": contract_type,
        "payment_method": payment_method,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "num_products": num_products,
        "has_credit_card": has_credit_card,
        "is_active_member": is_active_member,
        "estimated_salary": estimated_salary,
        "churned": churned,
    }
)

# --- inject outliers (deliberately extreme) ---
outlier_idx = RNG.choice(N, size=40, replace=False)
df.loc[outlier_idx[:20], "monthly_charges"] = RNG.uniform(250, 500, 20).round(2)
df.loc[outlier_idx[20:], "estimated_salary"] = RNG.uniform(400_000, 900_000, 20).round(2)

# --- inject missing values ---
# MCAR: age missing at random
age_missing = RNG.choice(N, size=int(0.08 * N), replace=False)
df.loc[age_missing, "age"] = np.nan

# MAR: total_charges missing more often when tenure_months == 0 (new customers)
new_cust = df.index[df["tenure_months"] == 0].to_numpy()
extra = RNG.choice(N, size=int(0.04 * N), replace=False)
df.loc[np.unique(np.concatenate([new_cust, extra])), "total_charges"] = np.nan

# MCAR: estimated_salary missing
sal_missing = RNG.choice(N, size=int(0.06 * N), replace=False)
df.loc[sal_missing, "estimated_salary"] = np.nan

# MCAR: a few missing categorical values too (real datasets have these)
edu_missing = RNG.choice(N, size=int(0.03 * N), replace=False)
df.loc[edu_missing, "education"] = np.nan

df.to_csv("data/customer_churn.csv", index=False)

print(f"Wrote data/customer_churn.csv  shape={df.shape}")
print("\nMissing values per column:")
print(df.isna().sum()[df.isna().sum() > 0])
print(f"\nChurn rate: {df['churned'].mean():.1%}")
