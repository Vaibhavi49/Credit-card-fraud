# 💳 Credit Card Fraud Detection

A machine learning project to detect fraudulent credit card transactions using real-world data.

## 📊 Dataset
- 284,807 transactions with only 0.17% fraud cases
- Source: [Kaggle Credit Card Fraud Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

## 🔍 Problem
Highly imbalanced binary classification — detecting fraud without 
flagging too many legitimate transactions.

## ⚙️ Approach
- Exploratory Data Analysis (EDA)
- Feature scaling and preprocessing
- SMOTE to handle class imbalance
- Compared Logistic Regression vs XGBoost

## 📈 Results
| Model | Fraud Caught | False Alarms | PR-AUC |
|---|---|---|---|
| Logistic Regression | 90/98 | 1,509 | 0.77 |
| XGBoost ✅ | 89/98 | 468 | 0.81 |

## 🏆 Key Findings
- XGBoost outperformed Logistic Regression significantly
- V14 was the most important feature (48% importance)
- Model catches 91% of fraud while keeping false alarms low

## 🛠️ Libraries Used
- pandas, numpy, matplotlib, seaborn
- scikit-learn
- imbalanced-learn (SMOTE)
- XGBoost
