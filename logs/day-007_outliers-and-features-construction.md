# Day 007: Outliers and Features construction

| 📅 Date | 🏷️ Category | ⏱️ Time Spent | ⭐ Rating |
|:---|:---|:---|:---|
| `2026-08-25` | **📊 Data Preprocessing & EDA** | `4 hours` | ⭐⭐⭐⭐⭐ (Crystal Clear) |

---

## 💡 Key Learnings & Concepts
TODAY'S MACHINE LEARNING LEARNING

1. Detect Outliers
   - Learned how to detect unusual or extreme values in a dataset.
   - Outliers can affect ML model performance.

2. Z-Score Method
   - Used Z-score to detect outliers.
   - Based on mean and standard deviation.
   - Generally, Z-score > 3 or < -3 is considered an outlier.

3. IQR Method
   - Learned Interquartile Range (IQR) method.
   - IQR = Q3 - Q1
   - Lower Bound = Q1 - 1.5 × IQR
   - Upper Bound = Q3 + 1.5 × IQR
   - Values outside these limits can be treated as outliers.

4. Percentile Method
   - Learned how percentiles can be used to detect extreme values.
   - Example: 1st and 99th percentile can be used as boundaries.

5. Feature Construction
   - Learned how to create new features from existing features.
   - Helps in extracting useful information from data.
   - Can improve ML model performance.

6. Curse of Dimensionality
   - Learned the problems caused by having too many features.
   - High-dimensional data increases computational complexity.
   - Can lead to overfitting and reduced model performance.

7. PCA (Principal Component Analysis)
   - Learned PCA for dimensionality reduction.
   - Converts many features into fewer principal components.
   - Tries to retain maximum important information/variance.
   - Helps reduce the number of features and computational complexity.

TODAY'S MAIN FOCUS:

Outlier Detection → Feature Construction → Dimensionality → PCA

## 💻 Code / Implementation
```python

```

---
*Logged automatically via [Daily ML Learning Tracker](https://github.com/kunalBainsla007/daily-ml-learning) on 2026-08-25 14:46 UTC*
