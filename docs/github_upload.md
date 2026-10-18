# Step 10 - GitHub Upload Steps

## Overview

Uploading your project to GitHub gives you public proof of work for placements, internships, and recruiters. This guide covers repo creation, connecting your local folder, pushing code, commit messages, uploading screenshots, and repo metadata.

---

## Recommended Repo Metadata

| Field | Recommended Value |
|-------|-------------------|
| **Repo name** | `Employee-Performance-Predictor` |
| **Description** | Employee Performance Predictor using Data Analytics - Synthetic HR dataset, Random Forest classification, EDA, feature importance, and HR insights for people analytics |
| **Visibility** | Public |
| **Tags/Topics** | `employee-performance`, `people-analytics`, `hr-analytics`, `machine-learning`, `random-forest`, `data-science`, `python`, `student-project`, `placement-portfolio` |
| **License** | MIT License (optional, recommended for open projects) |

---

## Step 1: Create the GitHub Repository

1. Go to https://github.com and sign in
2. Click the **+** icon → **New repository**
3. Repository name: `Employee-Performance-Predictor`
4. Description: (copy from table above)
5. Select **Public**
6. **Do NOT** check "Add a README file" (you already have one locally)
7. **Do NOT** check "Add .gitignore" (you already have one locally)
8. **Do NOT** check "Choose a license" (you can add later)
9. Click **Create repository**

You'll see a page with commands to push an existing repository. Copy the repository URL (e.g., `https://github.com/<your-username>/Employee-Performance-Predictor.git`).

---

## Step 2: Connect Local Folder to GitHub

Open PowerShell/Terminal in your project folder:

```powershell
cd "C:\Users\kumar\OneDrive\Desktop\Ayush_Kumar_Dubey\Data Science\Project (3)\Employee-Performance-Predictor"
```

### Initialize Git (if not already done)
```powershell
git init
git branch -M main
```

### Add the remote repository
```powershell
git remote add origin https://github.com/<your-username>/Employee-Performance-Predictor.git
```

Replace `<your-username>` with your actual GitHub username.

### Verify remote
```powershell
git remote -v
```

---

## Step 3: Stage and Commit All Files

### Check current status
```powershell
git status
```

### Stage all files
```powershell
git add -A
```

### Commit with descriptive message
```powershell
git commit -m "Initial commit: Employee Performance Predictor project

- Synthetic HR dataset generator
- Data preprocessing and cleaning pipeline
- Feature engineering with derived features
- Random Forest + Logistic Regression models
- Model evaluation with confusion matrix and metrics
- Performance prediction module
- HR insights and recommendations
- Documentation: explanation, tech stack, architecture, implementation plan,
  folder structure, installation guide, how to run, virtual simulation
- requirements.txt, .gitignore, main.py entry point"
```

---

## Step 4: Push Code to GitHub

### Push to main branch
```powershell
git push -u origin main
```

### If prompted for authentication
- Use a Personal Access Token (PAT) instead of your password
- Generate PAT at: https://github.com/settings/tokens
- Copy the token and paste it when prompted

### Verify push
```powershell
git log --oneline
git status
```

Your code should now be visible at: `https://github.com/<your-username>/Employee-Performance-Predictor`

---

## Step 5: Upload Screenshots to `images/` Folder

Take screenshots of:
1. Dataset preview (first 10 rows of `data/employee_data.csv`)
2. Performance rating distribution chart
3. Correlation heatmap from EDA
4. Model accuracy score (console output)
5. Confusion matrix (`outputs/evaluation/confusion_matrix.png`)
6. Feature importance chart
7. Sample predictions (`outputs/predictions/predictions.csv`)
8. Full pipeline run output

### Add screenshots
```powershell
git add images/
git commit -m "Add screenshots for README and project proof"
git push origin main
```

---

## Step 6: Commit Message Convention

Use descriptive, phase-based commit messages throughout the project:

| Phase | Commit Message Example |
|-------|----------------------|
| Setup | `Setup: project structure, venv, requirements.txt` |
| Data | `Data: synthetic HR dataset generator (1000 employees)` |
| Cleaning | `Cleaning: handle missing values, encode and scale features` |
| EDA | `EDA: exploratory data analysis with visualizations` |
| Features | `Features: derived features and train-test split` |
| Model | `Model: Random Forest + Logistic Regression training` |
| Eval | `Evaluation: accuracy, confusion matrix, classification report` |
| Predict | `Predict: performance prediction module` |
| Insights | `Insights: performance drivers and HR recommendations` |
| Docs | `Docs: project explanation, architecture, implementation plan` |
| README | `README: professional project documentation` |
| Screenshots | `Screenshots: add proof images for GitHub` |

**Bad commit messages** (avoid):
- `update`
- `fix`
- `changes`
- `stuff`

**Good commit messages:**
- `Phase 2: Data Creation - synthetic HR dataset generator`
- `Phase 6: Model Building - Random Forest + Logistic Regression`
- `Phase 7: Evaluation - accuracy, confusion matrix, feature importance`

---

## Step 7: Update README.md with GitHub Info

Your local `README.md` should include:
- Project title and badges
- Problem statement
- Tech stack
- Architecture diagram
- How to run (commands)
- Results (accuracy ~72.5%)
- Screenshots (from `images/`)
- Folder structure
- License

Commit and push the README:
```powershell
git add README.md
git commit -m "README: professional project documentation with screenshots"
git push origin main
```

---

## Step 8: Enable GitHub Pages (Optional, for Dashboard)

If you want to host a simple dashboard:
1. Go to repo Settings → Pages
2. Source: Deploy from a branch → `main` → `/ (root)`
3. Click Save
4. Your site will be at `https://<your-username>.github.io/Employee-Performance-Predictor/`

---

## GitHub Upload Checklist

- [ ] GitHub repository created (public)
- [ ] Remote origin added
- [ ] All code committed (`src/`, `main.py`, `requirements.txt`, etc.)
- [ ] Documentation committed (`docs/`, `README.md`)
- [ ] `.gitignore` configured (excludes `__pycache__`, `.env`, large binaries)
- [ ] Code pushed to `main` branch
- [ ] Screenshots uploaded to `images/`
- [ ] Commit messages are descriptive (not "update" or "fix")
- [ ] Repo has description and topics/tags
- [ ] Repo URL works and is publicly accessible

---

## Example Git Command Sequence (Copy-Paste Ready)

```powershell
# Navigate to project
cd "C:\Users\kumar\OneDrive\Desktop\Ayush_Kumar_Dubey\Data Science\Project (3)\Employee-Performance-Predictor"

# Initialize and set branch
git init
git branch -M main

# Add remote (replace <your-username>)
git remote add origin https://github.com/<your-username>/Employee-Performance-Predictor.git

# Stage all
git add -A

# Commit
git commit -m "Initial commit: Employee Performance Predictor project"

# Push
git push -u origin main
```

---

## Your Public Repo URL

After pushing, share this link on your resume:
```
https://github.com/<your-username>/Employee-Performance-Predictor
```
