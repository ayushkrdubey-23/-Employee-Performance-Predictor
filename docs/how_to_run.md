## Overview

This guide explains how to run the Employee Performance Predictor project end-to-end, what commands to use, what output to expect, and the expected results.

---

## Prerequisites

Before running, complete the installation (Step 6):
- Python 3.10+ installed
- Virtual environment activated
- Dependencies installed (`pip install -r requirements.txt`)

---

## Method 1: Run the Full Pipeline (Recommended)

Run the entire project with a single command:

### Windows (PowerShell)
```powershell
# Activate virtual environment first
venv\Scripts\Activate.ps1

# Run the pipeline
python main.py
```

### Mac/Linux (Terminal)
```bash
# Activate virtual environment first
source venv/bin/activate

# Run the pipeline
python main.py
```

### What Happens (Phase by Phase)

| Phase | What Runs | Output |
|-------|-----------|--------|
| Phase 2 | `src/generate_data.py` | `data/employee_data.csv` |
| Phase 3 | `src/preprocess.py` | `data/employee_data_cleaned.csv`, `models/*.pkl` |
| Phase 5 | `src/feature_engineering.py` | `outputs/X_train.csv`, `X_test.csv`, etc. |
| Phase 6 | `src/train_model.py` | `models/employee_performance_model.pkl` |
| Phase 7 | `src/evaluate.py` | `outputs/evaluation/confusion_matrix.png`, metrics |
| Phase 7 | `src/predict.py` | `outputs/predictions/predictions.csv` |
| Phase 8 | `src/insights.py` | `outputs/insights.txt` |

---

## Method 2: Run Individual Modules

You can run each phase separately for testing or debugging:

### Generate Data Only
```powershell
python -c "from src.generate_data import generate_dataset; generate_dataset()"
```

### Preprocess Data Only
```powershell
python -c "from src.preprocess import preprocess_data; preprocess_data()"
```

### Feature Engineering Only
```powershell
python -c "from src.feature_engineering import feature_engineering; feature_engineering()"
```

### Train Model Only
```powershell
python -c "from src.train_model import train_models; train_models()"
```

### Evaluate Model Only
```powershell
python -c "from src.evaluate import evaluate_model; evaluate_model()"
```

### Predict Only
```powershell
python -c "from src.predict import predict_performance; predict_performance()"
```

### Generate Insights Only
```powershell
python -c "from src.insights import generate_insights; generate_insights()"
```

---

## Expected Output (Console)

When you run `python main.py`, you should see output similar to:

```
============================================================
Employee Performance Predictor - Pipeline
============================================================

[Phase 2] Generating synthetic HR dataset...
Dataset generated: data/employee_data.csv
Shape: (1000, 14)

Performance rating distribution:
Medium    584
High      340
Low        76

[Phase 3] Preprocessing and cleaning data...
...
Cleaned dataset saved to data/employee_data_cleaned.csv
Cleaned dataset shape: (1000, 13)
Encoders saved to models/label_encoders.pkl
Scaler saved to models/scaler.pkl

[Phase 5] Feature engineering and train-test split...
...
Train-test split (test_size=0.2):
  X_train: (800, 16), y_train: (800,)
  X_test:  (200, 200), y_test:  (200,)

[Phase 6] Model training...
...
Random Forest training accuracy: 0.9325
Logistic Regression training accuracy: 0.7675
Best model selected: Random Forest
Random Forest model saved to models/employee_performance_model.pkl

[Phase 7] Evaluating model...
...
Model Accuracy: 0.7250 (72.50%)

Classification Report:
              precision    recall  f1-score   support
        High       0.73      0.65      0.69        68
         Low       0.50      0.13      0.21        15
      Medium       0.73      0.85      0.78       117

[Phase 7] Making predictions on employee data...
...
Prediction distribution:
Medium    640
High      317
Low        43

[Phase 8] Generating HR insights...
...
Insights report saved to outputs/insights.txt

============================================================
Pipeline completed successfully!
============================================================
```

---

## Expected Results

| Metric | Expected Value |
|--------|---------------|
| Dataset size | 1,000 employees × 14 columns |
| Train-test split | 800 train / 200 test |
| Model accuracy | ~72.5% |
| Top feature | engagement_score |
| Prediction distribution | High ~30%, Medium ~65%, Low ~5% |

---

## Files Generated After Running

```
data/
├── employee_data.csv              # Raw synthetic dataset
└── employee_data_cleaned.csv      # Cleaned dataset

models/
├── employee_performance_model.pkl # Trained Random Forest model
├── baseline_model.pkl             # Logistic Regression baseline
├── label_encoders.pkl             # Fitted encoders
├── scaler.pkl                     # Fitted scaler
└── feature_importance.csv         # Feature importance ranking

outputs/
├── X_train.csv                    # Training features
├── X_test.csv                     # Test features
├── y_train.csv                    # Training target
├── y_test.csv                     # Test target
├── feature_names.json             # Feature names
├── evaluation/
│   ├── confusion_matrix.png       # Confusion matrix chart
│   ├── classification_metrics.png # Metrics bar chart
│   └── metrics.txt                # Text metrics report
├── predictions/
│   └── predictions.csv            # Predicted ratings per employee
└── insights.txt                   # HR insights report
```

---

## How to Verify It Worked

1. **Check `data/employee_data.csv` exists** — 1,000 rows, 14 columns
2. **Check `models/employee_performance_model.pkl` exists** — model is saved
3. **Check console shows "Model Accuracy: 0.7250"** — model trained and evaluated
4. **Check `outputs/predictions/predictions.csv` exists** — predictions generated
5. **Check `outputs/insights.txt` exists** — HR insights generated

---

## Quick Reference Commands

### Windows (PowerShell)
```powershell
venv\Scripts\Activate.ps1
python main.py
deactivate
```

### Mac/Linux (Terminal)
```bash
source venv/bin/activate
python main.py
deactivate
```

---

## Common Issues When Running

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'src'` | Run from the project root directory, not inside `src/` |
| `FileNotFoundError: outputs/X_train.csv` | Run phases in order: generate → preprocess → feature_engineering → train |
| `Execution policy error` (Windows) | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Accuracy much lower than 72% | Delete `data/`, `models/`, `outputs/` folders and re-run `python main.py` |
| Predictions all same class | Ensure you're predicting on raw data (`data/employee_data.csv`), not cleaned data |
