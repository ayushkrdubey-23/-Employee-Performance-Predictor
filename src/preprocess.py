"""
src/preprocess.py
Data cleaning and preprocessing for the Employee Performance Predictor.

Handles:
- Loading raw dataset
- Missing value handling
- Duplicate removal
- Categorical encoding
- Numerical scaling
- Saving cleaned dataset and preprocessors
"""

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler


def preprocess_data(
    input_path="data/employee_data.csv",
    output_path="data/employee_data_cleaned.csv",
    encoders_path="models/label_encoders.pkl",
    scaler_path="models/scaler.pkl"
):
    """
    Load, clean, encode, scale, and save the dataset.

    Parameters
    ----------
    input_path : str
        Path to the raw CSV dataset.
    output_path : str
        Path to save the cleaned dataset.
    encoders_path : str
        Path to save fitted label encoders.
    scaler_path : str
        Path to save the fitted scaler.

    Returns
    -------
    pd.DataFrame
        Cleaned and preprocessed dataset.
    """
    # ---------------------------------------------------------
    # 1. Load raw dataset
    # ---------------------------------------------------------
    print(f"Loading dataset from {input_path}...")
    df = pd.read_csv(input_path)
    print(f"Raw dataset shape: {df.shape}")

    # ---------------------------------------------------------
    # 2. Handle missing values
    # ---------------------------------------------------------
    missing_before = df.isnull().sum().sum()
    print(f"Missing values before cleaning: {missing_before}")

    # For numerical columns: fill with median
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].median())

    # For categorical columns: fill with mode
    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        if col == "employee_id":
            continue
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].mode()[0])

    missing_after = df.isnull().sum().sum()
    print(f"Missing values after cleaning: {missing_after}")

    # ---------------------------------------------------------
    # 3. Remove duplicates
    # ---------------------------------------------------------
    duplicates_before = df.duplicated().sum()
    df = df.drop_duplicates()
    duplicates_after = df.duplicated().sum()
    print(f"Duplicates removed: {duplicates_before - duplicates_after}")

    # ---------------------------------------------------------
    # 4. Drop employee_id (not a feature for modeling)
    # ---------------------------------------------------------
    df_model = df.drop(columns=["employee_id"])

    # ---------------------------------------------------------
    # 5. Encode categorical variables
    # ---------------------------------------------------------
    cat_columns = ["gender", "department", "education_level", "job_level", "manager_feedback_rating"]
    encoders = {}

    for col in cat_columns:
        le = LabelEncoder()
        df_model[col] = le.fit_transform(df_model[col].astype(str))
        encoders[col] = le
        print(f"Encoded column: {col} -> classes: {list(le.classes_)}")

    # ---------------------------------------------------------
    # 6. Scale numerical features
    # ---------------------------------------------------------
    num_columns = ["age", "experience_years", "salary", "training_hours",
                   "attendance_rate", "projects_completed", "workload_score"]

    scaler = StandardScaler()
    df_model[num_columns] = scaler.fit_transform(df_model[num_columns])
    print(f"Scaled numerical columns: {num_columns}")

    # ---------------------------------------------------------
    # 7. Encode target variable
    # ---------------------------------------------------------
    target_le = LabelEncoder()
    df_model["performance_rating"] = target_le.fit_transform(df_model["performance_rating"])
    encoders["performance_rating"] = target_le
    print(f"Encoded target: performance_rating -> classes: {list(target_le.classes_)}")

    # ---------------------------------------------------------
    # 8. Save cleaned dataset
    # ---------------------------------------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_model.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to {output_path}")
    print(f"Cleaned dataset shape: {df_model.shape}")

    # ---------------------------------------------------------
    # 9. Save encoders and scaler for consistent prediction later
    # ---------------------------------------------------------
    os.makedirs(os.path.dirname(encoders_path), exist_ok=True)
    joblib.dump(encoders, encoders_path)
    joblib.dump(scaler, scaler_path)
    print(f"Encoders saved to {encoders_path}")
    print(f"Scaler saved to {scaler_path}")

    return df_model


if __name__ == "__main__":
    preprocess_data()
