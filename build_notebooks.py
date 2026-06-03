"""
Build the six teaching notebooks for the data preprocessing module.

Run:  python build_notebooks.py
"""

import json
import os
from textwrap import dedent

OUT_DIR = "."


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": dedent(text).strip().splitlines(keepends=True),
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": dedent(text).strip().splitlines(keepends=True),
    }


def nb(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.13"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_nb(filename: str, cells: list[dict]) -> None:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb(cells), f, indent=1, ensure_ascii=False)
    print(f"  wrote {filename}")


# =====================================================================
# Shared header used at the top of every notebook
# =====================================================================
def header(title: str, objectives: list[str]) -> list[dict]:
    obj_md = "\n".join(f"- {o}" for o in objectives)
    return [
        md(f"""
        # {title}

        > Part of the **Data Preprocessing** module — taught alongside the `data/customer_churn.csv` dataset.

        ## Learning objectives
        {obj_md}

        ---
        """),
        code("""
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns

        sns.set_theme(style="whitegrid")
        pd.set_option("display.max_columns", 30)
        pd.set_option("display.width", 140)

        df = pd.read_csv("data/customer_churn.csv")
        print("shape:", df.shape)
        df.head()
        """),
    ]


# =====================================================================
# 01 — Handling Missing Data
# =====================================================================
nb1 = header(
    "01 · Handling Missing Data (Imputation Techniques)",
    [
        "Detect and quantify missing values in a real dataset",
        "Distinguish MCAR, MAR, and MNAR — and why the type matters",
        "Apply mean / median / mode, KNN, and iterative (MICE) imputation",
        "Add a *missingness indicator* and understand when to keep one",
        "Choose the right strategy per column — not one-size-fits-all",
    ],
) + [
    md("""
    ## 1. Detect missing values

    Always start by *measuring* the problem. `isna().sum()` per column gives the count;
    dividing by `len(df)` gives the fraction — a more useful number for deciding strategy.
    """),
    code("""
    missing = pd.DataFrame({
        "n_missing": df.isna().sum(),
        "pct_missing": df.isna().mean().round(3),
        "dtype": df.dtypes,
    })
    missing[missing["n_missing"] > 0].sort_values("pct_missing", ascending=False)
    """),
    code("""
    # Visual map of missingness — useful for spotting patterns across rows
    plt.figure(figsize=(10, 4))
    sns.heatmap(df.isna(), cbar=False, yticklabels=False)
    plt.title("Missingness map (white = missing)")
    plt.show()
    """),
    md("""
    ## 2. MCAR vs MAR vs MNAR

    | Type | Meaning | Example |
    |------|---------|---------|
    | **MCAR** | Missing completely at random | Sensor randomly drops a reading |
    | **MAR**  | Missingness depends on *other observed* columns | `total_charges` missing because `tenure_months == 0` |
    | **MNAR** | Missingness depends on the *missing value itself* | High earners refuse to disclose salary |

    MCAR is safest to drop. MAR can usually be imputed well using other features.
    MNAR is the dangerous one — imputation will be biased; sometimes you need a separate model
    or a *missingness indicator* feature.
    """),
    code("""
    # Quick MAR check: is total_charges missing more often for new customers?
    df.assign(missing_total=df["total_charges"].isna()) \\
      .groupby(df["tenure_months"] == 0)["churned"].count() \\
      .rename(index={True: "tenure==0", False: "tenure>0"})
    print("Missing rate when tenure==0:",
          df.loc[df["tenure_months"] == 0, "total_charges"].isna().mean().round(3))
    print("Missing rate when tenure>0 :",
          df.loc[df["tenure_months"] >  0, "total_charges"].isna().mean().round(3))
    """),
    md("""
    ## 3. Strategy 1 — Drop

    Dropping is fine when missingness is small (<5%) **and** MCAR. It is wrong when the
    missingness itself is informative.
    """),
    code("""
    print("Original rows:", len(df))
    print("After dropna() :", len(df.dropna()))
    print("Lose:", df.isna().any(axis=1).mean().round(3), "of rows")
    """),
    md("""
    ## 4. Strategy 2 — Simple imputation (mean / median / mode)

    - **Mean** — for symmetric numeric columns
    - **Median** — for skewed numeric columns or when outliers exist
    - **Mode** — for categorical columns

    Always **fit the imputer on the training set only**, then transform both train and test.
    Doing it on the whole dataframe leaks information.
    """),
    code("""
    from sklearn.model_selection import train_test_split
    from sklearn.impute import SimpleImputer

    X = df.drop(columns=["customer_id", "churned"])
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    num_cols = X_train.select_dtypes(include="number").columns.tolist()
    cat_cols = X_train.select_dtypes(exclude="number").columns.tolist()

    median_imp = SimpleImputer(strategy="median")
    mode_imp   = SimpleImputer(strategy="most_frequent")

    X_train_num = pd.DataFrame(median_imp.fit_transform(X_train[num_cols]),
                               columns=num_cols, index=X_train.index)
    X_train_cat = pd.DataFrame(mode_imp.fit_transform(X_train[cat_cols]),
                               columns=cat_cols, index=X_train.index)

    X_train_num.isna().sum().sum(), X_train_cat.isna().sum().sum()
    """),
    md("""
    ## 5. Strategy 3 — KNN imputation

    Fills a missing value using the *k* nearest rows (by the other features). Captures
    relationships between columns that mean/median can't. Pricier to compute, but often
    much more accurate when features are correlated.
    """),
    code("""
    from sklearn.impute import KNNImputer

    knn_imp = KNNImputer(n_neighbors=5)
    X_train_knn = pd.DataFrame(
        knn_imp.fit_transform(X_train[num_cols]),
        columns=num_cols, index=X_train.index,
    )
    X_train_knn[num_cols].describe().round(2)
    """),
    md("""
    ## 6. Strategy 4 — Iterative imputation (MICE-style)

    Models each column with missing values as a regression on the others, iterating until
    convergence. The most flexible option for numeric data.
    """),
    code("""
    from sklearn.experimental import enable_iterative_imputer  # noqa: F401
    from sklearn.impute import IterativeImputer

    mice = IterativeImputer(max_iter=10, random_state=0)
    X_train_mice = pd.DataFrame(
        mice.fit_transform(X_train[num_cols]),
        columns=num_cols, index=X_train.index,
    )
    X_train_mice[num_cols].describe().round(2)
    """),
    md("""
    ## 7. Bonus — Missingness indicator

    Sometimes *the fact that a value is missing* is itself predictive (think: a customer who
    didn't fill in salary may behave differently). Add a binary `_was_missing` column before
    imputing and let the model decide if it's useful.
    """),
    code("""
    train = X_train.copy()
    for col in ["age", "total_charges", "estimated_salary"]:
        train[f"{col}_was_missing"] = train[col].isna().astype(int)

    train.filter(like="_was_missing").mean().round(3)
    """),
    md("""
    ## 8. Compare strategies side-by-side

    Same column (`age`) imputed three different ways. Look at the resulting distributions —
    mean/median imputation creates a **spike** at the imputed value; KNN/MICE preserve shape.
    """),
    code("""
    fig, axes = plt.subplots(1, 4, figsize=(16, 3.5), sharey=True)

    axes[0].hist(df["age"].dropna(), bins=30); axes[0].set_title("Original (drop NA)")

    median_age = df["age"].median()
    axes[1].hist(df["age"].fillna(median_age), bins=30); axes[1].set_title("Median imputed")

    axes[2].hist(X_train_knn["age"], bins=30);  axes[2].set_title("KNN imputed")
    axes[3].hist(X_train_mice["age"], bins=30); axes[3].set_title("MICE imputed")

    for a in axes: a.set_xlabel("age")
    plt.tight_layout(); plt.show()
    """),
    md("""
    ## 9. Cheat sheet — when to use what

    | Situation | Use |
    |-----------|-----|
    | Tiny missing % (<1%), MCAR | drop |
    | Numeric, skewed, fast pipeline | median |
    | Categorical | mode (most_frequent) or `"Missing"` as its own category |
    | Features correlated, more compute OK | KNN |
    | Mixed columns, want best quality | IterativeImputer (MICE) |
    | Missingness might be informative | add a `_was_missing` indicator |

    ## Exercise
    1. Build a `ColumnTransformer` that median-imputes numeric and mode-imputes categorical,
       then trains a `LogisticRegression` and reports test accuracy.
    2. Repeat with `KNNImputer` for numeric. Did accuracy change? Why or why not?
    """),
]
write_nb("01_handling_missing_data.ipynb", nb1)


# =====================================================================
# 02 — Outlier Detection and Handling
# =====================================================================
nb2 = header(
    "02 · Outlier Detection and Handling",
    [
        "Spot outliers visually (boxplot, histogram) and statistically (IQR, Z-score, MAD)",
        "Use Isolation Forest and LOF for multivariate outliers",
        "Decide between *removing*, *capping (winsorising)*, and *transforming*",
        "Avoid the trap of treating all extremes as bad",
    ],
) + [
    md("""
    ## 1. What is an outlier?

    A point far from the rest of the data. **Outlier ≠ error.** A genuine extreme observation
    can be the most important point in your dataset (fraud, churn, equipment failure).

    Two questions before any handling:
    1. Is it a *data error* (typo, unit mix-up) or a *real* extreme?
    2. Will it distort the model I'm planning to fit?

    Tree-based models tolerate outliers well. Linear models, distance-based models (KNN, k-means),
    and PCA do not.
    """),
    code("""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    sns.boxplot(x=df["monthly_charges"], ax=axes[0])
    axes[0].set_title("monthly_charges")
    sns.boxplot(x=df["estimated_salary"], ax=axes[1])
    axes[1].set_title("estimated_salary")
    plt.tight_layout(); plt.show()
    """),
    md("""
    ## 2. IQR method (Tukey's fences)

    A point is an outlier if it falls below `Q1 − 1.5·IQR` or above `Q3 + 1.5·IQR`.
    Robust because it ignores the tails when computing the cutoffs. Works on any distribution
    shape.
    """),
    code("""
    def iqr_bounds(s, k=1.5):
        q1, q3 = s.quantile([0.25, 0.75])
        iqr = q3 - q1
        return q1 - k * iqr, q3 + k * iqr

    for col in ["monthly_charges", "estimated_salary"]:
        lo, hi = iqr_bounds(df[col])
        n_out = ((df[col] < lo) | (df[col] > hi)).sum()
        print(f"{col:20s}  bounds=({lo:.0f}, {hi:.0f})  outliers={n_out}")
    """),
    md("""
    ## 3. Z-score method

    A point is an outlier if `|z| > 3` where `z = (x − mean) / std`.
    Assumes the column is roughly Gaussian — use it on near-normal columns only. The mean and
    std are themselves pulled by outliers, which is why people prefer the next method.
    """),
    code("""
    from scipy import stats
    z = np.abs(stats.zscore(df["monthly_charges"], nan_policy="omit"))
    print("monthly_charges z>3 outliers:", (z > 3).sum())
    """),
    md("""
    ## 4. Modified Z-score (MAD)

    Uses **median absolute deviation** instead of mean/std → robust to the very outliers
    you're trying to detect. Threshold ≈ 3.5.

    `mod_z = 0.6745 · (x − median) / MAD`
    """),
    code("""
    def modified_zscore(x):
        x = np.asarray(x, dtype=float)
        med = np.nanmedian(x)
        mad = np.nanmedian(np.abs(x - med))
        return 0.6745 * (x - med) / (mad if mad else 1)

    mz = modified_zscore(df["monthly_charges"])
    print("monthly_charges |mod_z|>3.5 outliers:", (np.abs(mz) > 3.5).sum())
    """),
    md("""
    ## 5. Multivariate outliers — Isolation Forest

    A point can look normal in every column individually but be weird *in combination*
    (e.g. a 22-year-old earning ₹5 lakh/month with a 60-month tenure). Univariate methods miss these.

    Isolation Forest builds random trees; outliers are the points that get isolated in *fewer*
    splits.
    """),
    code("""
    from sklearn.ensemble import IsolationForest

    iso_features = ["age", "tenure_months", "monthly_charges", "estimated_salary"]
    sub = df[iso_features].dropna()

    iso = IsolationForest(contamination=0.02, random_state=42)
    is_outlier = iso.fit_predict(sub) == -1
    print(f"Isolation Forest flagged {is_outlier.sum()} of {len(sub)} rows ({is_outlier.mean():.1%})")
    sub.loc[is_outlier].head()
    """),
    md("""
    ## 6. Local Outlier Factor (LOF)

    Compares the local density of a point to the densities of its neighbours. Good for
    clustered data where global thresholds don't make sense.
    """),
    code("""
    from sklearn.neighbors import LocalOutlierFactor

    lof = LocalOutlierFactor(n_neighbors=20, contamination=0.02)
    lof_flag = lof.fit_predict(sub) == -1
    print(f"LOF flagged {lof_flag.sum()} rows")
    """),
    md("""
    ## 7. Handling — three options

    ### a) Remove (use sparingly)
    Only when you're sure they're errors. You lose information otherwise.

    ### b) Cap / Winsorise
    Clip values to the IQR fences (or the 1st/99th percentile). Keeps the row but tames
    the extreme.

    ### c) Transform
    A `log1p` or square-root transform pulls the long tail in. Often eliminates the
    "outlier" entirely without removing data.
    """),
    code("""
    df_capped = df.copy()
    for col in ["monthly_charges", "estimated_salary"]:
        lo, hi = iqr_bounds(df_capped[col])
        df_capped[col] = df_capped[col].clip(lo, hi)

    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5), sharey=True)
    sns.boxplot(x=df["monthly_charges"], ax=axes[0]).set(title="Before capping")
    sns.boxplot(x=df_capped["monthly_charges"], ax=axes[1]).set(title="After IQR cap")
    plt.tight_layout(); plt.show()
    """),
    code("""
    # Log transform on a long-tailed column
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    df["estimated_salary"].hist(bins=40, ax=axes[0]); axes[0].set_title("Original")
    np.log1p(df["estimated_salary"]).hist(bins=40, ax=axes[1]); axes[1].set_title("log1p")
    plt.tight_layout(); plt.show()
    """),
    md("""
    ## 8. Decision guide

    | Situation | Action |
    |-----------|--------|
    | Clear data error (impossible value) | drop or fix |
    | Real extreme, linear/distance model | cap or transform |
    | Real extreme, tree model | usually leave alone |
    | Multivariate weirdness | Isolation Forest / LOF + investigate |
    | Imbalanced rare class (e.g. fraud) | the "outliers" are your signal — keep them |

    ## Exercise
    1. Apply the IQR cap only on the training set (not test) — why does that order matter?
    2. Compare logistic-regression accuracy with vs without log-transforming `estimated_salary`.
    """),
]
write_nb("02_outlier_detection.ipynb", nb2)


# =====================================================================
# 03 — Encoding Categorical Data
# =====================================================================
nb3 = header(
    "03 · Encoding Categorical Data",
    [
        "Tell nominal from ordinal — and why the distinction changes the encoder",
        "Apply Label, Ordinal, and One-Hot encoding correctly",
        "Use `OneHotEncoder` from sklearn (the version that handles unseen categories)",
        "Handle high-cardinality columns with frequency / target encoding (and avoid leakage)",
        "Wire encoders into a `ColumnTransformer` pipeline",
    ],
) + [
    md("""
    ## 1. Nominal vs ordinal

    - **Nominal** — categories with *no order*: `gender`, `city`, `payment_method`
    - **Ordinal** — categories with a *meaningful order*: `education` (HS < Bachelors < Masters < PhD), `contract_type` (Month-to-month < One year < Two year)

    Using a label encoder on a nominal column tells the model `Mumbai (0) < Delhi (1) < Bengaluru (2)` — which is nonsense and hurts most models.
    """),
    code("""
    df.select_dtypes(exclude="number").nunique()
    """),
    md("""
    ## 2. Label Encoding — for the **target** or true ordinal columns

    `LabelEncoder` was designed for **the target column `y`**, not for features. For features
    use `OrdinalEncoder` instead — it accepts a 2D array and lets you specify the order.
    """),
    code("""
    from sklearn.preprocessing import LabelEncoder

    le = LabelEncoder()
    y_enc = le.fit_transform(df["gender"])
    print("classes:", le.classes_)
    print("first 10:", y_enc[:10])
    """),
    md("""
    ## 3. Ordinal Encoding — for ordered categories with a known order

    Always pass `categories=` explicitly. The default alphabetic order will silently
    miscode `education` as `Bachelors=0, High School=1, Masters=2, PhD=3`.
    """),
    code("""
    from sklearn.preprocessing import OrdinalEncoder

    education_order = ["High School", "Bachelors", "Masters", "PhD"]
    contract_order  = ["Month-to-month", "One year", "Two year"]

    ord_enc = OrdinalEncoder(
        categories=[education_order, contract_order],
        handle_unknown="use_encoded_value", unknown_value=-1,
    )
    sample = df[["education", "contract_type"]].dropna().head(8)
    ord_enc.fit_transform(sample)
    """),
    md("""
    ## 4. One-Hot Encoding — for nominal columns

    Creates one binary column per category. The right default for nominal features fed to
    linear / distance / neural models. Tree models work fine with it too.

    Two common APIs:
    - `pd.get_dummies()` — quick and DataFrame-friendly
    - `sklearn.preprocessing.OneHotEncoder` — the production choice (handles unseen categories at inference time, plays nicely with pipelines)
    """),
    code("""
    pd.get_dummies(df["payment_method"], prefix="pay").head()
    """),
    code("""
    from sklearn.preprocessing import OneHotEncoder

    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    encoded = ohe.fit_transform(df[["gender", "city", "payment_method"]])
    pd.DataFrame(encoded, columns=ohe.get_feature_names_out()).head()
    """),
    md("""
    ### `drop="first"` — when and why

    For linear models with an intercept, the *k* one-hot columns are perfectly collinear
    (their sum is always 1). Drop one to avoid the **dummy variable trap**. For tree-based
    models, leaving all *k* in is fine and slightly more interpretable.
    """),
    code("""
    ohe_drop = OneHotEncoder(drop="first", sparse_output=False)
    ohe_drop.fit_transform(df[["gender", "contract_type"]])[:5]
    """),
    md("""
    ## 5. High-cardinality columns

    One-hot a column with 10,000 unique values and you have 10,000 new columns. Two
    common alternatives:

    ### Frequency encoding
    Replace each category with how often it appears. Simple, no leakage.
    """),
    code("""
    freq = df["city"].value_counts(normalize=True)
    df["city_freq"] = df["city"].map(freq)
    df[["city", "city_freq"]].head()
    """),
    md("""
    ### Target (mean) encoding — *with leakage warning*

    Replace each category with the mean of `y` for that category. Powerful but dangerous:
    if you compute the means on the full dataset, you've leaked the target into your features.

    **Always compute means on the training fold only**, ideally with cross-validated smoothing.
    """),
    code("""
    from sklearn.model_selection import train_test_split

    X = df.drop(columns=["customer_id", "churned"])
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    target_mean = y_train.groupby(X_train["city"]).mean()
    global_mean = y_train.mean()

    X_train["city_te"] = X_train["city"].map(target_mean)
    X_test["city_te"]  = X_test["city"].map(target_mean).fillna(global_mean)

    X_train[["city", "city_te"]].drop_duplicates().head()
    """),
    md("""
    ## 6. Putting it together — `ColumnTransformer`

    Real pipelines apply different encoders to different columns. `ColumnTransformer` is
    the clean way to express that.
    """),
    code("""
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler

    nominal_cols = ["gender", "city", "payment_method"]
    ordinal_cols = ["education", "contract_type"]
    numeric_cols = ["age", "tenure_months", "monthly_charges",
                    "total_charges", "estimated_salary",
                    "num_products", "has_credit_card", "is_active_member"]

    numeric_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale",  StandardScaler()),
    ])

    nominal_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("ohe",    OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    ordinal_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("ord",    OrdinalEncoder(
            categories=[education_order, contract_order],
            handle_unknown="use_encoded_value", unknown_value=-1)),
    ])

    pre = ColumnTransformer([
        ("num", numeric_pipe, numeric_cols),
        ("nom", nominal_pipe, nominal_cols),
        ("ord", ordinal_pipe, ordinal_cols),
    ])

    X_proc = pre.fit_transform(X_train.drop(columns=["city_te"]))
    print("Processed shape:", X_proc.shape)
    """),
    md("""
    ## 7. Cheat sheet

    | Column kind | Encoder |
    |-------------|---------|
    | Target / true ordinal | `LabelEncoder` (target) or `OrdinalEncoder` (features) |
    | Nominal, low cardinality (<~15) | `OneHotEncoder` |
    | Nominal, high cardinality | frequency or target encoding |
    | Linear model with intercept | `OneHotEncoder(drop="first")` |
    | Tree model | `OneHotEncoder()` (no drop) |

    ## Exercise
    1. Why does using `LabelEncoder` on `city` produce *worse* results than one-hot for
       a logistic regression, but make little difference for a random forest?
    2. Implement target encoding using *5-fold out-of-fold* means (no leakage). Hint:
       `KFold` + `groupby` inside the loop.
    """),
]
write_nb("03_encoding_categorical.ipynb", nb3)


# =====================================================================
# 04 — Scaling & Normalization
# =====================================================================
nb4 = header(
    "04 · Data Scaling & Normalization",
    [
        "Know which models need scaling and which don't",
        "Apply Min-Max, Standard (Z-score), Robust, and MaxAbs scalers",
        "See the difference visually on real columns",
        "Avoid the #1 mistake: fitting the scaler on the test set",
    ],
) + [
    md("""
    ## 1. Why scale?

    Many algorithms compute distances or use gradient descent. If `estimated_salary` ranges
    over 0–200,000 and `age` over 18–90, the salary column dominates everything.

    | Needs scaling | Doesn't care |
    |---------------|--------------|
    | KNN, K-means, SVM, PCA, neural nets, logistic regression with regularisation | Decision trees, random forests, gradient boosting |

    Tree-based models split on thresholds — they're invariant to monotonic rescaling.
    """),
    code("""
    cols = ["age", "tenure_months", "monthly_charges", "estimated_salary"]
    df[cols].describe().round(2)
    """),
    md("""
    ## 2. Min-Max scaling — squish to [0, 1]

    `x' = (x − min) / (max − min)`

    Preserves the shape of the original distribution. Sensitive to outliers — one extreme
    value pulls everything else into a narrow band.
    """),
    code("""
    from sklearn.preprocessing import MinMaxScaler

    mm = MinMaxScaler()
    X_mm = pd.DataFrame(mm.fit_transform(df[cols].fillna(df[cols].median())), columns=cols)
    X_mm.describe().round(3)
    """),
    md("""
    ## 3. Standardisation (Z-score)

    `x' = (x − mean) / std`

    Centres at 0, unit variance. Doesn't bound the output. The default choice for most
    linear models, SVMs, and neural nets.
    """),
    code("""
    from sklearn.preprocessing import StandardScaler

    ss = StandardScaler()
    X_ss = pd.DataFrame(ss.fit_transform(df[cols].fillna(df[cols].median())), columns=cols)
    X_ss.describe().round(3)
    """),
    md("""
    ## 4. Robust scaling

    `x' = (x − median) / IQR`

    Uses median + IQR instead of mean + std → unaffected by outliers. Great when you have
    extreme values you don't want to remove.
    """),
    code("""
    from sklearn.preprocessing import RobustScaler

    rs = RobustScaler()
    X_rs = pd.DataFrame(rs.fit_transform(df[cols].fillna(df[cols].median())), columns=cols)
    X_rs.describe().round(3)
    """),
    md("""
    ## 5. Visual comparison

    Look at `estimated_salary` (which has heavy outliers) under each scaler.
    """),
    code("""
    fig, axes = plt.subplots(1, 4, figsize=(16, 3.5))
    series = [
        ("Original",       df["estimated_salary"].fillna(df["estimated_salary"].median())),
        ("Min-Max",        X_mm["estimated_salary"]),
        ("Standardised",   X_ss["estimated_salary"]),
        ("Robust",         X_rs["estimated_salary"]),
    ]
    for ax, (title, s) in zip(axes, series):
        ax.hist(s, bins=40); ax.set_title(title)
    plt.tight_layout(); plt.show()
    """),
    md("""
    Notice how the Min-Max plot squashes everything to the left because of the outliers,
    while Robust keeps the bulk of the data spread out.

    ## 6. MaxAbs and Normalizer

    - **`MaxAbsScaler`** — divides by the maximum absolute value. Maps to [-1, 1] without
      shifting. Good for sparse data (it doesn't break sparsity).
    - **`Normalizer`** — scales each *row* (sample) to unit length. Different beast: useful
      for text vectors / cosine similarity, almost never for tabular data.
    """),
    code("""
    from sklearn.preprocessing import MaxAbsScaler, Normalizer

    MaxAbsScaler().fit_transform(df[cols].fillna(0))[:3]
    """),
    md("""
    ## 7. The #1 mistake — leaking through the scaler

    ```python
    # WRONG — fits on whole dataset, leaks test stats into training
    X_scaled = StandardScaler().fit_transform(X)
    X_train, X_test = train_test_split(X_scaled, ...)

    # RIGHT — fit on train only, transform both
    X_train, X_test = train_test_split(X, ...)
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test  = scaler.transform(X_test)
    ```

    The cleanest version is to put the scaler inside a `Pipeline` so it's fit per
    cross-validation fold automatically.
    """),
    code("""
    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score

    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("clf",   LogisticRegression(max_iter=1000)),
    ])

    X_num = df[cols].fillna(df[cols].median())
    scores = cross_val_score(pipe, X_num, df["churned"], cv=5, scoring="roc_auc")
    print(f"ROC-AUC: {scores.mean():.3f}  ± {scores.std():.3f}")
    """),
    md("""
    ## 8. Cheat sheet

    | Scenario | Use |
    |----------|-----|
    | Default for most ML | `StandardScaler` |
    | Bounded output needed (neural nets, image-like) | `MinMaxScaler` |
    | Outliers present, can't remove | `RobustScaler` |
    | Sparse data (text, recommender) | `MaxAbsScaler` |
    | Tree-based model | none — skip scaling |

    ## Exercise
    1. Train KNN on the dataset *without* scaling, then *with* `StandardScaler`.
       Compare ROC-AUC. Why is the difference so large?
    2. Repeat with a `RandomForestClassifier`. Explain why the difference is tiny.
    """),
]
write_nb("04_scaling_normalization.ipynb", nb4)


# =====================================================================
# 05 — Feature Selection & Feature Engineering
# =====================================================================
nb5 = header(
    "05 · Feature Selection & Feature Engineering",
    [
        "Engineer new features from domain knowledge (ratios, bins, flags)",
        "Use filter, wrapper, and embedded methods to *select* features",
        "Read tree-based feature importance correctly (and its limits)",
        "Use L1 (Lasso) regularisation as automatic selection",
    ],
) + [
    md("""
    ## Part A — Feature Engineering

    Often the single biggest lever in a tabular project. The model can only see the columns
    you give it; if the right transform isn't there, the model can't learn it well.

    ### 1. Domain-driven features
    Combinations and ratios that capture business meaning.
    """),
    code("""
    feats = df.copy()
    feats["tenure_years"]      = feats["tenure_months"] / 12
    feats["charges_per_month"] = feats["total_charges"] / feats["tenure_months"].replace(0, np.nan)
    feats["high_value"]        = (feats["monthly_charges"] > feats["monthly_charges"].quantile(0.75)).astype(int)
    feats["new_customer"]      = (feats["tenure_months"] <= 6).astype(int)

    feats[["tenure_months", "tenure_years", "monthly_charges",
           "charges_per_month", "high_value", "new_customer"]].head()
    """),
    md("""
    ### 2. Binning continuous variables

    Useful when the relationship with the target is non-linear and you're using a linear
    model. `pd.cut` for fixed bins, `pd.qcut` for quantile-based bins.
    """),
    code("""
    feats["age_group"] = pd.cut(
        feats["age"],
        bins=[0, 25, 35, 50, 65, 100],
        labels=["<25", "25-34", "35-49", "50-64", "65+"],
    )
    feats["age_group"].value_counts().sort_index()
    """),
    md("""
    ### 3. Interaction features
    Sometimes two columns matter only in combination.
    """),
    code("""
    feats["active_x_contract"] = feats["is_active_member"].astype(str) + "_" + feats["contract_type"]
    feats["active_x_contract"].value_counts()
    """),
    md("""
    ### 4. Log / power transforms
    For long-tailed numeric features. Already covered in notebook 02 — bring it back into
    your engineering toolkit.
    """),
    code("""
    feats["log_estimated_salary"] = np.log1p(feats["estimated_salary"])
    """),
    md("""
    ---
    ## Part B — Feature Selection

    Three families:

    - **Filter** — score each feature against the target, keep the top ones. Cheap, model-agnostic.
    - **Wrapper** — train a model on different feature subsets. Expensive but accurate.
    - **Embedded** — selection happens *inside* the model (Lasso, tree importances).
    """),
    code("""
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.model_selection import train_test_split

    X = df.drop(columns=["customer_id", "churned"])
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    numeric_cols = X.select_dtypes(include="number").columns.tolist()
    cat_cols     = X.select_dtypes(exclude="number").columns.tolist()

    pre = ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                          ("sc",  StandardScaler())]),
         numeric_cols),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh",  OneHotEncoder(handle_unknown="ignore", sparse_output=False))]),
         cat_cols),
    ])
    X_train_p = pre.fit_transform(X_train)
    X_test_p  = pre.transform(X_test)
    feat_names = pre.get_feature_names_out()
    print("Total features after preprocessing:", X_train_p.shape[1])
    """),
    md("""
    ### 5. Filter — Variance Threshold
    Drops near-constant features (no information to learn from).
    """),
    code("""
    from sklearn.feature_selection import VarianceThreshold

    vt = VarianceThreshold(threshold=0.01)
    X_vt = vt.fit_transform(X_train_p)
    print(f"{X_train_p.shape[1]}  →  {X_vt.shape[1]} features (dropped near-constants)")
    """),
    md("""
    ### 6. Filter — Univariate (ANOVA F / mutual information)
    """),
    code("""
    from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif

    skb = SelectKBest(score_func=f_classif, k=15).fit(X_train_p, y_train)
    top = pd.Series(skb.scores_, index=feat_names).sort_values(ascending=False).head(15)
    top.round(2)
    """),
    md("""
    ### 7. Filter — Correlation
    Drop highly correlated numeric features (one of each redundant pair).
    """),
    code("""
    corr = pd.DataFrame(X_train_p, columns=feat_names).corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    to_drop = [c for c in upper.columns if (upper[c] > 0.9).any()]
    print("Highly correlated features to drop:", to_drop)
    """),
    md("""
    ### 8. Wrapper — Recursive Feature Elimination (RFE)
    Trains a model, drops the weakest feature, repeats. Slower but uses model performance
    directly.
    """),
    code("""
    from sklearn.feature_selection import RFE
    from sklearn.linear_model import LogisticRegression

    rfe = RFE(LogisticRegression(max_iter=1000), n_features_to_select=10)
    rfe.fit(X_train_p, y_train)
    selected = pd.Series(feat_names)[rfe.support_].tolist()
    print("RFE chose:", selected)
    """),
    md("""
    ### 9. Embedded — tree-based importance

    Random forest gives one importance per feature based on how much it reduces impurity.
    Fast and respects interactions.

    **Watch out**: importance is biased toward high-cardinality features. Always sanity-check
    against permutation importance for the model you actually care about.
    """),
    code("""
    from sklearn.ensemble import RandomForestClassifier

    rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    rf.fit(X_train_p, y_train)

    imp = pd.Series(rf.feature_importances_, index=feat_names).sort_values(ascending=True).tail(15)
    imp.plot(kind="barh", figsize=(7, 5)); plt.title("Top 15 features (Random Forest)")
    plt.tight_layout(); plt.show()
    """),
    md("""
    ### 10. Embedded — L1 (Lasso) regularisation
    Shrinks unimportant coefficients to *exactly zero* — selection comes for free.
    """),
    code("""
    from sklearn.linear_model import LogisticRegression

    lasso = LogisticRegression(penalty="l1", solver="saga", C=0.3, max_iter=2000)
    lasso.fit(X_train_p, y_train)

    coef = pd.Series(lasso.coef_[0], index=feat_names)
    print("Non-zero coefficients:", (coef != 0).sum(), "of", len(coef))
    coef[coef != 0].sort_values(key=abs, ascending=False).head(10)
    """),
    md("""
    ### 11. Permutation importance — the trustworthy one
    Shuffles one feature at a time and measures how much performance drops. Slower but
    unbiased and works for any model.
    """),
    code("""
    from sklearn.inspection import permutation_importance

    perm = permutation_importance(rf, X_test_p, y_test, n_repeats=5,
                                  random_state=42, n_jobs=-1)
    pd.Series(perm.importances_mean, index=feat_names).sort_values(ascending=True).tail(10) \\
       .plot(kind="barh", figsize=(7, 4)); plt.title("Permutation importance (top 10)")
    plt.tight_layout(); plt.show()
    """),
    md("""
    ## Cheat sheet

    | Goal | Technique |
    |------|-----------|
    | Drop dead-weight features fast | `VarianceThreshold` |
    | Quick numeric ranking | `SelectKBest(f_classif)` / mutual info |
    | Remove redundant features | correlation filter (>0.9) |
    | Best subset, slow | RFE / forward / backward |
    | Linear model selection | L1 (Lasso) |
    | Honest importance for any model | permutation importance |

    ## Exercise
    1. Pick the top-10 features from L1 vs RFE vs RF importance. How much do the three lists overlap?
    2. Engineer two new features you think should help. Re-run RF importance — did they make the cut?
    """),
]
write_nb("05_feature_selection_engineering.ipynb", nb5)


# =====================================================================
# 06 — Imbalanced Data
# =====================================================================
nb6 = header(
    "06 · Handling Imbalanced Data",
    [
        "See why accuracy lies on imbalanced problems — and what to use instead",
        "Apply random oversampling, undersampling, and SMOTE / SMOTENC / ADASYN",
        "Use `class_weight` as a one-line alternative to resampling",
        "Combine over- and under-sampling (SMOTEENN, SMOTETomek)",
        "Resample **only on the training fold** — the most common bug in this area",
    ],
) + [
    md("""
    > Requires the `imbalanced-learn` package.
    > `pip install imbalanced-learn` if you haven't already.
    """),
    code("""
    df["churned"].value_counts(normalize=True).round(3)
    """),
    md("""
    ## 1. Why accuracy is misleading

    Predict "no churn" for everyone on a 9% churn dataset → 91% accuracy. Useless model.

    What to use instead:
    - **Confusion matrix** — see TP/FP/TN/FN directly
    - **Precision** — of those we flagged, how many were right
    - **Recall (sensitivity)** — of the real churners, how many did we catch
    - **F1** — harmonic mean of precision and recall
    - **ROC-AUC** — overall ranking quality
    - **PR-AUC** — preferred over ROC-AUC when the positive class is rare
    """),
    code("""
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (classification_report, confusion_matrix,
                                  roc_auc_score, average_precision_score)

    X = df.drop(columns=["customer_id", "churned"])
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    num_cols = X.select_dtypes(include="number").columns.tolist()
    cat_cols = X.select_dtypes(exclude="number").columns.tolist()

    pre = ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                          ("sc",  StandardScaler())]), num_cols),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh",  OneHotEncoder(handle_unknown="ignore", sparse_output=False))]),
         cat_cols),
    ])
    X_train_p = pre.fit_transform(X_train)
    X_test_p  = pre.transform(X_test)

    def evaluate(name, model):
        proba = model.predict_proba(X_test_p)[:, 1]
        pred  = (proba >= 0.5).astype(int)
        print(f"--- {name} ---")
        print(confusion_matrix(y_test, pred))
        print(f"ROC-AUC: {roc_auc_score(y_test, proba):.3f}   "
              f"PR-AUC: {average_precision_score(y_test, proba):.3f}")
        print(classification_report(y_test, pred, digits=3))

    baseline = LogisticRegression(max_iter=1000).fit(X_train_p, y_train)
    evaluate("Baseline (no resampling)", baseline)
    """),
    md("""
    ## 2. The cheapest fix — `class_weight="balanced"`

    The model penalises mistakes on the minority class more during training. Often as good
    as resampling, with no extra plumbing.
    """),
    code("""
    weighted = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_train_p, y_train)
    evaluate("class_weight='balanced'", weighted)
    """),
    md("""
    ## 3. Random Oversampling

    Duplicate minority class samples until the classes are balanced. Risk: the same rows
    appear many times → models can memorise them and overfit.
    """),
    code("""
    from imblearn.over_sampling import RandomOverSampler

    ros = RandomOverSampler(random_state=42)
    X_ros, y_ros = ros.fit_resample(X_train_p, y_train)
    print("After ROS:", np.bincount(y_ros))
    evaluate("Random Oversampling", LogisticRegression(max_iter=1000).fit(X_ros, y_ros))
    """),
    md("""
    ## 4. SMOTE — Synthetic Minority Oversampling

    Instead of duplicating, SMOTE *creates new* minority samples by interpolating between
    existing ones and their nearest neighbours. The default modern choice for tabular
    imbalance.

    ⚠ SMOTE works on **numeric** features. For mixed numeric+categorical, use **SMOTENC**.
    """),
    code("""
    from imblearn.over_sampling import SMOTE

    smote = SMOTE(random_state=42, k_neighbors=5)
    X_sm, y_sm = smote.fit_resample(X_train_p, y_train)
    print("After SMOTE:", np.bincount(y_sm))
    evaluate("SMOTE", LogisticRegression(max_iter=1000).fit(X_sm, y_sm))
    """),
    md("""
    ## 5. ADASYN

    Like SMOTE but generates more synthetic samples *near hard-to-classify* minority points
    (those near the decision boundary). Sometimes helps, sometimes hurts.
    """),
    code("""
    from imblearn.over_sampling import ADASYN

    ada = ADASYN(random_state=42)
    X_ad, y_ad = ada.fit_resample(X_train_p, y_train)
    evaluate("ADASYN", LogisticRegression(max_iter=1000).fit(X_ad, y_ad))
    """),
    md("""
    ## 6. Random Undersampling

    Drop majority class samples until balanced. Fast, but you throw away information.
    Useful when the dataset is huge and the majority class is highly redundant.
    """),
    code("""
    from imblearn.under_sampling import RandomUnderSampler

    rus = RandomUnderSampler(random_state=42)
    X_rus, y_rus = rus.fit_resample(X_train_p, y_train)
    print("After RUS:", np.bincount(y_rus))
    evaluate("Random Undersampling", LogisticRegression(max_iter=1000).fit(X_rus, y_rus))
    """),
    md("""
    ## 7. Tomek Links and SMOTEENN

    - **Tomek links** remove ambiguous pairs at the class boundary → cleaner separation.
    - **SMOTEENN** = SMOTE + Edited Nearest Neighbours: oversamples the minority then
      cleans up noisy synthetic points. Often the best single recipe.
    """),
    code("""
    from imblearn.combine import SMOTEENN

    smen = SMOTEENN(random_state=42)
    X_se, y_se = smen.fit_resample(X_train_p, y_train)
    print("After SMOTEENN:", np.bincount(y_se))
    evaluate("SMOTEENN", LogisticRegression(max_iter=1000).fit(X_se, y_se))
    """),
    md("""
    ## 8. The critical rule — resample only on the training fold

    Resampling the whole dataset before splitting **leaks** synthetic / duplicated samples
    into the test set → optimistic, useless metrics.

    The right way is `imblearn.pipeline.Pipeline` (note: `imblearn`'s pipeline, not
    `sklearn`'s — only the imblearn one is aware of resamplers and runs them only on training data).
    """),
    code("""
    from imblearn.pipeline import Pipeline as ImbPipeline
    from sklearn.model_selection import cross_val_score, StratifiedKFold

    pipe = ImbPipeline([
        ("pre",   pre),
        ("smote", SMOTE(random_state=42)),
        ("clf",   LogisticRegression(max_iter=1000)),
    ])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(pipe, X, y, cv=cv, scoring="average_precision", n_jobs=-1)
    print(f"PR-AUC (CV): {scores.mean():.3f}  ± {scores.std():.3f}")
    """),
    md("""
    ## 9. Threshold tuning — often more impactful than resampling

    The default threshold of 0.5 is rarely optimal on imbalanced data. Sweep thresholds
    and pick one that matches your business cost (e.g. you care about recall ≥ 0.8).
    """),
    code("""
    from sklearn.metrics import precision_recall_curve

    proba = baseline.predict_proba(X_test_p)[:, 1]
    prec, rec, thr = precision_recall_curve(y_test, proba)

    plt.figure(figsize=(7, 4))
    plt.plot(thr, prec[:-1], label="precision")
    plt.plot(thr, rec[:-1],  label="recall")
    plt.xlabel("threshold"); plt.ylabel("score"); plt.legend(); plt.title("Precision–Recall vs threshold")
    plt.show()
    """),
    md("""
    ## 10. Cheat sheet

    | Situation | First thing to try |
    |-----------|---------------------|
    | Slight imbalance (30/70) | nothing — just use proper metrics |
    | Moderate imbalance | `class_weight="balanced"` |
    | Strong imbalance, numeric features | SMOTE |
    | Strong imbalance, mixed features | SMOTENC |
    | Huge dataset, redundant majority | random undersampling |
    | Noisy boundary | SMOTEENN / SMOTETomek |
    | Always | tune the decision threshold |

    ## Exercise
    1. Repeat the comparison with a `RandomForestClassifier`. Does SMOTE still help, or
       does `class_weight="balanced_subsample"` already do the job?
    2. Replace the metric in `cross_val_score` with `f1`. Does the ranking of methods change?
    """),
]
write_nb("06_handling_imbalanced_data.ipynb", nb6)


# =====================================================================
# README
# =====================================================================
print("All notebooks written.")
