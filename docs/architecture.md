# Step 3 - Project Architecture

## Architecture Overview

The Employee Performance Predictor follows a modular, end-to-end machine learning pipeline architecture. Data flows from raw employee records through preprocessing, analysis, model training, prediction, and finally to HR insights.

## Text-Based Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT LAYER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────────────┐   │
│  │ employee_   │  │ synthetic   │  │ new_employee_     │   │
│  │ data.csv    │  │ generator   │  │ data.csv (single) │   │
│  └──────┬──────┘  └──────┬──────┘  └─────────┬────────┘   │
│         │                │                   │            │
│         └────────────────┴───────────────────┘            │
│                           │                               │
└───────────────────────────┼───────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  PREPROCESSING LAYER                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. Load CSV                                           │  │
│  │ 2. Handle missing values                              │  │
│  │ 3. Encode categorical variables                       │  │
│  │ 4. Scale numerical features                           │  │
│  │ 5. Train-test split                                   │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                               │
└───────────────────────────┼───────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  ANALYSIS LAYER (EDA)                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ • Univariate distributions                            │  │
│  │ • Bivariate correlations                              │  │
│  │ • Performance vs each feature                         │  │
│  │ • Output: charts in outputs/eda/                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                               │
└───────────────────────────┼───────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 FEATURE ENGINEERING LAYER                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ • Create derived features                             │  │
│  │ • Select relevant features                            │  │
│  │ • Prepare X (features) and y (target)                 │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                               │
└───────────────────────────┼───────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  MODEL LAYER                                │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ Random Forest    │  │ Logistic         │                │
│  │ Classifier       │  │ Regression       │                │
│  │ (primary)        │  │ (baseline)       │                │
│  └────────┬─────────┘  └────────┬─────────┘                │
│           └──────────┬──────────┘                          │
│                      ▼                                      │
│              Trained model (.pkl via Joblib)                │
│                           │                               │
└───────────────────────────┼───────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               EVALUATION LAYER                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ • Accuracy score                                      │  │
│  │ • Confusion matrix                                    │  │
│  │ • Classification report                               │  │
│  │ • Feature importance                                  │  │
│  │ • Output: charts in outputs/evaluation/               │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                               │
└───────────────────────────┼───────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               PREDICTION LAYER                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Load model → input employee features → predict        │  │
│  │ High / Medium / Low performance rating                │  │
│  │ Output: predictions.csv                               │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                               │
└───────────────────────────┼───────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 INSIGHTS & OUTPUT LAYER                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ • Performance drivers (feature importance)            │  │
│  │ • At-risk employee list                               │  │
│  │ • HR action recommendations                           │  │
│  │ • Visualizations in outputs/visualizations/           │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                               │
└───────────────────────────┼───────────────────────────────┘
                            ▼
                    HR DECISIONS / ACTIONS
```

## Data Flow Explanation

### Stage 1: Input Layer
- **employee_data.csv**: Synthetic HR dataset with columns — employee_id, age, gender, department, education_level, job_level, experience_years, salary, training_hours, attendance_rate, projects_completed, manager_feedback_rating, workload_score, performance_rating (target)
- **new_employee_data.csv**: Single employee record for real-time prediction
- Data is either loaded from CSV or generated synthetically using NumPy/Pandas

### Stage 2: Preprocessing Layer
1. **Load** the CSV into a Pandas DataFrame
2. **Clean** — handle missing values (drop or impute), remove duplicates
3. **Encode** categorical columns (department, education_level, job_level, gender, manager_feedback_rating) using One-Hot Encoding or Label Encoding
4. **Scale** numerical features (age, salary, training_hours, etc.) using StandardScaler or MinMaxScaler
5. **Split** into training (80%) and testing (20%) sets with stratification on the target

### Stage 3: Analysis Layer (EDA)
- Univariate analysis: distribution of each feature and the target (performance_rating)
- Bivariate analysis: correlation heatmap, scatter plots, box plots comparing features across performance categories
- Output charts saved to `outputs/eda/`

### Stage 4: Feature Engineering Layer
- Create derived features (e.g., salary_per_experience, training_per_year)
- Select the most relevant features using correlation and feature importance
- Separate into X (feature matrix) and y (target vector)

### Stage 5: Model Layer
- **Primary model:** Random Forest Classifier (n_estimators=100, random_state=42)
- **Baseline model:** Logistic Regression for comparison
- Train on training set, tune hyperparameters if needed
- Save trained model using Joblib to `models/employee_performance_model.pkl`

### Stage 6: Evaluation Layer
- Predict on test set
- Compute accuracy, precision, recall, F1-score
- Generate confusion matrix and classification report
- Extract feature importance from Random Forest
- Save charts to `outputs/evaluation/`

### Stage 7: Prediction Layer
- Load the saved .pkl model
- Preprocess new employee data using the same encoders/scalers
- Predict performance rating (High / Medium / Low)
- Output predictions to `outputs/predictions.csv`

### Stage 8: Insights & Output Layer
- Identify top performance drivers from feature importance
- List at-risk employees (predicted Low performance)
- Generate HR action recommendations (coaching, training, retention)
- Save visualizations to `outputs/visualizations/`

### Final Output: HR Decisions
HR and managers use the predictions and insights to:
- Identify high performers for promotion/rewards
- Plan training for medium performers
- Design retention/coaching interventions for low performers

## Folder Mapping to Architecture

| Architecture Layer | Code/File Location |
|-------------------|-------------------|
| Input Layer | `data/employee_data.csv`, `data/generate_data.py` |
| Preprocessing Layer | `src/preprocess.py` |
| Analysis Layer | `notebooks/eda.ipynb` |
| Feature Engineering | `src/feature_engineering.py` |
| Model Layer | `src/train_model.py` |
| Evaluation Layer | `src/evaluate.py` |
| Prediction Layer | `src/predict.py` |
| Insights & Output | `outputs/`, `src/insights.py` |
| Model Artifact | `models/employee_performance_model.pkl` |

## Key Design Principles

1. **Modularity** — Each stage is a separate script/function, easy to test and modify
2. **Reproducibility** — Fixed random_state, saved model artifact, requirements.txt
3. **Explainability** — Feature importance and SHAP values surface why predictions are made
4. **Beginner-friendly** — Clear variable names, comments, step-by-step execution via main.py
5. **Portfolio-ready** — Clean folder structure, documented code, visual outputs
