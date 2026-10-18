# Step 6 - Installation Guide

## Overview

This guide shows how to set up the Employee Performance Predictor project on your machine. Steps are provided for both **Windows** and **Mac/Linux**.

---

## 1. Python Setup

### Check if Python is installed

**Windows (PowerShell):**
```powershell
python --version
```
or
```powershell
py --version
```

**Mac/Linux (Terminal):**
```bash
python3 --version
```

**Expected output:** `Python 3.10.x` or similar (3.10+ recommended).

### If Python is not installed

1. Go to https://www.python.org/downloads/
2. Download the latest stable Python 3.x installer
3. **Windows:** During installation, **check "Add Python to PATH"** — this is critical
4. Complete the installation
5. Restart your terminal/command prompt and verify with `python --version`

---

## 2. Clone / Download the Project

**Option A: Clone from GitHub (after Phase 10)**
```bash
git clone https://github.com/<your-username>/Employee-Performance-Predictor.git
cd Employee-Performance-Predictor
```

**Option B: Use the local folder**
```powershell
# Windows PowerShell
cd "C:\Users\kumar\OneDrive\Desktop\Ayush_Kumar_Dubey\Data Science\Project (3)\Employee-Performance-Predictor"
```

```bash
# Mac/Linux Terminal
cd ~/Desktop/Ayush_Kumar_Dubey/Data\ Science/Project\ \(3\)/Employee-Performance-Predictor
```

---

## 3. Create a Virtual Environment

A virtual environment keeps project dependencies isolated and prevents conflicts.

### Windows (PowerShell)
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### Mac/Linux (Terminal)
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verify activation:** Your terminal prompt should now show `(venv)` at the beginning.

---

## 4. Install Required Libraries

With the virtual environment activated, install dependencies from `requirements.txt`:

### Windows & Mac/Linux
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### What gets installed
| Package | Version | Purpose |
|---------|---------|---------|
| pandas | >=1.5.0 | Data manipulation and analysis |
| numpy | >=1.24.0 | Numerical computing |
| scikit-learn | >=1.2.0 | Machine learning models and preprocessing |
| matplotlib | >=3.7.0 | Basic plotting |
| seaborn | >=0.12.0 | Statistical visualization |
| joblib | >=1.2.0 | Model serialization (.pkl) |
| jupyter | >=1.0.0 | Notebooks for EDA |
| streamlit | >=1.28.0 | Interactive dashboard |
| plotly | >=5.17.0 | Interactive charts |

### Verify installation
```powershell
pip list
```

You should see all packages listed above.

---

## 5. Verify the Setup

Run a quick test to confirm everything works:

```powershell
python -c "import pandas, numpy, sklearn, matplotlib, seaborn, joblib; print('All imports successful')"
```

**Expected output:** `All imports successful`

---

## 6. Jupyter Notebook (Optional, for EDA)

To open the EDA notebook:

```powershell
jupyter notebook notebooks/eda.ipynb
```

This will open a browser window with the notebook.

---

## 7. Running the Project

After installation, run the full pipeline:

```powershell
python main.py
```

This executes all phases: data generation → preprocessing → training → evaluation → prediction.

To run the Streamlit dashboard:

```powershell
streamlit run streamlit_app.py
```

---

## 8. Deactivating the Virtual Environment

When you're done working:

### Windows
```powershell
deactivate
```

### Mac/Linux
```bash
deactivate
```

---

## Troubleshooting Installation

| Problem | Solution |
|---------|----------|
| `python` not recognized | Re-install Python and check "Add to PATH" during install |
| `venv\Scripts\Activate.ps1` blocked | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `pip` not recognized | Run `python -m pip install --upgrade pip` |
| Permission denied on Mac | Use `python3 -m venv venv` (no sudo needed with venv) |
| Package install fails | Upgrade pip first: `pip install --upgrade pip` |

---

## Quick Reference Commands

**Windows:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
streamlit run streamlit_app.py
deactivate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
streamlit run streamlit_app.py
deactivate
```
