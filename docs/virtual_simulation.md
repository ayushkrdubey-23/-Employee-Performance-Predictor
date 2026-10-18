# Step 8 - Virtual Simulation

## Overview

Since you don't have access to real company HR data, this project uses **virtual simulation** to create a realistic company environment. The simulation mimics how employee data is generated, how performance scores are calculated, how the AI predicts performance, and how HR would use the system.

---

## Simulation Concept

You are playing the role of an HR Analyst at a mid-sized company ("TechCorp Solutions") with 1,000 employees. The company wants to predict upcoming performance ratings to plan promotions, training, and retention actions.

---

## Step-by-Step Simulation

### Step 1: Employee Data Generation (HR Records)

**What happens:** The HR department maintains employee records. Each record contains:
- Demographics: age, gender, education_level
- Job info: department, job_level, experience_years, salary
- Work metrics: training_hours, attendance_rate, projects_completed
- Feedback: manager_feedback_rating (1-5), workload_score (1-10)

**How it's simulated:** `src/generate_data.py` creates 1,000 synthetic employee records using NumPy random distributions with realistic correlations (e.g., higher experience → higher salary).

**Command:**
```powershell
python -c "from src.generate_data import generate_dataset; generate_dataset()"
```

**Output:** `data/employee_data.csv` (1,000 rows × 14 columns)

**Screenshot to take:** Preview of the first 10 rows of employee_data.csv

---

### Step 2: Data Cleaning (HR Data Quality)

**What happens:** HR discovers some records have missing values or duplicates. They clean the data before analysis.

**How it's simulated:** `src/preprocess.py` loads the raw CSV, handles missing values (median/mode imputation), removes duplicates, encodes categorical variables, scales numerical features, and encodes the target.

**Command:**
```powershell
python -c "from src.preprocess import preprocess_data; preprocess_data()"
```

**Output:** `data/employee_data_cleaned.csv`, `models/label_encoders.pkl`, `models/scaler.pkl`

**Screenshot to take:** Missing values report and cleaned dataset shape

---

### Step 3: Performance Score Calculation (The "Truth")

**What happens:** In the simulation, each employee's true performance rating is determined by a weighted formula that reflects real-world drivers:

```
Performance Score =
  20% experience + 15% training + 15% attendance +
  15% projects + 20% manager feedback + 10% workload +
  5% education + noise
```

Employees scoring ≥ 0.65 → **High**, ≥ 0.40 → **Medium**, else → **Low**

**How it's simulated:** This happens inside `generate_dataset.py` — the `performance_rating` column is the ground truth the AI will try to predict.

**Screenshot to take:** Performance rating distribution chart (count plot)

---

### Step 4: EDA — HR Analyst Explores the Data

**What happens:** The HR analyst explores patterns:
- Which departments have the most high performers?
- Does training hours correlate with performance?
- Is attendance a strong predictor?

**How it's simulated:** `notebooks/eda.ipynb` generates univariate distributions, correlation heatmaps, and box plots.

**Command:**
```powershell
jupyter notebook notebooks/eda.ipynb
```

**Output:** Charts in `outputs/eda/`

**Screenshot to take:** Correlation heatmap, performance distribution, box plots by department

---

### Step 5: Feature Engineering (Preparing Data for AI)

**What happens:** The analyst creates derived features:
- salary_per_experience
- training_per_year
- projects_per_year
- engagement_score (combined attendance + training + projects)

Then splits data 80/20 into train/test sets.

**How it's simulated:** `src/feature_engineering.py`

**Command:**
```powershell
python -c "from src.feature_engineering import feature_engineering; feature_engineering()"
```

**Output:** `outputs/X_train.csv`, `outputs/X_test.csv`, `outputs/y_train.csv`, `outputs/y_test.csv`, `outputs/feature_names.json`

**Screenshot to take:** Feature list and train/test split sizes

---

### Step 6: AI Model Training (Building the Predictor)

**What happens:** The data science team trains a Random Forest Classifier to learn the patterns that lead to High/Medium/Low performance. They also train a Logistic Regression baseline for comparison.

**How it's simulated:** `src/train_model.py`

**Command:**
```powershell
python -c "from src.train_model import train_models; train_models()"
```

**Output:** `models/employee_performance_model.pkl`, `models/baseline_model.pkl`, `models/feature_importance.csv`

**Screenshot to take:** Feature importance chart, training accuracy

---

### Step 7: Model Evaluation (Checking AI Accuracy)

**What happens:** HR tests the AI on unseen employee data (the 20% test set) to measure:
- Overall accuracy
- Per-class precision, recall, F1-score
- Confusion matrix (which ratings get confused)

**How it's simulated:** `src/evaluate.py`

**Command:**
```powershell
python -c "from src.evaluate import evaluate_model; evaluate_model()"
```

**Output:** `outputs/evaluation/confusion_matrix.png`, `outputs/evaluation/classification_metrics.png`, `outputs/evaluation/metrics.txt`

**Result:** ~72.5% accuracy

**Screenshot to take:** Confusion matrix, accuracy score, classification report

---

### Step 8: Performance Prediction (AI Makes Predictions)

**What happens:** HR runs the trained model on employee data to predict each employee's upcoming performance rating (High / Medium / Low).

**How it's simulated:** `src/predict.py` loads the saved model, preprocesses input data using the same encoders/scalers, and outputs predictions.

**Command:**
```powershell
python -c "from src.predict import predict_performance; predict_performance()"
```

**Output:** `outputs/predictions/predictions.csv`

**Screenshot to take:** First 10 predictions with employee IDs

---

### Step 9: HR Insights & Action Planning

**What happens:** HR analyzes the predictions:
- Which features drive performance most? (feature importance)
- Which employees are at risk of Low performance? (at-risk list)
- What actions should HR take for each group?

**How it's simulated:** `src/insights.py`

**Command:**
```powershell
python -c "from src.insights import generate_insights; generate_insights()"
```

**Output:** `outputs/insights.txt`

**Screenshot to take:** Top performance drivers, HR recommendations

---

### Step 10: HR Decisions (Final Output)

**What happens:** HR managers use the insights to make decisions:

| Performance Group | HR Action |
|-------------------|-----------|
| High (predicted) | Promotion consideration, retention bonuses, mentorship roles |
| Medium (predicted) | Targeted training, goal-setting, quarterly check-ins |
| Low (predicted) | Coaching, performance improvement plan, root-cause investigation |

**Example decision:** "Employee E1042 is predicted Low performance with low attendance_rate and low manager_feedback_rating. HR schedules a coaching session and investigates workload issues."

---

## Complete Simulation Flow (One-Command Run)

Run the entire simulation end-to-end:

```powershell
python main.py
```

**What you'll see in console:**
1. Dataset generation (1,000 employees)
2. Data cleaning and encoding
3. Feature engineering and train-test split
4. Model training (Random Forest + Logistic Regression)
5. Evaluation (accuracy, confusion matrix)
6. Predictions for all employees
7. HR insights report

**Total time:** ~30 seconds

---

## What Screenshots to Take (Proof for GitHub)

| # | What to capture | File location |
|---|----------------|---------------|
| 1 | Dataset preview (first 10 rows) | `data/employee_data.csv` |
| 2 | Performance rating distribution | `outputs/eda/` |
| 3 | Correlation heatmap | `outputs/eda/` |
| 4 | Train-test split summary | Console output |
| 5 | Feature importance chart | `models/feature_importance.csv` |
| 6 | Model accuracy score | Console output (~72.5%) |
| 7 | Confusion matrix | `outputs/evaluation/confusion_matrix.png` |
| 8 | Sample predictions | `outputs/predictions/predictions.csv` |
| 9 | Top performance drivers | `outputs/insights.txt` |
| 10 | Full pipeline run | Console output of `python main.py` |

---

## What Graphs to Generate

All graphs are generated automatically by the code:

1. **`outputs/eda/`** — distribution plots, correlation heatmap, box plots
2. **`outputs/evaluation/`** — confusion matrix heatmap, classification metrics bar chart
3. **`outputs/visualizations/`** — final presentation charts (create these manually from the data for your README)

---

## What Proof to Save

Save these in your GitHub repo under `images/`:
- Dataset preview screenshot
- EDA charts (correlation heatmap, performance distribution)
- Model accuracy screenshot
- Confusion matrix screenshot
- Feature importance screenshot
- Prediction output screenshot
- Full pipeline console output

---

## How HR Would Use This System (Real-World Scenario)

1. **Quarterly review:** HR runs the predictor before appraisal cycles
2. **Identify high performers:** Top 20% predicted High → promotion candidates
3. **Identify at-risk:** Predicted Low → schedule coaching meetings
4. **Training budget:** Focus training on features with low importance that can be improved
5. **Retention:** High performers with declining engagement scores get retention offers

---

## Simulation Summary

| Step | Action | Script | Output |
|------|--------|--------|--------|
| 1 | Generate employee data | `src/generate_data.py` | `data/employee_data.csv` |
| 2 | Clean and preprocess | `src/preprocess.py` | `data/employee_data_cleaned.csv` |
| 3 | Explore data (EDA) | `notebooks/eda.ipynb` | `outputs/eda/*.png` |
| 4 | Feature engineering | `src/feature_engineering.py` | `outputs/X_train.csv`, etc. |
| 5 | Train AI model | `src/train_model.py` | `models/*.pkl` |
| 6 | Evaluate model | `src/evaluate.py` | `outputs/evaluation/*.png` |
| 7 | Predict performance | `src/predict.py` | `outputs/predictions/predictions.csv` |
| 8 | HR insights & actions | `src/insights.py` | `outputs/insights.txt` |
