# Step 12 - Proof Building Strategy

## Overview

For placements and internships, recruiters want to see **consistent, documented progress** — not just a final dump of code. This strategy shows what to upload each day over 5 days, with commit messages and proof screenshots, so your GitHub commit history tells a story of real work.

---

## 5-Day Proof Building Plan

| Day | Focus | What to Upload | Commit Message |
|-----|-------|---------------|----------------|
| **Day 1** | Setup | Folder structure, `.gitignore`, `requirements.txt`, `main.py` skeleton, `docs/` | `Day 1: Setup - project structure, venv, requirements.txt` |
| **Day 2** | Dataset | `src/generate_data.py`, `data/employee_data.csv`, dataset preview screenshot | `Day 2: Dataset - synthetic HR data generator (1000 employees)` |
| **Day 3** | EDA | `notebooks/eda.ipynb`, `src/preprocess.py`, `src/feature_engineering.py`, EDA charts | `Day 3: EDA - exploratory data analysis and feature engineering` |
| **Day 4** | Model | `src/train_model.py`, `src/evaluate.py`, `models/*.pkl`, accuracy + confusion matrix screenshots | `Day 4: Model - Random Forest training and evaluation` |
| **Day 5** | Results | `src/predict.py`, `src/insights.py`, `outputs/predictions/`, `outputs/insights.txt`, final screenshots, `README.md` | `Day 5: Results - predictions, HR insights, and project documentation` |

---

## Day 1: Setup (Project Foundation)

### What to Do
1. Create project folder structure (`data/`, `src/`, `models/`, `outputs/`, `images/`, `docs/`)
2. Create `.gitignore` (exclude `__pycache__`, `.env`, `.ipynb_checkpoints`)
3. Create `requirements.txt` (pandas, numpy, scikit-learn, matplotlib, seaborn, joblib, jupyter)
4. Create `main.py` entry point skeleton
5. Initialize Git repo, create `main` branch
6. Write `docs/project_explanation.md`

### Files to Commit
```
.gitignore
requirements.txt
main.py
src/__init__.py
docs/project_explanation.md
```

### Commit Command
```powershell
git add -A
git commit -m "Day 1: Setup - project structure, venv, requirements.txt"
```

### Proof Screenshots to Take
- Empty folder structure in VS Code / file explorer
- `requirements.txt` contents
- `git log` showing first commit
- Virtual environment activated in terminal

---

## Day 2: Dataset (Synthetic HR Data)

### What to Do
1. Write `src/generate_data.py` — generates 1,000 employee records
2. Run it to create `data/employee_data.csv`
3. Verify dataset shape and column names
4. Write `docs/tech_stack.md` (Option B selected)
5. Take dataset preview screenshot

### Files to Commit
```
src/generate_data.py
data/employee_data.csv
docs/tech_stack.md
```

### Commit Command
```powershell
git add -A
git commit -m "Day 2: Dataset - synthetic HR data generator (1000 employees)"
```

### Proof Screenshots to Take
- First 10 rows of `employee_data.csv` opened in Excel/Pandas
- Dataset shape output (1000, 14)
- Column names list
- Performance rating distribution count

---

## Day 3: EDA + Feature Engineering

### What to Do
1. Write `src/preprocess.py` — cleaning, encoding, scaling
2. Write `src/feature_engineering.py` — derived features, train-test split
3. Create `notebooks/eda.ipynb` with charts
4. Generate EDA visualizations (distribution, correlation heatmap, box plots)
5. Write `docs/architecture.md`
6. Run preprocessing and feature engineering

### Files to Commit
```
src/preprocess.py
src/feature_engineering.py
notebooks/eda.ipynb
docs/architecture.md
data/employee_data_cleaned.csv
outputs/X_train.csv, X_test.csv, y_train.csv, y_test.csv
outputs/feature_names.json
```

### Commit Command
```powershell
git add -A
git commit -m "Day 3: EDA - exploratory data analysis and feature engineering"
```

### Proof Screenshots to Take
- Correlation heatmap chart
- Performance rating distribution bar chart
- Box plot (e.g., training_hours by performance_rating)
- Train/test split sizes (800/200)
- Feature list (16 features after engineering)

---

## Day 4: Model Building + Evaluation

### What to Do
1. Write `src/train_model.py` — Random Forest + Logistic Regression
2. Write `src/evaluate.py` — accuracy, confusion matrix, classification report
3. Train models and save `.pkl` files
4. Generate evaluation charts
5. Write `docs/implementation_plan.md`
6. Record accuracy score

### Files to Commit
```
src/train_model.py
src/evaluate.py
models/employee_performance_model.pkl
models/baseline_model.pkl
models/label_encoders.pkl
models/scaler.pkl
models/feature_importance.csv
outputs/evaluation/confusion_matrix.png
outputs/evaluation/classification_metrics.png
outputs/evaluation/metrics.txt
docs/implementation_plan.md
```

### Commit Command
```powershell
git add -A
git commit -m "Day 4: Model - Random Forest training and evaluation"
```

### Proof Screenshots to Take
- Console output showing accuracy (~72.5%)
- Confusion matrix image
- Classification report (precision/recall/F1 per class)
- Feature importance ranking (top 5 features)
- Training vs baseline model comparison

---

## Day 5: Prediction + Insights + Documentation

### What to Do
1. Write `src/predict.py` — batch prediction on employee data
2. Write `src/insights.py` — performance drivers, at-risk list, HR recommendations
3. Run full pipeline (`python main.py`)
4. Generate predictions CSV and insights report
5. Write `docs/installation_guide.md`, `docs/how_to_run.md`, `docs/virtual_simulation.md`, `docs/github_upload.md`
6. Write professional `README.md`
7. Take final screenshots for `images/`
8. Push everything to GitHub

### Files to Commit
```
src/predict.py
src/insights.py
outputs/predictions/predictions.csv
outputs/insights.txt
docs/installation_guide.md
docs/how_to_run.md
docs/virtual_simulation.md
docs/github_upload.md
docs/folder_structure.md
images/*.png (screenshots)
README.md
```

### Commit Command
```powershell
git add -A
git commit -m "Day 5: Results - predictions, HR insights, and project documentation"
git push origin main
```

### Proof Screenshots to Take
- Full pipeline console output (`python main.py`)
- `outputs/predictions/predictions.csv` first 10 rows
- `outputs/insights.txt` content
- Top performance drivers list
- HR recommendations per performance group
- Completed GitHub repository page

---

## Daily Commit Message Examples

| Day | Good Commit Message |
|-----|--------------------|
| Day 1 | `Day 1: Setup - project structure, venv, requirements.txt` |
| Day 2 | `Day 2: Dataset - synthetic HR data generator (1000 employees)` |
| Day 3 | `Day 3: EDA - exploratory data analysis and feature engineering` |
| Day 4 | `Day 4: Model - Random Forest training and evaluation` |
| Day 5 | `Day 5: Results - predictions, HR insights, and project documentation` |

**Avoid:** `update`, `fix`, `changes`, `done`, `final`

---

## Proof Screenshots Checklist (for GitHub README)

| # | Screenshot | When to Take | Where to Save |
|---|-----------|-------------|---------------|
| 1 | Project folder structure | Day 1 | `images/01_folder_structure.png` |
| 2 | requirements.txt | Day 1 | `images/02_requirements.png` |
| 3 | Dataset preview (first 10 rows) | Day 2 | `images/03_dataset_preview.png` |
| 4 | Dataset shape (1000, 14) | Day 2 | `images/04_dataset_shape.png` |
| 5 | Performance rating distribution | Day 2 | `images/05_rating_distribution.png` |
| 6 | Correlation heatmap | Day 3 | `images/06_correlation_heatmap.png` |
| 7 | Box plot by performance | Day 3 | `images/07_boxplot_performance.png` |
| 8 | Train/test split | Day 3 | `images/08_train_test_split.png` |
| 9 | Model accuracy console output | Day 4 | `images/09_model_accuracy.png` |
| 10 | Confusion matrix | Day 4 | `images/10_confusion_matrix.png` |
| 11 | Feature importance chart | Day 4 | `images/11_feature_importance.png` |
| 12 | Sample predictions | Day 5 | `images/12_predictions.png` |
| 13 | HR insights report | Day 5 | `images/13_insights.png` |
| 14 | Full pipeline run | Day 5 | `images/14_pipeline_run.png` |
| 15 | GitHub repo page | Day 5 | `images/15_github_repo.png` |

---

## How to Take Screenshots (Windows)

- **Full screen:** `PrtScn` key → paste into Paint or Snipping Tool
- **Active window:** `Alt + PrtScn`
- **Snipping Tool:** `Win + Shift + S` → select area → save
- **VS Code:** Install "Screenshot" extension or use built-in preview

Save all screenshots as `.png` in the `images/` folder with clear names.

---

## GitHub Commit History Goal

Your final GitHub commit graph should show 5+ distinct commits spread across days, like:

```
* 0976f79 Day 5: Results - predictions, HR insights, documentation
* d72669f Day 5: GitHub upload steps documentation
* a7569d5 Day 5: How to run project
* 2350b25 Day 5: Installation guide
* d31caf5 Day 5: Virtual simulation
* f2affc1 Day 4: Model - training and evaluation code
* ac17afa Day 4: Implementation plan
* 9f8c519 Day 3: Folder structure
* 88d6287 Day 3: Architecture
* 143d509 Day 2: Tech stack selection
* 1723793 Day 1: Project explanation
```

This shows **consistent progress over 5 days** — exactly what placement recruiters look for.

---

## What to Show in Interviews

When interviewers ask about your project, you can say:

> "I built this over 5 days. Day 1 was setup, Day 2 was the synthetic dataset, Day 3 was EDA and feature engineering, Day 4 was model training with Random Forest, and Day 5 was predictions, HR insights, and documentation. You can see the daily progress in my GitHub commit history."

Then show them your GitHub repo with the commit graph and screenshots.
