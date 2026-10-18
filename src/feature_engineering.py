"""
src/feature_engineering.py
Feature engineering for the Employee Performance Predictor.

Handles:
- Creating derived features
- Selecting relevant features
- Splitting into X (features) and y (target)
- Train-test split (stratified, 80/20)
- Saving processed splits
"""

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split


def add_derived_features(df):
    """
    Create derived features from existing columns.

    Parameters
    ----------
    df : pd.DataFrame
        Preprocessed dataset.

    Returns
    -------
    pd.DataFrame
        Dataset with derived features added.
    """
    df = df.copy()

    # Salary per year of experience (avoid division by zero)
    df["salary_per_experience"] = df["salary"] / (df["experience_years"] + 1)

    # Training hours per year of experience
    df["training_per_year"] = df["training_hours"] / (df["experience_years"] + 1)

    # Projects per year of experience
    df["projects_per_year"] = df["projects_completed"] / (df["experience_years"] + 1)

    # Combined engagement score (attendance + training + projects)
    df["engagement_score"] = (
        df["attendance_rate"] +
        df["training_hours"] +
        df["projects_completed"]
    ) / 3

    print(f"Added derived features: salary_per_experience, training_per_year, "
          f"projects_per_year, engagement_score")

    return df


def feature_engineering(
    input_path="data/employee_data_cleaned.csv",
    output_dir="outputs",
    test_size=0.2,
    random_seed=42
):
    """
    Perform feature engineering and train-test split.

    Parameters
    ----------
    input_path : str
        Path to cleaned dataset.
    output_dir : str
        Directory to save processed splits.
    test_size : float
        Fraction of data for testing.
    random_seed : int
        Random seed for reproducibility.

    Returns
    -------
    dict
        Dictionary containing X_train, X_test, y_train, y_test and feature names.
    """
    # ---------------------------------------------------------
    # 1. Load cleaned dataset
    # ---------------------------------------------------------
    print(f"Loading cleaned dataset from {input_path}...")
    df = pd.read_csv(input_path)
    print(f"Dataset shape: {df.shape}")

    # ---------------------------------------------------------
    # 2. Add derived features
    # ---------------------------------------------------------
    df = add_derived_features(df)

    # ---------------------------------------------------------
    # 3. Separate features (X) and target (y)
    # ---------------------------------------------------------
    target_column = "performance_rating"
    X = df.drop(columns=[target_column])
    y = df[target_column]

    feature_names = list(X.columns)
    print(f"Target column: {target_column}")
    print(f"Feature columns ({len(feature_names)}): {feature_names}")
    print(f"Target distribution:\n{y.value_counts()}")

    # ---------------------------------------------------------
    # 4. Train-test split (stratified to keep class balance)
    # ---------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_seed, stratify=y
    )

    print(f"\nTrain-test split (test_size={test_size}):")
    print(f"  X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"  X_test:  {X_test.shape},  y_test:  {y_test.shape}")

    # ---------------------------------------------------------
    # 5. Save processed splits
    # ---------------------------------------------------------
    os.makedirs(output_dir, exist_ok=True)
    X_train.to_csv(os.path.join(output_dir, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(output_dir, "X_test.csv"), index=False)
    y_train.to_csv(os.path.join(output_dir, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(output_dir, "y_test.csv"), index=False)

    # Save feature names for reference
    import json
    with open(os.path.join(output_dir, "feature_names.json"), "w") as f:
        json.dump(feature_names, f)

    print(f"\nProcessed splits saved to {output_dir}/")

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "feature_names": feature_names
    }


if __name__ == "__main__":
    feature_engineering()
