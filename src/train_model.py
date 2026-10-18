"""
src/train_model.py
Model training for the Employee Performance Predictor.

Trains:
- Random Forest Classifier (primary model)
- Logistic Regression (baseline model)

Saves the best model to models/employee_performance_model.pkl using Joblib.
"""

import pandas as pd
import numpy as np
import os
import joblib
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def train_models(
    X_train_path="outputs/X_train.csv",
    y_train_path="outputs/y_train.csv",
    feature_names_path="outputs/feature_names.json",
    model_path="models/employee_performance_model.pkl",
    baseline_path="models/baseline_model.pkl",
    random_seed=42
):
    """
    Train Random Forest and Logistic Regression models.

    Parameters
    ----------
    X_train_path : str
        Path to training features CSV.
    y_train_path : str
        Path to training target CSV.
    feature_names_path : str
        Path to feature names JSON.
    model_path : str
        Path to save the primary (Random Forest) model.
    baseline_path : str
        Path to save the baseline (Logistic Regression) model.
    random_seed : int
        Random seed for reproducibility.

    Returns
    -------
    dict
        Dictionary containing trained models and training scores.
    """
    # ---------------------------------------------------------
    # 1. Load training data
    # ---------------------------------------------------------
    print(f"Loading training data from {X_train_path} and {y_train_path}...")
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).squeeze()  # convert to Series

    # Load feature names
    with open(feature_names_path, "r") as f:
        feature_names = json.load(f)

    print(f"Training samples: {X_train.shape[0]}, Features: {X_train.shape[1]}")

    # ---------------------------------------------------------
    # 2. Train Random Forest Classifier (primary model)
    # ---------------------------------------------------------
    print("\nTraining Random Forest Classifier...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=random_seed,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    rf_train_score = rf_model.score(X_train, y_train)
    print(f"Random Forest training accuracy: {rf_train_score:.4f}")

    # ---------------------------------------------------------
    # 3. Train Logistic Regression (baseline model)
    # ---------------------------------------------------------
    print("\nTraining Logistic Regression (baseline)...")
    lr_model = LogisticRegression(
        max_iter=1000,
        random_state=random_seed,
        n_jobs=-1
    )
    lr_model.fit(X_train, y_train)
    lr_train_score = lr_model.score(X_train, y_train)
    print(f"Logistic Regression training accuracy: {lr_train_score:.4f}")

    # ---------------------------------------------------------
    # 4. Select best model (Random Forest usually performs better on tabular data)
    # ---------------------------------------------------------
    best_model = rf_model if rf_train_score >= lr_train_score else lr_model
    best_name = "Random Forest" if best_model is rf_model else "Logistic Regression"
    print(f"\nBest model selected: {best_name}")

    # ---------------------------------------------------------
    # 5. Save models
    # ---------------------------------------------------------
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(rf_model, model_path)
    joblib.dump(lr_model, baseline_path)
    print(f"Random Forest model saved to {model_path}")
    print(f"Logistic Regression model saved to {baseline_path}")

    # ---------------------------------------------------------
    # 6. Save feature importance from Random Forest
    # ---------------------------------------------------------
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": rf_model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    importance_path = os.path.join(os.path.dirname(model_path), "feature_importance.csv")
    importance_df.to_csv(importance_path, index=False)
    print(f"Feature importance saved to {importance_path}")
    print(f"\nTop 5 important features:")
    print(importance_df.head(5))

    return {
        "random_forest": rf_model,
        "logistic_regression": lr_model,
        "best_model": best_model,
        "best_name": best_name,
        "rf_train_score": rf_train_score,
        "lr_train_score": lr_train_score,
        "feature_importance": importance_df
    }


if __name__ == "__main__":
    train_models()
