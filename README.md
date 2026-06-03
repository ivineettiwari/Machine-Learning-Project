# Data Preprocessing — Teaching Module

A six-notebook walkthrough of the core data-preprocessing toolkit, built around a
single realistic dataset (`data/customer_churn.csv`) that is intentionally messy:
missing values, outliers, mixed categoricals, and an imbalanced target.

## Contents

| # | Notebook | Topic |
|---|----------|-------|
| 1 | [01_handling_missing_data.ipynb](01_handling_missing_data.ipynb) | Missing-value detection, MCAR/MAR/MNAR, mean/median/mode/KNN/MICE imputation, missingness indicators |
| 2 | [02_outlier_detection.ipynb](02_outlier_detection.ipynb) | IQR, Z-score, MAD, Isolation Forest, LOF — and capping vs transforming vs removing |
| 3 | [03_encoding_categorical.ipynb](03_encoding_categorical.ipynb) | Label / Ordinal / One-Hot / Frequency / Target encoding + `ColumnTransformer` |
| 4 | [04_scaling_normalization.ipynb](04_scaling_normalization.ipynb) | Min-Max, Standard, Robust, MaxAbs scalers; the train/test leakage trap |
| 5 | [05_feature_selection_engineering.ipynb](05_feature_selection_engineering.ipynb) | Domain features, binning, interactions; filter / wrapper / embedded selection; permutation importance |
| 6 | [06_handling_imbalanced_data.ipynb](06_handling_imbalanced_data.ipynb) | Why accuracy lies; `class_weight`, ROS/SMOTE/ADASYN, RUS, SMOTEENN; resample only on the training fold |

Each notebook follows the same shape: **objectives → motivation → 3–6 techniques → comparison → cheat sheet → exercise.**

## Setup

```bash
pip install pandas numpy scikit-learn matplotlib seaborn scipy imbalanced-learn jupyter
```

## Regenerate the dataset

```bash
python generate_data.py
```

Produces `data/customer_churn.csv` (5,000 rows, 15 columns, ~9% churn). The file
already exists — only re-run if you want to reseed.

## Rebuild the notebooks

```bash
python build_notebooks.py
```

The notebooks are generated from a single Python source so corrections / extensions
stay in one place.
