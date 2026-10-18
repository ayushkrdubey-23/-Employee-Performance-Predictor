# Step 4 - Implementation Plan (Phase-Wise)

## Phase 1: Setup

**What to do:**
- Install Python 3.10+
- Create project folder structure
- Set up virtual environment (venv)
- Install required libraries (pandas, numpy, scikit-learn, matplotlib, seaborn, joblib, jupyter)
- Initialize Git repository
- Create requirements.txt

**Why:** Establishes a clean, isolated development environment so dependencies don't conflict and the project is reproducible.

**Expected output:**
- Virtual environment activated
- requirements.txt with all dependencies
- Empty Git repo on main branch
- Folder structure created

**Common mistakes:**
- Forgetting to activate the virtual environment before installing packages
- Installing packages globally instead of in venv
- Not creating requirements.txt, making it hard for others to reproduce

**Commit message:** `Phase 1: Setup - project structure, venv, requirements.txt`

---

## Phase 2: Data Creation / Loading

**What to do:**
- Create synthetic HR dataset generator script (`src/generate_data.py`)
- Generate 1000+ employee records with realistic features
- Save dataset to `data/employee_data.csv`
- Load and preview the dataset

**Features to generate:**
- employee_id, age, gender, department, education_level, job_level
- experience_years, salary, training_hours, attendance_rate
- projects_completed, manager_feedback_rating, workload_score
- performance_rating (target: High / Medium / Low)

**Why:** Since real HR data is not available, synthetic data simulates a real company environment and lets the project run end-to-end.

**Expected output:**
- `data/employee_data.csv` with 1000+ rows
- First 5 rows printed to console
- Dataset info (shape, columns, dtypes)

**Common mistakes:**
- Target column not balanced across High/Medium/Low
- Unrealistic correlations (e.g., low experience but high salary)
- Not setting random_seed for reproducibility

**Commit message:** `Phase 2: Data Creation - synthetic HR dataset generator`

---

## Phase 3: Data Cleaning

**What to do:**
- Load `data/employee_data.csv`
- Check for missing values and handle them (drop or impute)
- Remove duplicate rows
- Validate data types
- Save cleaned dataset to `data/employee_data_cleaned.csv`

**Why:** Raw synthetic data may have inconsistencies; cleaning ensures the model trains on quality data.

**Expected output:**
- Missing value report (before/after)
- Duplicate count removed
- `data/employee_data_cleaned.csv`
- Data types validated

**Common mistakes:**
- Dropping too many rows with missing values, losing data
- Not saving the cleaned dataset separately
- Ignoring data type mismatches

**Commit message:** `Phase 3: Data Cleaning - handle missing values and duplicates`

---

## Phase 4: EDA (Exploratory Data Analysis)

**What to do:**
- Univariate analysis: distribution of each feature and target
- Bivariate analysis: correlation heatmap, performance vs each feature
- Visualize performance_rating distribution
- Save charts to `outputs/eda/`

**Charts to generate:**
- Count plot of performance_rating
- Histograms of numerical features
- Box plots of features by performance_rating
- Correlation heatmap
- Pairplot (selected features)

**Why:** Understand data patterns, find which features drive performance, detect outliers.

**Expected output:**
- EDA notebook (`notebooks/eda.ipynb`)
- Charts saved in `outputs/eda/`
- Key findings summary (e.g., "training_hours correlates with performance")

**Common mistakes:**
- Not saving charts, so no visual proof for GitHub
- Overlooking class imbalance in target
- Not interpreting correlations, just producing plots

**Commit message:** `Phase 4: EDA - exploratory data analysis and visualizations`

---

## Phase 5: Feature Engineering

**What to do:**
- Encode categorical variables (department, education_level, job_level, gender, manager_feedback_rating)
- Scale numerical features (StandardScaler / MinMaxScaler)
- Create derived features (e.g., salary_per_year_experience, training_per_year)
- Select relevant features
- Split into X (features) and y (target)
- Train-test split (80/20, stratified)

**Why:** Machine learning models need numerical input; encoding and scaling make categorical and numerical data model-ready.

**Expected output:**
- `src/preprocess.py` and `src/feature_engineering.py`
- X_train, X_test, y_train, y_test arrays
- Saved encoders and scalers (for consistent prediction later)
- Feature list documented

**Common mistakes:**
- Fitting scaler on entire dataset before train-test split (data leakage)
- Not saving encoders/scalers, so prediction on new data fails
- Including target column in features

**Commit message:** `Phase 5: Feature Engineering - encoding, scaling, train-test split`

---

## Phase 6: Model Building

**What to do:**
- Train Random Forest Classifier (primary model)
- Train Logistic Regression (baseline model)
- Compare both models
- Save best model to `models/employee_performance_model.pkl` using Joblib

**Why:** Random Forest handles tabular HR data well and provides feature importance; Logistic Regression gives a baseline for comparison.

**Expected output:**
- `src/train_model.py`
- Trained Random Forest model (.pkl)
- Baseline Logistic Regression results
- Model saved in `models/`

**Common mistakes:**
- Not setting random_state, so results aren't reproducible
- Using default hyperparameters without consideration
- Saving model without saving encoders/scalers

**Commit message:** `Phase 6: Model Building - Random Forest + Logistic Regression`

---

## Phase 7: Evaluation

**What to do:**
- Predict on test set
- Calculate accuracy, precision, recall, F1-score
- Generate confusion matrix
- Generate classification report
- Extract feature importance from Random Forest
- Save charts to `outputs/evaluation/`

**Why:** Quantify model performance and understand which features matter most.

**Expected output:**
- `src/evaluate.py`
- Accuracy score printed
- Confusion matrix plot saved
- Classification report printed
- Feature importance chart saved
- `outputs/evaluation/`

**Common mistakes:**
- Evaluating on training data instead of test data (overfitting illusion)
- Not checking per-class metrics (important for imbalanced classes)
- Not visualizing confusion matrix

**Commit message:** `Phase 7: Evaluation - accuracy, confusion matrix, feature importance`

---

## Phase 8: Insights

**What to do:**
- Identify top performance drivers from feature importance
- List at-risk employees (predicted Low performance)
- Generate HR action recommendations (coaching, training, retention)
- Save insights report

**Why:** Turn model predictions into actionable HR decisions.

**Expected output:**
- `src/insights.py`
- Top 5 performance drivers listed
- At-risk employee list
- HR recommendations per performance category
- Insights saved to `outputs/insights.txt`

**Common mistakes:**
- Not connecting feature importance to business actions
- Providing predictions without recommendations
- Not identifying which employees need intervention

**Commit message:** `Phase 8: Insights - performance drivers and HR recommendations`

---

## Phase 9: Visualization

**What to do:**
- Create final visualizations for presentation
- Performance distribution chart
- Feature importance bar chart
- Confusion matrix heatmap
- Prediction distribution (High/Medium/Low)
- Save all to `outputs/visualizations/`

**Why:** Visual proof for GitHub README, placement portfolio, and interviews.

**Expected output:**
- `outputs/visualizations/*.png`
- All key charts ready for screenshots
- Visual summary of project results

**Common mistakes:**
- Low-resolution images not suitable for README
- Not labeling charts clearly
- Missing charts that interviewers expect to see

**Commit message:** `Phase 9: Visualization - final charts for portfolio and README`

---

## Phase 10: GitHub Upload

**What to do:**
- Create GitHub repository
- Add all code, data, models, outputs, docs
- Create .gitignore (exclude __pycache__, .env, large .pkl if needed)
- Commit with descriptive messages
- Push to GitHub
- Upload screenshots to `images/` folder
- Update README.md with project details

**Why:** Public proof of work for placements, internships, and recruiters.

**Expected output:**
- Public GitHub repository
- All code and assets pushed
- README.md with badges, screenshots, how-to-run
- Commit history showing phase-wise progress

**Common mistakes:**
- Committing secrets or large binary files
- Poor commit messages ("update", "fix")
- Missing README, making repo hard to understand

**Commit message:** `Phase 10: GitHub Upload - push all project files to GitHub`

---

## Phase Summary Table

| Phase | Task | Key Output | Status |
|-------|------|------------|--------|
| 1 | Setup | venv, requirements.txt, folder structure | Planned |
| 2 | Data Creation | `data/employee_data.csv` | Planned |
| 3 | Data Cleaning | `data/employee_data_cleaned.csv` | Planned |
| 4 | EDA | `notebooks/eda.ipynb`, `outputs/eda/` | Planned |
| 5 | Feature Engineering | `src/preprocess.py`, train-test split | Planned |
| 6 | Model Building | `models/*.pkl` | Planned |
| 7 | Evaluation | `outputs/evaluation/`, metrics | Planned |
| 8 | Insights | `outputs/insights.txt` | Planned |
| 9 | Visualization | `outputs/visualizations/*.png` | Planned |
| 10 | GitHub Upload | Public repo, README.md | Planned |

**Progress after Phase 4 (every 5 steps checkpoint):**
- Completed: 0 of 16 steps
- Remaining: 16 of 16 steps
