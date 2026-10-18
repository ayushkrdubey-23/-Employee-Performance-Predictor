# Employee Performance Predictor using Data Analytics

> A data-driven machine learning system that predicts an employee's upcoming performance rating (High / Medium / Low) and surfaces actionable drivers to guide HR interventions and manager coaching.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-orange.svg)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Data-Pandas-yellow.svg)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Student Project](https://img.shields.io/badge/Student-Placement%20Portfolio-purple.svg)]()

---

## 📋 Project Overview

The **Employee Performance Predictor** is an end-to-end people analytics project that uses machine learning to forecast employee performance ratings. Built with Python, Pandas, Scikit-learn, and Random Forest, it processes synthetic HR data, trains a classification model, and generates actionable HR insights.

This project is designed as a **placement-ready portfolio project** for students — complete with synthetic data generation, preprocessing, EDA, model training, evaluation, prediction, and HR insights — all without needing access to real company HR data.

---

## 🎯 Problem Statement

Companies struggle to:
- Identify high performers before appraisal cycles
- Predict which employees are at risk of low performance
- Make data-driven promotion and training decisions
- Reduce bias in performance evaluations

HR decisions are often intuition-based rather than evidence-based. This project builds a predictive system that forecasts performance ratings (High / Medium / Low) and identifies the key drivers behind each prediction, enabling proactive HR interventions.

---

## 💼 Business Value

| Stakeholder | Value Delivered |
|-------------|----------------|
| **HR Teams** | Objective performance predictions, reduced appraisal bias, targeted retention planning |
| **Managers** | Early identification of at-risk employees, data-backed coaching conversations |
| **Business Leaders** | Workforce performance visibility, optimized training budgets, succession planning |
| **Employees** | Transparent, criteria-based performance feedback |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.10+ |
| **Data Handling** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Machine Learning** | Scikit-learn (Random Forest, Logistic Regression) |
| **Model Persistence** | Joblib |
| **Environment** | venv / virtualenv |
| **Notebooks** | Jupyter Notebook |
| **Version Control** | Git |

**Selected Option:** Intermediate (Option B) — Random Forest Classifier as primary model with Logistic Regression baseline.

---

## 🏗 Architecture

```
Input Layer → Preprocessing → EDA → Feature Engineering → Model → Evaluation → Prediction → Insights → HR Decisions
```

### Data Flow

1. **Input:** Synthetic HR dataset (1,000 employees, 14 features)
2. **Preprocessing:** Missing value handling, categorical encoding, numerical scaling, train-test split
3. **EDA:** Distribution analysis, correlation heatmaps, performance vs features
4. **Feature Engineering:** Derived features (engagement_score, salary_per_experience, etc.)
5. **Model:** Random Forest Classifier (primary), Logistic Regression (baseline)
6. **Evaluation:** Accuracy, confusion matrix, classification report, feature importance
7. **Prediction:** Performance rating (High/Medium/Low) for each employee
8. **Insights:** Top performance drivers, at-risk employee list, HR recommendations
9. **HR Decisions:** Promotions, training, retention, coaching actions

### Folder Structure

```
Employee-Performance-Predictor/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── data/
│   ├── employee_data.csv
│   ├── employee_data_cleaned.csv
│   └── generate_data.py
├── notebooks/
│   └── eda.ipynb
├── src/
│   ├── generate_data.py
│   ├── preprocess.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── evaluate.py
│   ├── predict.py
│   └── insights.py
├── models/
│   └── employee_performance_model.pkl
├── outputs/
│   ├── eda/
│   ├── evaluation/
│   ├── predictions/
│   ├── visualizations/
│   └── insights.txt
├── images/
└── docs/
```

---

## 🚀 How to Run

### 1. Setup

```powershell
# Clone the repository
git clone https://github.com/<your-username>/Employee-Performance-Predictor.git
cd Employee-Performance-Predictor

# Create virtual environment
python -m venv venv
venv\Scripts\Activate.ps1      # Windows
# source venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Full Pipeline

```powershell
python main.py
```

### 3. Expected Output

```
============================================================
Employee Performance Predictor - Pipeline
============================================================

[Phase 2] Generating synthetic HR dataset...
Dataset generated: data/employee_data.csv
Shape: (1000, 14)

[Phase 6] Model training...
Random Forest training accuracy: 0.9325
Best model selected: Random Forest

[Phase 7] Evaluating model...
Model Accuracy: 0.7250 (72.50%)

[Phase 8] Generating HR insights...
Insights report saved to outputs/insights.txt

============================================================
Pipeline completed successfully!
============================================================
```

---

## 📊 Results

| Metric | Value |
|--------|-------|
| Dataset Size | 1,000 employees × 14 columns |
| Train/Test Split | 800 train / 200 test |
| Model Accuracy | ~72.5% |
| Primary Model | Random Forest Classifier |
| Baseline Model | Logistic Regression |
| Top Performance Driver | engagement_score |
| Prediction Distribution | High ~32%, Medium ~64%, Low ~4% |

### Sample Classification Report

```
              precision    recall  f1-score   support
        High       0.73      0.65      0.69        68
         Low       0.50      0.13      0.21        15
      Medium       0.73      0.85      0.78       117

    accuracy                           0.72       200
   macro avg       0.65      0.54      0.56       200
weighted avg       0.71      0.72      0.71       200
```

### Top 5 Performance Drivers

1. engagement_score (0.144)
2. experience_years (0.102)
3. age (0.088)
4. projects_per_year (0.086)
5. training_per_year (0.085)

---

## 📸 Screenshots

Add the following screenshots to the `images/` folder:

| # | Screenshot | Purpose |
|---|-----------|---------|
| 1 | Dataset preview (first 10 rows) | Shows raw HR data structure |
| 2 | Performance rating distribution | Shows class balance |
| 3 | Correlation heatmap | Shows feature relationships |
| 4 | Model accuracy score | Shows model performance |
| 5 | Confusion matrix | Shows prediction errors |
| 6 | Feature importance chart | Shows key drivers |
| 7 | Sample predictions output | Shows prediction format |
| 8 | Full pipeline console output | Shows end-to-end execution |

---

## 📁 Module Reference

| Module | Purpose |
|--------|---------|
| `src/generate_data.py` | Synthetic HR dataset generation |
| `src/preprocess.py` | Data cleaning, encoding, scaling |
| `src/feature_engineering.py` | Derived features, train-test split |
| `src/train_model.py` | Random Forest + Logistic Regression training |
| `src/evaluate.py` | Accuracy, confusion matrix, metrics |
| `src/predict.py` | Performance prediction on employee data |
| `src/insights.py` | Performance drivers, HR recommendations |
| `main.py` | Full pipeline entry point |

---

## 🎓 Interview Preparation

This project is designed to answer common placement interview questions:

**For HR interviews:**
- "What does your project do?" → Predicts employee performance using ML
- "Why did you choose this topic?" → People analytics is growing, helps companies make data-driven HR decisions
- "What was your role?" → End-to-end: data generation to model to insights

**For technical interviews:**
- "Which algorithm did you use and why?" → Random Forest — handles tabular data well, provides feature importance, resists overfitting
- "How did you handle categorical variables?" → Label Encoding with scikit-learn
- "How did you evaluate the model?" → Accuracy, confusion matrix, classification report (precision, recall, F1)
- "What is feature importance?" → Measures how much each feature contributes to predictions
- "How would you handle class imbalance?" → Stratified train-test split, class weights, or resampling

---

## 🔮 Future Improvements

- Real HR dataset (with proper anonymization)
- Deep learning models (Neural Networks)
- Employee attrition prediction
- Interactive dashboard (Streamlit/Flask)
- Real-time prediction API (FastAPI)
- SHAP values for individual prediction explainability
- Model monitoring and drift detection

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` from project root |
| `Execution policy error` (Windows) | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Low accuracy | Delete `data/`, `models/`, `outputs/` and re-run `python main.py` |
| All predictions same class | Ensure predicting on raw data, not already-processed data |

---

## 📄 License

MIT License. See LICENSE file for details.

---

## 👨‍💻 Author

**Ayush Kumar Dubey** — Data Science Student

Built as a placement portfolio project demonstrating full-stack data science skills: data engineering → EDA → ML → explainability → HR insights.

---

⭐ **If this project helped you, please star the repository!**
