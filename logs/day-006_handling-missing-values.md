# Day 006: Handling missing values

| 📅 Date | 🏷️ Category | ⏱️ Time Spent | ⭐ Rating |
|:---|:---|:---|:---|
| `2026-08-24` | **📊 Data Preprocessing & EDA** | `5 hours` | ⭐⭐⭐⭐⭐ (Crystal Clear) |

---

## 💡 Key Learnings & Concepts
📘 Daily Machine Learning Notes — 24 Aug 2026
Topics Learned Today
Handling Mixed Variables
Numerical + categorical variables ko ek dataset me handle karna.
Different preprocessing techniques ko appropriate columns par apply karna.
Handling Date & Time Variables
Date/time columns ko useful features me convert karna.
Examples:
Year
Month
Day
Day of week
Hour
Date ko directly model me dene ke bajay meaningful features extract karna.
Handling Missing Data
Dataset me missing values (NaN) identify aur handle karna.
Missing data ko:
Drop kar sakte hain
Mean/Median/Mode se impute kar sakte hain
Advanced imputation techniques use kar sakte hain.
Numerical & Categorical Missing Data
Numerical: Mean, Median, KNN Imputer, MICE etc.
Categorical: Most Frequent/Mode ya suitable category se impute karna.
KNN Imputer
Similar observations/neighbours ke basis par missing numerical values fill karta hai.
sklearn.impute.KNNImputer ka use kiya.
Missing Indicator
Missing value thi ya nahi, iska separate indicator feature create karta hai.
Example:
Age = NaN → Age_missing = 1
Age = 22 → Age_missing = 0
MICE (Multiple Imputation by Chained Equations)
Missing values ko other available variables ke relationships ke basis par iteratively estimate karta hai.
Complex datasets me useful advanced imputation approach.
🛠️ Libraries Practiced
Pandas → data cleaning, missing values aur date-time handling
Scikit-learn → imputation aur preprocessing techniques
Important tools/classes:
SimpleImputer
KNNImputer
MissingIndicator
preprocessing pipelines

## 💻 Code / Implementation
```python

```

---
*Logged automatically via [Daily ML Learning Tracker](https://github.com/kunalBainsla007/daily-ml-learning) on 2026-08-24 15:51 UTC*
