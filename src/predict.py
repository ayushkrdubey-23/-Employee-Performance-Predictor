"""
src/predict.py
Prediction module for the Employee Performance Predictor.

Loads the trained model and preprocessors, then predicts performance
rating (High / Medium / Low) for new employee data.

Can be used for:
- Single employee prediction
- Batch prediction from a CSV file
"""

import pandas as pd
import numpy as np
import os
import joblib
import json


def load_artifacts(
    model_path="models/employee_performance_model.pkl",
    encoders_path="models/label_encoders.pkl",
    scaler_path="models/scaler.pkl",
    feature_names_path="outputs/feature_names.json"
):
    """
    Load the trained model, encoders, scaler, and feature names.

    Returns
    -------
    dict
        Dictionary with model, encoders, scaler, feature_names.
    """
    model = joblib.load(model_path)
    encoders = joblib.load(encoders_path)
    scaler = joblib.load(scaler_path)

    with open(feature_names_path, "r") as f:
        feature_names = json.load(f)

    return {
        "model": model,
        "encoders": encoders,
        "scaler": scaler,
        "feature_names": feature_names
    }


def preprocess_input(df, encoders, scaler, feature_names):
    """
    Preprocess new employee data using the same encoders and scaler
    that were used during training.

    Parameters
    ----------
    df : pd.DataFrame
        Raw input data (new employee(s)).
    encoders : dict
        Fitted label encoders.
    scaler : StandardScaler
        Fitted scaler.
    feature_names : list
        List of feature names used during training.

    Returns
    -------
    pd.DataFrame
        Preprocessed feature matrix ready for prediction.
    """
    df = df.copy()

    # Drop employee_id if present (not a feature)
    if "employee_id" in df.columns:
        df = df.drop(columns=["employee_id"])

    # Encode categorical columns using the same encoders from training
    cat_columns = ["gender", "department", "education_level", "job_level", "manager_feedback_rating"]
    for col in cat_columns:
        if col in df.columns:
            le = encoders[col]
            # Handle unseen categories by mapping to the most frequent class
            df[col] = df[col].astype(str)
            known_classes = set(le.classes_)
            df[col] = df[col].apply(lambda x: x if x in known_classes else le.classes_[0])
            df[col] = le.transform(df[col])

    # Scale numerical columns
    num_columns = ["age", "experience_years", "salary", "training_hours",
                   "attendance_rate", "projects_completed", "workload_score"]
    df[num_columns] = scaler.transform(df[num_columns])

    # Add derived features (same as feature_engineering.py)
    df["salary_per_experience"] = df["salary"] / (df["experience_years"] + 1)
    df["training_per_year"] = df["training_hours"] / (df["experience_years"] + 1)
    df["projects_per_year"] = df["projects_completed"] / (df["experience_years"] + 1)
    df["engagement_score"] = (
        df["attendance_rate"] + df["training_hours"] + df["projects_completed"]
    ) / 3

    # Ensure columns are in the same order as training
    df = df[feature_names]

    return df


def predict_single(employee_data, artifacts):
    """
    Predict performance rating for a single employee.

    Parameters
    ----------
    employee_data : dict
        Dictionary with employee features.
    artifacts : dict
        Output of load_artifacts().

    Returns
    -------
    str
        Predicted performance rating (High / Medium / Low).
    """
    df = pd.DataFrame([employee_data])
    df_processed = preprocess_input(df, artifacts["encoders"], artifacts["scaler"], artifacts["feature_names"])
    prediction = artifacts["model"].predict(df_processed)[0]

    # Decode prediction back to label
    target_le = artifacts["encoders"]["performance_rating"]
    predicted_label = target_le.inverse_transform([prediction])[0]

    return predicted_label


def predict_batch(input_path, output_path="outputs/predictions/predictions.csv", artifacts=None):
    """
    Predict performance ratings for a batch of employees from a CSV file.

    Parameters
    ----------
    input_path : str
        Path to input CSV with employee data.
    output_path : str
        Path to save predictions CSV.
    artifacts : dict
        Output of load_artifacts(). If None, loads artifacts internally.

    Returns
    -------
    pd.DataFrame
        DataFrame with employee_id and predicted performance rating.
    """
    if artifacts is None:
        artifacts = load_artifacts()

    df = pd.read_csv(input_path)

    # Save employee_ids for reference
    employee_ids = df["employee_id"] if "employee_id" in df.columns else None

    df_processed = preprocess_input(df, artifacts["encoders"], artifacts["scaler"], artifacts["feature_names"])
    predictions = artifacts["model"].predict(df_processed)

    # Decode predictions
    target_le = artifacts["encoders"]["performance_rating"]
    predicted_labels = target_le.inverse_transform(predictions)

    results = pd.DataFrame({
        "employee_id": employee_ids if employee_ids is not None else range(len(predicted_labels)),
        "predicted_performance_rating": predicted_labels
    })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    results.to_csv(output_path, index=False)

    print(f"Batch predictions saved to {output_path}")
    print(f"Prediction distribution:\n{results['predicted_performance_rating'].value_counts()}")

    return results


def predict_performance(
    input_path="data/employee_data_cleaned.csv",
    output_path="outputs/predictions/predictions.csv"
):
    """
    Main entry point for prediction phase.
    Loads artifacts and runs batch prediction.

    Parameters
    ----------
    input_path : str
        Path to input CSV with employee data.
    output_path : str
        Path to save predictions.
    """
    print("Loading model artifacts...")
    artifacts = load_artifacts()

    print(f"Running batch prediction on {input_path}...")
    results = predict_batch(input_path, output_path, artifacts)

    print(f"\nSample predictions:")
    print(results.head(10))

    return results


if __name__ == "__main__":
    predict_performance()
