# Step 16 - Troubleshooting

## Overview

This guide covers common errors you may encounter while building and running the Employee Performance Predictor project, along with solutions. It's divided into installation, coding, and runtime issues.

---

## Section 1: Installation & Environment Issues

### Problem 1: `python` is not recognized

**Error:**
```
'python' is not recognized as an internal or external command
```

**Cause:** Python is not installed or not added to PATH during installation.

**Solution:**
1. Re-install Python from https://www.python.org/downloads/
2. During installation, **check "Add Python to PATH"**
3. Restart your terminal/PowerShell
4. Verify: `python --version`

**Alternative on Windows:** Use `py` instead of `python`:
```powershell
py --version
py -m venv venv
```

---

### Problem 2: Virtual environment activation blocked (Windows)

**Error:**
```
venv\Scripts\Activate.ps1 : Cannot be loaded because running scripts is disabled on this system.
```

**Cause:** PowerShell execution policy prevents running scripts.

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

---

### Problem 3: `pip` not recognized

**Error:**
```
'pip' is not recognized as an internal or external command
```

**Cause:** pip not installed or not in PATH.

**Solution:**
```powershell
python -m pip install --upgrade pip
```

Then install requirements:
```powershell
pip install -r requirements.txt
```

---

### Problem 4: Package installation fails

**Error:**
```
ERROR: Could not find a version that satisfies the requirement scikit-learn
```

**Cause:** Outdated pip or network issue.

**Solution:**
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If a specific package fails, install it individually:
```powershell
pip install scikit-learn
```

---

### Problem 5: Permission denied on Mac/Linux

**Error:**
```
Permission denied: '/usr/local/lib/python3.x/site-packages'
```

**Cause:** Trying to install packages globally without using venv.

**Solution:** Always use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Never use `sudo pip install` — it breaks system Python.

---

## Section 2: Code & Runtime Issues

### Problem 6: `ModuleNotFoundError: No module named 'src'`

**Error:**
```
ModuleNotFoundError: No module named 'src'
```

**Cause:** Running Python from outside the project root directory, or `src/__init__.py` missing.

**Solution:**
1. Make sure you're in the project root directory:
```powershell
cd "C:\...\Employee-Performance-Predictor"
```
2. Verify `src/__init__.py` exists
3. Run from project root:
```powershell
python main.py
```

---

### Problem 7: `FileNotFoundError: outputs/X_train.csv`

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'outputs/X_train.csv'
```

**Cause:** Running model training before feature engineering (phases out of order).

**Solution:** Run phases in order:
1. `python -c "from src.generate_data import generate_dataset; generate_dataset()"` (Phase 2)
2. `python -c "from src.preprocess import preprocess_data; preprocess_data()"` (Phase 3)
3. `python -c "from src.feature_engineering import feature_engineering; feature_engineering()"` (Phase 5)
4. `python -c "from src.train_model import train_models; train_models()"` (Phase 6)

Or just run `python main.py` which executes all phases in order.

---

### Problem 8: `FileNotFoundError: models/employee_performance_model.pkl`

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'models/employee_performance_model.pkl'
```

**Cause:** Trying to evaluate or predict before training the model.

**Solution:** Train the model first:
```powershell
python -c "from src.train_model import train_models; train_models()"
```
Or run `python main.py` which trains before evaluating/predicting.

---

### Problem 9: All predictions are the same class (e.g., all "Low")

**Error:**
```
Prediction distribution:
Low    1000
```

**Cause:** Predicting on already-processed (encoded+scaled) data, double-processing it.

**Solution:** In `src/predict.py`, `predict_performance()` should use raw data (`data/employee_data.csv`), NOT cleaned data (`data/employee_data_cleaned.csv`). The preprocess function in `predict.py` handles encoding and scaling internally.

**Check your code:**
```python
# Correct - uses raw data
def predict_performance(input_path="data/employee_data.csv", ...):
```

---

### Problem 10: Accuracy much lower than expected (~72.5%)

**Error:**
```
Model Accuracy: 0.4500 (45.00%)
```

**Cause:** Data leakage, wrong train-test split, or model not trained properly.

**Solutions:**
1. Delete `data/`, `models/`, `outputs/` folders and re-run `python main.py` from scratch
2. Ensure encoders/scaler are fit only on training data (not test data)
3. Check that `stratify=y` is used in train_test_split
4. Verify feature names match between training and prediction

---

### Problem 11: `ValueError: y contains previously unseen labels`

**Error:**
```
ValueError: y contains previously unseen labels: 'Low'
```

**Cause:** Label encoder was fit on different classes than what's in the prediction data.

**Solution:** Save and load the same label encoders used during training. In `src/predict.py`, load encoders from `models/label_encoders.pkl` and use them to transform, not re-fit.

---

### Problem 12: `KeyError` on column name

**Error:**
```
KeyError: 'employee_id'
```

**Cause:** Column name mismatch between training and prediction data.

**Solution:** Ensure column names are identical. In `predict.py`, `preprocess_input()` drops `employee_id` if present and ensures columns match `feature_names` order.

---

### Problem 13: `FutureWarning: 'n_jobs' has no effect since 1.8`

**Error:**
```
FutureWarning: 'n_jobs' has no effect since 1.8 and will be removed in 1.10.
```

**Cause:** `n_jobs` parameter deprecated in LogisticRegression in scikit-learn 1.8+.

**Solution:** This is just a warning, not an error. The code still works. To remove it, remove `n_jobs=-1` from `LogisticRegression` in `src/train_model.py`:
```python
lr_model = LogisticRegression(max_iter=1000, random_state=random_seed)
```

---

## Section 3: Data Issues

### Problem 14: Missing values in dataset

**Error:**
```
Dataset has NaN values
```

**Cause:** Raw data has empty cells.

**Solution:** `src/preprocess.py` handles this automatically:
- Numerical columns: filled with median
- Categorical columns: filled with mode
- Verified by checking `df.isnull().sum()` before and after

---

### Problem 15: Duplicate rows

**Error:**
```
Duplicates found in dataset
```

**Cause:** Same employee record appears multiple times.

**Solution:** `src/preprocess.py` removes duplicates with `df.drop_duplicates()`. Check count before/after in console output.

---

### Problem 16: Class imbalance in target

**Error:**
```
Low class only has 76 samples out of 1000
```

**Cause:** Natural imbalance — few employees are low performers.

**Solutions:**
1. Use stratified train-test split (already implemented)
2. Check per-class metrics (precision, recall, F1) not just accuracy
3. Future improvement: Use SMOTE or class_weight='balanced'

---

## Section 4: Git Issues

### Problem 17: `fatal: not a git repository`

**Error:**
```
fatal: not a git repository (or any of the parent directories): .git
```

**Cause:** Not in a Git-initialized directory.

**Solution:**
```powershell
git init
git branch -M main
```

---

### Problem 18: `error: failed to push some refs to origin`

**Error:**
```
error: failed to push some refs to 'https://github.com/...'
```

**Cause:** Remote has changes you don't have locally, or branch mismatch.

**Solution:**
```powershell
git pull origin main --allow-unrelated-histories
git push origin main
```

---

### Problem 19: Authentication failed when pushing

**Error:**
```
remote: Support for password authentication was removed on August 13, 2021.
```

**Cause:** GitHub no longer accepts password authentication for HTTPS.

**Solution:** Use a Personal Access Token (PAT):
1. Go to https://github.com/settings/tokens
2. Generate a new token with `repo` scope
3. When prompted for password, paste the token instead

---

### Problem 20: Large files rejected by GitHub

**Error:**
```
error: File data/employee_data.csv is 100.00 MB; this exceeds GitHub's file size limit of 100.00 MB
```

**Cause:** CSV or model files too large for GitHub.

**Solution:**
1. Add large files to `.gitignore`:
```
data/*.csv
models/*.pkl
```
2. Remove from cache if already tracked:
```powershell
git rm --cached data/employee_data.csv
git commit -m "Remove large data files from tracking"
git push origin main
```

---

## Section 5: Verification Checklist

Before considering your project complete, verify:

- [ ] `python --version` shows 3.10+
- [ ] Virtual environment activates successfully
- [ ] `pip install -r requirements.txt` completes without errors
- [ ] `python main.py` runs end-to-end without errors
- [ ] Console shows "Model Accuracy: 0.7250 (72.50%)" (or similar)
- [ ] `data/employee_data.csv` exists with 1000 rows
- [ ] `models/employee_performance_model.pkl` exists
- [ ] `outputs/predictions/predictions.csv` exists with predictions
- [ ] `outputs/insights.txt` exists with HR insights
- [ ] All 7 source modules in `src/` exist
- [ ] `README.md` exists with project documentation
- [ ] Git repo has multiple commits with descriptive messages
- [ ] `.gitignore` excludes `__pycache__`, `.env`, large binaries

---

## Quick Fix Commands

Save these for reference:

```powershell
# Full reset (delete generated files, re-run everything)
Remove-Item -Recurse -Force data, models, outputs -ErrorAction SilentlyContinue
python main.py

# Reinstall all packages
pip install --upgrade pip
pip install -r requirements.txt

# Fix PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Check git status
git status
git log --oneline -10
```

---

## When All Else Fails

1. Delete `data/`, `models/`, `outputs/` folders
2. Run `python main.py` from scratch
3. Read the error message carefully — it usually tells you exactly which file or line caused the problem
4. Check that you're running from the project root directory
5. Verify virtual environment is activated (`(venv)` should appear in your prompt)
