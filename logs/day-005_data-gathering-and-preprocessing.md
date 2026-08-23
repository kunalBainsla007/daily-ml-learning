# Day 005: Data Gathering and Preprocessing

| 📅 Date | 🏷️ Category | ⏱️ Time Spent | ⭐ Rating |
|:---|:---|:---|:---|
| `2026-08-23` | **📊 Data Preprocessing & EDA** | `5 hours` | ⭐⭐⭐⭐⭐ (Crystal Clear) |

---

## 💡 Key Learnings & Concepts
Daily ML Notes — 23 August 2026
1. Data Gathering
ML project ka first step data collect karna hota hai.
Data sources:
CSV files
JSON data
APIs
Web scraping
Databases
Good quality aur relevant data model ke performance ke liye important hai.
2. CSV
CSV = Comma Separated Values
Tabular data store karne ka simple format.
Rows = records, Columns = features.
Python me mainly Pandas se handle karte hain.
Example:
import pandas as pd
df = pd.read_csv("data.csv")
3. JSON
JSON = JavaScript Object Notation
Structured data exchange ke liye commonly used format.
APIs se data mostly JSON format me milta hai.
Python me json library ya Pandas se handle kar sakte hain.
4. Web Scraping
Website se automatically data extract karna = Web Scraping.
Common Python libraries:
BeautifulSoup
Requests
Selenium
Use cases: price data, articles, reviews, public datasets etc.
5. API Fetching
API = Application Programming Interface
API ke through kisi service/server se data programmatically obtain kar sakte hain.
Usually: Request → Server → Response → JSON/Data
Python me requests library commonly use hoti hai.
6. EDA — Exploratory Data Analysis
EDA ka purpose data ko understand karna hota hai.
Important steps:
head()
tail()
shape
info()
describe()
Missing values check
Duplicate values check
Outlier detection
Distribution analysis
Correlation analysis
Visualization using Matplotlib/Seaborn
7. Data Preprocessing
Raw data ko ML model ke liye usable format me convert karna.
Main steps:
Missing values handle karna
Duplicate data remove karna
Outliers handle karna
Categorical data encode karna
Numerical data scale/normalize karna
Incorrect data types fix karna
8. Feature Engineering
Existing data se new useful features create karna ya existing features ko transform karna.
Examples:
Date → day, month, year
Height + Weight → BMI
First Name + Last Name → Full Name
Continuous values ko categories me convert karna
Log transformation / mathematical transformations
Goal: Model ko aise features dena jo patterns ko better understand karne me help karein

## 💻 Code / Implementation
```python

```

---
*Logged automatically via [Daily ML Learning Tracker](https://github.com/kunalBainsla007/daily-ml-learning) on 2026-08-23 15:18 UTC*
