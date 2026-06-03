# Machine Learning Algorithms — Student Notes

> Covers: Logistic Regression · KNN · Decision Tree · Random Forest · SVM · Linear Regression · Lasso · Ridge · Polynomial Regression · Bagging · AdaBoost · Gradient Boosting · XGBoost

---

## Table of Contents

1. [Logistic Regression](#1-logistic-regression)
2. [K-Nearest Neighbors (KNN)](#2-k-nearest-neighbors-knn)
3. [Decision Tree](#3-decision-tree)
4. [Random Forest](#4-random-forest)
5. [Support Vector Machine (SVM)](#5-support-vector-machine-svm)
6. [Linear Regression](#6-linear-regression)
7. [Ridge Regression (L2)](#7-ridge-regression-l2)
8. [Lasso Regression (L1)](#8-lasso-regression-l1)
9. [Polynomial Regression](#9-polynomial-regression)
10. [Master Comparison Table](#10-master-comparison-table)
11. [When to Use What](#11-when-to-use-what)
12. [Bagging](#12-bagging)
13. [AdaBoost](#13-adaboost)
14. [Gradient Boosting](#14-gradient-boosting)
15. [XGBoost](#15-xgboost)
16. [Ensemble Family — Full Comparison](#16-ensemble-family--full-comparison)

---

## 1. Logistic Regression

### What It Does
Predicts a **probability (0 to 1)** for binary classification problems using the sigmoid function.

### How It Works — Steps

| Step | Action |
|------|--------|
| 1 | Compute linear combination: `z = w₀ + w₁x₁ + ... + wₙxₙ` |
| 2 | Apply sigmoid: `σ(z) = 1 / (1 + e^(-z))` |
| 3 | Apply threshold: predict 1 if `σ(z) ≥ 0.5`, else 0 |
| 4 | Compute Binary Cross-Entropy Loss |
| 5 | Update weights via Gradient Descent |
| 6 | Repeat until convergence |

### Key Formula
```
Loss = -1/m · Σ [ y·log(ŷ) + (1-y)·log(1-ŷ) ]
```

### Sigmoid Function Behavior
| z | σ(z) |
|---|------|
| Very negative | ≈ 0.0 |
| 0 | = 0.5 |
| Very positive | ≈ 1.0 |

### Key Points
- Decision boundary is **linear**
- Feature scaling **recommended**
- Outputs interpretable **coefficients**
- Use when relationship between features and log-odds is linear

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Highly interpretable | Only linear boundaries |
| Fast training & prediction | Assumes no multicollinearity |
| Outputs probabilities natively | Poor with complex relationships |
| Low overfitting risk | Sensitive to outliers |

---

## 2. K-Nearest Neighbors (KNN)

### What It Does
Makes predictions by finding the **K most similar training samples** and aggregating their labels.

### How It Works — Steps

| Step | Action |
|------|--------|
| 1 | Store all training data (no training phase) |
| 2 | Receive new data point |
| 3 | Compute distance to all training points |
| 4 | Sort and select K nearest neighbors |
| 5 | Classification → majority vote; Regression → average |

### Distance Metrics
| Metric | Formula | Use When |
|--------|---------|----------|
| Euclidean | `√Σ(aᵢ-bᵢ)²` | Continuous features (default) |
| Manhattan | `Σ|aᵢ-bᵢ|` | High dimensions, robust to outliers |
| Minkowski | `(Σ|aᵢ-bᵢ|ᵖ)^(1/p)` | Generalization of both |
| Hamming | % differing bits | Categorical / text data |

### Choosing K
| Small K | Large K |
|---------|---------|
| Low bias, high variance | High bias, low variance |
| Overfits | Underfits |
| Sensitive to noise | Ignores local patterns |

- Use **odd K** to avoid ties
- Start with `K = √n` as a rule of thumb
- Tune with **cross-validation**

### Key Points
- **Lazy learner** — no training, all work at prediction time
- Feature scaling is **critical** (distances are distorted otherwise)
- Suffers from **curse of dimensionality** in high dimensions
- Prediction time: O(n) — slow on large datasets

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Simple, no training time | Slow prediction O(n) |
| Handles multi-class naturally | High memory usage |
| Non-parametric | Feature scaling mandatory |
| Adapts instantly to new data | Fails in high dimensions |

---

## 3. Decision Tree

### What It Does
Builds a **flowchart of yes/no questions** about features to reach a prediction.

### Structure
```
Root Node → asks first question
Internal Nodes → ask further questions
Leaf Nodes → final predictions
```

### How It Works — Steps

| Step | Action |
|------|--------|
| 1 | At each node, evaluate all features and thresholds |
| 2 | Select split that maximizes purity gain |
| 3 | Split data into child nodes |
| 4 | Repeat recursively on each child |
| 5 | Stop when stopping criteria met |
| 6 | Assign majority class (or mean) to each leaf |

### Splitting Criteria
| Metric | Formula | Used For |
|--------|---------|----------|
| Gini Impurity | `1 - Σ pᵢ²` | Classification (default) |
| Information Gain | `H(parent) - avg H(children)` | Classification |
| MSE Reduction | Minimize child node MSE | Regression |

### Entropy Formula
```
H = -Σ pᵢ · log₂(pᵢ)

Pure node (one class)  → H = 0   (best)
50/50 split            → H = 1   (worst)
```

### Stopping Criteria
| Parameter | Controls |
|-----------|----------|
| `max_depth` | Maximum tree depth |
| `min_samples_split` | Min samples needed to split |
| `min_samples_leaf` | Min samples in a leaf |
| `min_impurity_decrease` | Min gain required to split |

### Pruning
- **Pre-pruning** — set constraints before training (`max_depth`, `min_samples_leaf`)
- **Post-pruning** — grow full tree then remove weak branches (`ccp_alpha`)

### Key Points
- No feature scaling needed
- High overfitting risk without pruning
- Provides **feature importance** rankings
- Splits are **axis-aligned** only
- Foundation of ensemble methods (Random Forest, XGBoost)

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Highly interpretable | Prone to overfitting |
| No feature scaling needed | High variance |
| Handles non-linearity | Biased toward high-cardinality features |
| Built-in feature importance | Axis-aligned splits only |

---

## 4. Random Forest

### What It Does
Builds **many diverse decision trees** and combines their predictions — reducing variance and overfitting.

### Two Sources of Randomness
1. **Bootstrap Sampling** — each tree trains on a random sample (with replacement) of the data
2. **Feature Subsampling** — at each split, only a random subset of features is considered

### How It Works — Steps

| Step | Action |
|------|--------|
| 1 | For each of N trees: draw bootstrap sample |
| 2 | At each node: randomly select `√p` features |
| 3 | Find best split among selected features only |
| 4 | Grow tree fully (or to max_depth) |
| 5 | Repeat for all N trees |
| 6 | Aggregate predictions across all trees |

### Aggregation
| Task | Method |
|------|--------|
| Classification | Majority vote across all trees |
| Regression | Average prediction across all trees |

### Out-of-Bag (OOB) Error
- ~37% of data is not used for each tree (OOB samples)
- These act as a **free validation set** per tree
- OOB error ≈ cross-validation score without extra computation

### Error Decomposition
```
Ensemble Error = Bias² + Variance/N + Irreducible Error
                              ↑
                  shrinks as number of trees grows
```

### Key Hyperparameters
| Parameter | What it Controls | Typical Values |
|-----------|-----------------|----------------|
| `n_estimators` | Number of trees | 100–500 |
| `max_depth` | Max depth per tree | 5–30, or None |
| `max_features` | Features per split | `sqrt`, `log2` |
| `min_samples_leaf` | Min leaf samples | 1–10 |
| `oob_score` | Enable OOB evaluation | True/False |

### Bagging vs Random Forest
| | Bagging | Random Forest |
|--|---------|---------------|
| Bootstrap sampling | Yes | Yes |
| Feature subsampling at splits | No | **Yes** ← key difference |
| Tree correlation | Higher | Lower (more diverse) |
| Performance | Good | Better |

### Key Points
- No feature scaling needed
- Rarely overfits
- Memory-heavy (stores all trees)
- Reliable feature importance (averaged over many trees)
- Building block for XGBoost, AdaBoost, LightGBM

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Low overfitting risk | Slower training and prediction |
| No feature scaling needed | Less interpretable |
| Robust to noise and outliers | High memory usage |
| Free OOB validation | Not ideal for sparse high-dim data |
| Reliable feature importance | Can't extrapolate beyond training range |

---

## 5. Support Vector Machine (SVM)

### What It Does
Finds the **hyperplane with maximum margin** between classes. Uses kernels to handle non-linear data.

### How It Works — Steps

| Step | Action |
|------|--------|
| 1 | Find hyperplane that separates classes |
| 2 | Maximize the margin between classes |
| 3 | Identify support vectors (closest points to boundary) |
| 4 | Allow margin violations via slack (soft margin) |
| 5 | Use kernel to handle non-linear data |
| 6 | Predict: sign of `w·x + b` |

### Key Concepts

**Decision boundary:** `w · x + b = 0`

**Margin width:** `2 / ||w||` — SVM maximizes this

**Support Vectors:** only training points that define the boundary — removing others doesn't change the model

### Hard vs Soft Margin
| | Hard Margin | Soft Margin |
|--|-------------|-------------|
| Violations allowed | None | Yes (with penalty C) |
| Works when | Perfectly separable | Real-world noisy data |
| Risk | Fails if not separable | Controlled by C |

### The C Hyperparameter
```
Small C                     Large C
───────────────             ───────────────
Wide margin                 Narrow margin
More violations OK          Few violations
Underfits                   Overfits
Better generalization       Fits training tightly
```

### Kernel Trick
Maps data to higher dimensions where linear separation is possible — without computing the transformation explicitly.

```
K(xᵢ, xⱼ) = φ(xᵢ) · φ(xⱼ)
```

### Common Kernels
| Kernel | Formula | Use When |
|--------|---------|----------|
| Linear | `xᵢ · xⱼ` | High-dim text, linearly separable |
| RBF (Gaussian) | `exp(-γ‖xᵢ-xⱼ‖²)` | Default, handles any shape |
| Polynomial | `(γ xᵢ·xⱼ + r)^d` | Image data |
| Sigmoid | `tanh(γ xᵢ·xⱼ + r)` | Rarely used |

### Gamma (γ) for RBF Kernel
```
Small γ                     Large γ
───────────────             ───────────────
Far reach per point         Close reach per point
Smoother boundary           Wiggly boundary
Underfits                   Overfits
```

### Key Hyperparameters
| Parameter | Controls | Typical Values |
|-----------|----------|----------------|
| `C` | Margin softness | 0.01, 0.1, 1, 10, 100 |
| `kernel` | Transformation type | `rbf`, `linear`, `poly` |
| `gamma` | RBF influence radius | `scale`, `auto`, float |
| `degree` | Polynomial degree | 2, 3, 4 |

### SVM for Regression (SVR)
- Fits data within an **ε-tube**
- Points inside tube → no penalty
- Points outside tube → penalized
- Only points outside tube are support vectors

### Key Points
- Feature scaling is **mandatory**
- Memory efficient — stores only support vectors
- Slow on large datasets: O(n²) to O(n³)
- Excellent for high-dimensional data (text, genes)
- Does not output probabilities natively (use `probability=True` to enable via cross-validation)

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Excellent in high dimensions | Very slow on large datasets |
| Memory efficient | Feature scaling mandatory |
| Handles non-linearity via kernels | Hard to interpret |
| Strong theoretical foundation | Kernel/C/γ tuning is tricky |
| Robust in high-dim, small-sample | No native probability output |

---

## 6. Linear Regression

### What It Does
Predicts a **continuous numeric value** by fitting a straight line (or hyperplane) through the data that minimizes the total prediction error.

> Core idea: **"Find the best-fit line that minimizes the distance between predictions and actual values."**

### How It Works — Steps

| Step | Action |
|------|--------|
| 1 | Assume a linear relationship: `ŷ = w₀ + w₁x₁ + ... + wₙxₙ` |
| 2 | Compute predictions for all training samples |
| 3 | Calculate MSE loss between predictions and true values |
| 4 | Update weights via Gradient Descent (or solve analytically) |
| 5 | Repeat until weights converge |

### Key Formulas

**Prediction:**
```
ŷ = w₀ + w₁x₁ + w₂x₂ + ... + wₙxₙ
```

**Loss — Mean Squared Error (MSE):**
```
MSE = 1/m · Σ (yᵢ - ŷᵢ)²
```

**Analytical Solution (Normal Equation):**
```
w = (XᵀX)⁻¹ Xᵀy
```
Works for small datasets. For large datasets, use Gradient Descent instead.

### Gradient Descent Weight Update
```
w = w - α · (∂MSE/∂w)
  = w - α · (2/m) · Xᵀ(ŷ - y)

α = learning rate
```

### Evaluation Metrics

| Metric | Formula | Meaning |
|--------|---------|---------|
| **MAE** | `1/m · Σ|yᵢ - ŷᵢ|` | Average absolute error |
| **MSE** | `1/m · Σ(yᵢ - ŷᵢ)²` | Penalizes large errors more |
| **RMSE** | `√MSE` | Same units as target variable |
| **R²** | `1 - SS_res/SS_tot` | % variance explained (1.0 = perfect) |

### Assumptions of Linear Regression
1. **Linearity** — relationship between features and target is linear
2. **Independence** — observations are independent of each other
3. **Homoscedasticity** — residuals have constant variance
4. **Normality** — residuals are normally distributed
5. **No multicollinearity** — features are not highly correlated with each other

### Key Points
- Simple and highly interpretable
- Each coefficient = change in ŷ for 1-unit change in that feature (others fixed)
- Sensitive to **outliers** (MSE squares the errors)
- Use **MAE** loss instead if outliers are a concern
- Feature scaling recommended (for gradient descent convergence speed)

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Highly interpretable coefficients | Assumes linear relationship |
| Fast training and prediction | Sensitive to outliers |
| No hyperparameters (base form) | Fails with multicollinearity |
| Good baseline model | Underfits complex data |

---

## 7. Ridge Regression (L2)

### What It Does
Linear regression with an **L2 penalty** on the coefficients — shrinks all weights toward zero to reduce overfitting.

> Core idea: **"Penalize large weights so the model doesn't rely too heavily on any single feature."**

### How It Works

Ridge adds a penalty term to the MSE loss:

```
Ridge Loss = MSE + λ · Σ wᵢ²
                   ↑
              L2 penalty (sum of squared weights)
```

**Analytical solution:**
```
w = (XᵀX + λI)⁻¹ Xᵀy
```
The `λI` term makes the matrix always invertible — even when features are correlated (solving multicollinearity).

### Effect of Lambda (λ)

```
λ = 0                      λ → ∞
──────────────             ──────────────
Pure Linear Regression     All weights → 0
No regularization          Severe underfitting
Overfits if high dims       Useless model

← find the sweet spot via cross-validation →
```

### What Ridge Does to Coefficients

```
Feature:       w (no reg)    w (Ridge λ=1)   w (Ridge λ=10)
─────────────────────────────────────────────────────────
Monthly Charges    4.2           3.1              1.8
Tenure            -3.8          -2.9             -1.5
Contract          2.1            1.7              0.9
```

Ridge **shrinks all coefficients** — but never sets them exactly to zero.

### When to Use Ridge
- Many features, all somewhat relevant
- Multicollinearity present (correlated features)
- Want to keep all features but reduce their impact

### Key Hyperparameter
| Parameter | Controls | Values to try |
|-----------|----------|---------------|
| `alpha` (λ) | Strength of penalty | 0.01, 0.1, 1, 10, 100 |

Always use **RidgeCV** to find best alpha via cross-validation.

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Handles multicollinearity well | Does not perform feature selection |
| Reduces overfitting | Keeps all features (even irrelevant ones) |
| Stable solution always exists | Less interpretable than plain linear regression |
| Works well when all features matter | Requires feature scaling |

---

## 8. Lasso Regression (L1)

### What It Does
Linear regression with an **L1 penalty** — shrinks weights toward zero and can set some **exactly to zero**, performing automatic feature selection.

> Core idea: **"Penalize large weights AND eliminate irrelevant features entirely."**

### How It Works

Lasso adds an L1 penalty to MSE loss:

```
Lasso Loss = MSE + λ · Σ |wᵢ|
                    ↑
              L1 penalty (sum of absolute weights)
```

**No closed-form solution** — uses iterative methods (coordinate descent).

### Lasso vs Ridge — Key Difference

```
Ridge (L2):  penalizes w²  → shrinks toward 0, never exactly 0
Lasso (L1):  penalizes |w| → can set weights to EXACTLY 0
                              ↑
                     Built-in feature selection!
```

**Why does L1 produce zeros?** Geometry:

```
Ridge constraint: circle (smooth → touches axis rarely)
Lasso constraint: diamond (corners on axes → solution lands on corner = zero weight)
```

### Effect of Lambda (λ) on Lasso

```
Feature:       w (no reg)    w (Lasso λ=1)   w (Lasso λ=10)
─────────────────────────────────────────────────────────
Monthly Charges    4.2           2.8              1.2
Tenure            -3.8          -1.5              0.0  ← eliminated!
Contract          2.1            0.0              0.0  ← eliminated!
Irrelevant feat    0.3           0.0              0.0  ← eliminated!
```

### When to Use Lasso
- Many features but only a few are actually relevant
- Want automatic feature selection built into the model
- Need a sparse, interpretable model

### Lasso vs Ridge — Side by Side

| | Ridge (L2) | Lasso (L1) |
|--|------------|------------|
| Penalty | `λ · Σ wᵢ²` | `λ · Σ |wᵢ|` |
| Shrinks weights | Yes, toward 0 | Yes, to exactly 0 |
| Feature selection | No | **Yes** |
| Best when | All features relevant, multicollinearity | Few relevant features, want sparse model |
| Solution | Closed-form exists | Iterative (coordinate descent) |
| Stable with correlated features | Yes | No (picks one, ignores others) |

### Elastic Net — Best of Both
Combines L1 + L2 penalty:
```
Elastic Net Loss = MSE + λ₁·Σ|wᵢ| + λ₂·Σwᵢ²
```
- Does feature selection (like Lasso)
- Stable with correlated features (like Ridge)
- Controlled by `l1_ratio` parameter

### Key Hyperparameter
| Parameter | Controls | Values to try |
|-----------|----------|---------------|
| `alpha` (λ) | Strength of penalty | 0.001, 0.01, 0.1, 1, 10 |

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Automatic feature selection | Unstable with correlated features (picks arbitrarily) |
| Produces sparse models | No closed-form solution (slower) |
| More interpretable output | Can underfit with too many features eliminated |
| Useful when features >> samples | Requires feature scaling |

---

## 9. Polynomial Regression

### What It Does
Extends linear regression to capture **curved, non-linear relationships** by adding polynomial terms of the original features.

> Core idea: **"Transform features into higher powers, then apply linear regression on the transformed features."**

### How It Works — Steps

| Step | Action |
|------|--------|
| 1 | Take original features `x` |
| 2 | Create polynomial features: `x, x², x³, ..., xᵈ` |
| 3 | Run standard linear regression on the expanded feature set |
| 4 | The model is still LINEAR in the coefficients — just non-linear in the inputs |

### Example — Degree 2

```
Original feature: x = [tenure]

After PolynomialFeatures(degree=2):
  [1,  x,  x²]
  [1, tenure, tenure²]

Model: ŷ = w₀ + w₁·tenure + w₂·tenure²
           ↑
     Captures U-shaped or curved relationships
```

### Effect of Degree

```
Degree 1 (Linear):    straight line            → underfits curved data
Degree 2 (Quadratic): one curve (U or ∩)       → fits gentle curves
Degree 3 (Cubic):     one inflection point      → fits S-shaped curves
Degree N (High):      wiggly, passes all points → overfits!
```

### Bias-Variance Tradeoff with Degree

```
Low Degree                         High Degree
──────────────────                 ──────────────────
High bias                          High variance
Underfits                          Overfits
Misses curve in data               Memorizes training noise
Good generalization                Poor generalization
```

### How to Choose Degree
- Plot **learning curves** — training vs validation error vs degree
- Use **cross-validation** to find optimal degree
- Keep it as low as possible while capturing the pattern

### Interaction Terms
Polynomial features also create **interaction terms** between features:

```
Features: [x₁, x₂]

degree=2 creates: [1, x₁, x₂, x₁², x₁x₂, x₂²]
                                       ↑
                              interaction term
                        (effect of x₁ depends on x₂)
```

### Feature Explosion Warning

```
Original features (p) | Degree | New feature count
──────────────────────|────────|──────────────────
2                     | 2      | 6
2                     | 3      | 10
10                    | 2      | 66
10                    | 3      | 286
100                   | 2      | 5,151  ← computational cost!
```

Always combine with **Lasso or Ridge** to handle the expanded feature set.

### Polynomial + Regularization (Best Practice)

```
Plain Polynomial     →  overfits at high degree
Polynomial + Ridge   →  smooth curve, all terms kept
Polynomial + Lasso   →  sparse curve, irrelevant terms eliminated
```

### Key Points
- The model is still **linear regression** under the hood — just on transformed features
- Feature scaling is **critical** (x¹⁰ vs x creates massive scale differences)
- Use `sklearn.preprocessing.PolynomialFeatures` to generate features
- Always pair with regularization for degree ≥ 3

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Captures non-linear relationships | Feature count explodes with degree |
| Still uses linear regression (simple) | High degree → severe overfitting |
| Flexible curve fitting | Sensitive to outliers |
| Works well for smooth curves | Extrapolates poorly outside training range |

---

## Regression Family — Quick Comparison

| | Linear | Ridge | Lasso | Polynomial |
|--|--------|-------|-------|------------|
| **Penalty** | None | L2 (w²) | L1 (\|w\|) | None (but adds features) |
| **Feature Selection** | No | No | **Yes** | No |
| **Handles Multicollinearity** | No | **Yes** | Partially | No |
| **Handles Non-linearity** | No | No | No | **Yes** |
| **Overfitting Risk** | Medium | Low | Low | High (high degree) |
| **Interpretability** | High | Medium | High (sparse) | Low (many terms) |
| **Feature Scaling** | Recommended | **Required** | **Required** | **Required** |
| **Closed-form Solution** | Yes | Yes | No | Yes (after transform) |

---

## 10. Master Comparison Table

| Property | Linear Reg. | Ridge | Lasso | Polynomial | Logistic Reg. | KNN | Decision Tree | Random Forest | SVM |
|----------|------------|-------|-------|------------|--------------|-----|---------------|---------------|-----|
| **Task** | Regression | Regression | Regression | Regression | Classification | Both | Both | Both | Both |
| **Non-linearity** | No | No | No | Yes | No | Yes | Yes | Yes | Yes (kernel) |
| **Feature Scaling** | Recommended | Required | Required | Required | Recommended | Critical | Not needed | Not needed | Critical |
| **Feature Selection** | No | No | Yes | No | No | No | Built-in | Built-in | No |
| **Overfitting Risk** | Medium | Low | Low | High | Low | Medium | High | Low | Low |
| **Interpretability** | High | Medium | High | Low | High | Low | High | Low | Low |
| **Training Speed** | Fast | Fast | Medium | Fast | Medium | None | Fast | Slow | Very Slow |
| **Large Datasets** | Yes | Yes | Yes | Careful | Yes | No | Yes | Medium | No |

---

## 11. When to Use What

### For Regression Problems
```
Predicting a number?
        ↓
Is the relationship linear?
    ↓           ↓
   Yes           No
    ↓             ↓
Too many     Polynomial Regression
features?    (+ Ridge or Lasso)
  ↓     ↓
 Yes    No
  ↓     ↓
Relevant  All features    → Plain Linear Regression
features  matter?
only?       ↓       ↓
  ↓        Yes      No
Lasso     Ridge    Ridge
```

### For Classification Problems
```
Start here → Is your data linearly separable?
                    ↓
              Yes              No
               ↓                ↓
     Logistic Regression    How many samples?
     (interpretable,             ↓
      fast, simple)       Small (<10K)    Large (>10K)
                               ↓               ↓
                        High dimensions?   Random Forest
                          ↓         ↓      or XGBoost
                         Yes        No
                          ↓         ↓
                         SVM    Decision Tree / KNN
```

### Quick Reference

| Use Case | Best Choice |
|----------|-------------|
| Predict a number, linear data | Linear Regression |
| Correlated features, all relevant | Ridge Regression |
| Many features, few relevant | Lasso Regression |
| Curved/non-linear numeric target | Polynomial + Ridge/Lasso |
| Binary yes/no classification | Logistic Regression |
| Need to explain to stakeholders | Linear / Logistic / Decision Tree |
| Small dataset, no training time | KNN |
| General purpose, tabular data | Random Forest |
| Text classification | SVM (linear kernel) |
| Competitions / best accuracy | XGBoost / LightGBM |
| Need probabilities | Logistic Regression or Random Forest |

---

## Quick Formula Reference

| Algorithm | Core Formula |
|-----------|-------------|
| Linear Regression | `ŷ = w₀ + w₁x₁ + ... + wₙxₙ` |
| Ridge | `Loss = MSE + λ·Σwᵢ²` |
| Lasso | `Loss = MSE + λ·Σ|wᵢ|` |
| Polynomial | `ŷ = w₀ + w₁x + w₂x² + ... + wdxᵈ` |
| Logistic Regression | `ŷ = 1 / (1 + e^(-(w·x + b)))` |
| KNN | `ŷ = majority(k nearest neighbors)` |
| Decision Tree | `Split = argmax Information Gain` |
| Random Forest | `ŷ = majority vote / average of N trees` |
| SVM | `decision = sign(w·x + b)` ; maximize `2/‖w‖` |

---

## Common Preprocessing Checklist

| Step | Linear Reg. | Ridge | Lasso | Polynomial | Logistic Reg. | KNN | Decision Tree | Random Forest | SVM |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Handle missing values | Yes | Yes | Yes | Yes | Yes | Yes | Optional | Optional | Yes |
| Encode categoricals | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Feature scaling | Recommended | **Required** | **Required** | **Required** | Recommended | **Required** | No | No | **Required** |
| Remove outliers | Yes | Recommended | Recommended | Yes | Recommended | Recommended | No | No | Recommended |
| Feature selection | Optional | No | Built-in | Careful | Optional | Recommended | Built-in | Built-in | Optional |

---

## 12. Bagging

### What It Does
Trains **N independent copies** of a base learner on different bootstrap samples of data, then **averages** their predictions to reduce variance.

> Core idea: **"A crowd of independent models is more stable than any single model."**

### How It Works — Steps

| Step | Action |
|------|--------|
| 1 | Draw N bootstrap samples (with replacement) from training data |
| 2 | Train one base model on each bootstrap sample independently |
| 3 | Each model sees ~63% unique rows; the rest are Out-of-Bag (OOB) |
| 4 | For new data: get prediction from every model |
| 5 | Regression → average; Classification → majority vote |

### Data Flow
```
Original Dataset (n samples)
        ↓  bootstrap sampling × N
  [sample₁]  [sample₂]  ...  [sampleₙ]
      ↓           ↓               ↓
  Model₁       Model₂   ...   Modelₙ     ← trained in PARALLEL
      ↓           ↓               ↓
         Average / Majority Vote
                ↓
          Final Prediction
```

### Why It Works — The Math
```
Single model error  = Bias² + Variance + Irreducible
Ensemble error      = Bias² + Variance/N + Irreducible
                                   ↑
                        shrinks as N increases
                        (only if models are uncorrelated)
```

### OOB (Out-of-Bag) Score
- Each bootstrap sample uses ~63% of data → remaining ~37% = OOB samples
- Predict each training sample using only models that **did NOT train on it**
- OOB score ≈ cross-validation accuracy — free validation, no extra data needed

### Key Hyperparameters
| Parameter | Controls |
|-----------|----------|
| `n_estimators` | Number of base models |
| `max_samples` | Fraction of rows per model (default 1.0 = full bootstrap) |
| `max_features` | Fraction of features per model |
| `bootstrap` | True = with replacement (bagging), False = pasting |
| `oob_score` | Enable OOB evaluation |

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Dramatically reduces variance | Does not reduce bias |
| Training is fully parallelisable | More memory (stores N models) |
| Works with any base learner | Less interpretable than single model |
| OOB gives free validation | Slower prediction than single model |

---

## 13. AdaBoost

### What It Does
Trains weak learners **sequentially**, each one focusing more on the samples that previous learners got **wrong** by increasing their sample weights.

> Core idea: **"Learn from your mistakes — pay more attention to hard examples each round."**

### How It Works — Steps

| Step | Action |
|------|--------|
| 1 | Start: assign equal weight `wᵢ = 1/n` to every training sample |
| 2 | Train weak learner h₁ on weighted data |
| 3 | Compute weighted error `εₜ = Σ wᵢ · 𝟙[yᵢ ≠ hₜ(xᵢ)]` |
| 4 | Compute model weight `αₜ = ½ · ln((1-εₜ)/εₜ)` |
| 5 | Update sample weights: increase for wrong, decrease for correct |
| 6 | Repeat steps 2–5 for T rounds |
| 7 | Final prediction: `ŷ = sign(Σ αₜ · hₜ(x))` |

### Data Flow
```
Round 1: Equal weights  →  train h₁  →  errors get higher weight
Round 2: New weights    →  train h₂  →  focuses on round 1 errors
Round 3: New weights    →  train h₃  →  focuses on round 1+2 errors
  ...
Final: ŷ = α₁·h₁(x) + α₂·h₂(x) + ... + αT·hT(x)
           ↑ better models have higher αₜ vote weight
```

### Sample Weight Update Rule
```
Correct prediction   → wᵢ × e^(-αₜ)   ← weight decreases
Wrong prediction     → wᵢ × e^(+αₜ)   ← weight increases
```

### Key Hyperparameters
| Parameter | Controls | Typical Values |
|-----------|----------|----------------|
| `n_estimators` | Number of boosting rounds | 50–500 |
| `learning_rate` | Shrinks each αₜ contribution | 0.01–1.0 |
| `estimator` | Base weak learner | `DecisionTreeClassifier(max_depth=1)` |
| `loss` (regression) | Weight update function | `linear`, `square`, `exponential` |

### AdaBoost vs Bagging
| | Bagging | AdaBoost |
|--|---------|----------|
| Tree training | Parallel | Sequential |
| What it reduces | Variance | Bias |
| Sample weighting | Equal (random sampling) | Adaptive (error-driven) |
| Sensitive to outliers | No | **Yes** |

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Reduces bias (corrects errors) | Sequential — cannot parallelise |
| Works well with weak learners | Very sensitive to noisy data/outliers |
| Few hyperparameters | Can overfit with too many rounds |
| Competitive accuracy | Slower than bagging methods |

---

## 14. Gradient Boosting

### What It Does
Builds trees **sequentially**, where each new tree fits the **residuals (errors)** of the current ensemble — moving predictions in the direction of steepest loss descent.

> Core idea: **"Each new tree corrects what all previous trees got wrong."**

### How It Works — Steps

| Step | Action |
|------|--------|
| 1 | Start with a constant prediction: `F₀(x) = mean(y)` |
| 2 | Compute residuals: `rᵢ = yᵢ - F₀(xᵢ)` |
| 3 | Fit a tree `h₁` to the residuals |
| 4 | Update: `F₁(x) = F₀(x) + η·h₁(x)` |
| 5 | Compute new residuals: `rᵢ = yᵢ - F₁(xᵢ)` |
| 6 | Repeat until T trees built |
| 7 | Final: `F(x) = F₀(x) + η·Σ hₜ(x)` |

### Data Flow
```
ŷ₀ = mean(y)
r₁ = y - ŷ₀         → fit tree₁ to r₁
ŷ₁ = ŷ₀ + η·tree₁

r₂ = y - ŷ₁         → fit tree₂ to r₂
ŷ₂ = ŷ₁ + η·tree₂

...repeat T times...

ŷ_final = ŷ₀ + η·(tree₁ + tree₂ + ... + treeₜ)
```

### Learning Rate vs N Estimators Trade-off
```
Small η (e.g. 0.01)          Large η (e.g. 0.3)
─────────────────────        ─────────────────────
Needs more trees (slow)      Fewer trees needed
Better generalisation        Risk of overfitting
More robust                  Faster training
```
**Rule of thumb:** Use small η (0.01–0.1) with early stopping.

### Stochastic Gradient Boosting
Adding `subsample < 1.0` makes each tree see a random subset of rows:
- Acts as regularisation (reduces overfitting)
- Adds randomness → more diverse trees → lower variance
- Makes training faster

### Key Hyperparameters
| Parameter | Controls | Typical Values |
|-----------|----------|----------------|
| `n_estimators` | Number of trees | 100–1000 |
| `learning_rate` | Step size (η) | 0.01–0.1 |
| `max_depth` | Depth per tree | 3–6 |
| `subsample` | Row fraction per tree | 0.6–0.9 |
| `min_samples_leaf` | Min samples in leaf | 1–20 |
| `loss` | Loss function to minimise | `squared_error`, `huber` |

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Very high accuracy | Sequential — cannot parallelise tree building |
| Flexible loss functions | Slow to train on large data |
| Handles mixed data types | Many hyperparameters to tune |
| Robust to outliers (Huber loss) | Risk of overfitting without careful tuning |

---

## 15. XGBoost

### What It Does
An **optimised, regularised** implementation of Gradient Boosting that adds L1/L2 penalties on leaf weights, uses second-order gradients, and parallelises within-level tree construction.

> Core idea: **"Gradient Boosting + regularisation + engineering optimisations = competition winner."**

### How It Improves on Gradient Boosting

| Feature | Gradient Boosting | XGBoost |
|---------|------------------|---------|
| Loss approximation | 1st-order gradient | **1st + 2nd order (Newton method)** |
| Regularisation | None | **L1 (α) + L2 (λ) on leaf weights** |
| Feature subsampling | No | **Yes (like Random Forest)** |
| Missing values | Requires imputation | **Handled natively** |
| Parallelisation | Sequential | **Parallel within each level** |
| Tree pruning | Pre-pruning only | **Post-pruning (max_delta_step)** |
| Speed | Slow | **Much faster** |

### XGBoost Objective Function
```
Objective = Σ L(yᵢ, ŷᵢ)  +  Σ Ω(fₜ)
            ↑ loss              ↑ regularisation
            (e.g. MSE)

where Ω(f) = γ·T + ½λ·Σwⱼ²  +  α·Σ|wⱼ|
              ↑ min leaves   ↑ L2    ↑ L1
```

### Key Hyperparameters
| Parameter | Controls | Typical Values |
|-----------|----------|----------------|
| `n_estimators` | Number of trees | 100–1000 |
| `learning_rate` | Step size | 0.01–0.3 |
| `max_depth` | Max tree depth | 3–8 |
| `subsample` | Row fraction per tree | 0.6–1.0 |
| `colsample_bytree` | Feature fraction per tree | 0.6–1.0 |
| `colsample_bylevel` | Feature fraction per level | 0.6–1.0 |
| `reg_alpha` | L1 penalty (leaf weights) | 0–1 |
| `reg_lambda` | L2 penalty (leaf weights) | 0–10 |
| `gamma` | Min loss reduction to split | 0–5 |
| `min_child_weight` | Min sample weight in leaf | 1–10 |
| `tree_method` | Tree building algorithm | `hist` (fast), `exact` |

### Tuning Strategy (Recommended Order)
```
1. Fix learning_rate=0.1, tune n_estimators with early stopping
2. Tune max_depth and min_child_weight
3. Tune subsample and colsample_bytree
4. Tune reg_alpha and reg_lambda
5. Lower learning_rate (0.01–0.05), increase n_estimators
```

### Strengths & Weaknesses
| Strengths | Weaknesses |
|-----------|------------|
| Best accuracy on tabular data | Many hyperparameters |
| Built-in L1/L2 regularisation | Harder to interpret than single tree |
| Handles missing values natively | Memory intensive for large trees |
| Parallel within-level building | Still sequential across levels |
| Feature importance built-in | Sensitive to learning rate choice |
| Early stopping prevents overfit | Slower than Random Forest to tune |

---

## 16. Ensemble Family — Full Comparison

### Bagging vs Boosting — Core Difference
```
BAGGING                          BOOSTING
────────────────────             ────────────────────
Trees built in PARALLEL          Trees built SEQUENTIALLY
Each tree: independent           Each tree: corrects previous
Reduces VARIANCE                 Reduces BIAS
Bootstrap samples                Weighted/residual samples
Average predictions              Weighted sum of predictions
Less prone to overfit            Can overfit (early stopping helps)
```

### The Full Ensemble Family Tree
```
Ensemble Methods
│
├── BAGGING (reduce variance, parallel)
│     ├── Bagging Regressor / Classifier  ← any base learner
│     └── Random Forest                   ← trees + feature randomness
│
└── BOOSTING (reduce bias, sequential)
      ├── AdaBoost      ← re-weights samples, weighted vote
      ├── Gradient Boost ← fits residuals, additive model
      └── XGBoost        ← GBM + regularisation + speed optimisations
            (also: LightGBM, CatBoost — same family)
```

### Full Performance Comparison (typical tabular data)

| | Bagging | Random Forest | AdaBoost | Gradient Boost | XGBoost |
|--|---------|---------------|----------|----------------|---------|
| **What it reduces** | Variance | Variance | Bias | Bias | Bias + Variance |
| **Training** | Parallel | Parallel | Sequential | Sequential | Parallel (within level) |
| **Accuracy** | Medium | High | Medium-High | High | **Very High** |
| **Speed (train)** | Fast | Fast | Medium | Slow | Medium-Fast |
| **Overfitting risk** | Low | Low | Medium | Medium | Low (with tuning) |
| **Feature scaling** | No | No | No | No | No |
| **Missing values** | No | No | No | No | **Yes (native)** |
| **Interpretability** | Low | Low (importances) | Low | Low | Low (importances) |
| **Hyperparameters** | Few | Medium | Few | Many | **Many** |
| **Best for** | Quick baseline | General purpose | Weak learners | High accuracy | **Competitions, production** |

### When to Use Each

| Scenario | Best Choice |
|----------|-------------|
| Quick, reliable baseline | Random Forest |
| Maximum accuracy on tabular data | XGBoost / LightGBM |
| Simple weak learners (stumps) | AdaBoost |
| Custom loss function | Gradient Boosting |
| Data has missing values | XGBoost |
| Need feature importance | Random Forest or XGBoost |
| Very large dataset | LightGBM (faster than XGBoost) |
| Noisy / outlier-heavy data | Random Forest or Gradient Boost (Huber loss) |

### XGBoost vs LightGBM vs CatBoost (Quick Reference)

| | XGBoost | LightGBM | CatBoost |
|--|---------|----------|----------|
| Tree growth | Level-wise | **Leaf-wise** (faster) | Symmetric |
| Speed | Medium | **Fastest** | Medium |
| Categorical features | Manual encoding | Manual encoding | **Native** |
| Memory | High | Low | Medium |
| Accuracy | Very High | Very High | Very High |

---

## Common Preprocessing Checklist (Full)

| Step | Linear | Ridge | Lasso | Poly | Logistic | KNN | Dec. Tree | Rand. Forest | SVM | Bagging | AdaBoost | Grad. Boost | XGBoost |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Handle missing | Yes | Yes | Yes | Yes | Yes | Yes | Opt | Opt | Yes | Opt | Opt | Opt | **Native** |
| Encode cats | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Feature scaling | Rec | **Req** | **Req** | **Req** | Rec | **Req** | No | No | **Req** | No | No | No | No |
| Remove outliers | Yes | Rec | Rec | Yes | Rec | Rec | No | No | Rec | No | **Yes** | Rec | No |
| Feature selection | Opt | No | Built-in | Care | Opt | Rec | Built-in | Built-in | Opt | No | No | No | Built-in |

---

*Notes compiled from classroom sessions — covers all algorithms for the T361 course.*
