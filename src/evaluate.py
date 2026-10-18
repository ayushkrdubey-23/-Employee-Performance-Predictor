"""
src/evaluate.py
Model evaluation for the Employee Performance Predictor.

Computes:
- Accuracy score
- Confusion matrix
- Classification report (precision, recall, F1-score)
- Feature importance visualization

Saves charts to outputs/evaluation/ and metrics to console.
"""

import pandas as pd
import numpy as np
import os
import joblib
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report
)


def evaluate_model(
    X_test_path="outputs/X_test.csv",
    y_test_path="outputs/y_test.csv",
    feature_names_path="outputs/feature_names.json",
    model_path="models/employee_performance_model.pkl",
    encoders_path="models/label_encoders.pkl",
    output_dir="outputs/evaluation",
    random_seed=42
):
    """
    Evaluate the trained model on the test set.

    Parameters
    ----------
    X_test_path : str
        Path to test features CSV.
    y_test_path : str
        Path to test target CSV.
    feature_names_path : str
        Path to feature names JSON.
    model_path : str
        Path to the trained model (.pkl).
    encoders_path : str
        Path to label encoders (.pkl).
    output_dir : str
        Directory to save evaluation charts.
    random_seed : int
        Random seed (for consistency).

    Returns
    -------
    dict
        Dictionary containing accuracy, classification report, confusion matrix.
    """
    # ---------------------------------------------------------
    # 1. Load test data and model
    # ---------------------------------------------------------
    print(f"Loading test data from {X_test_path} and {y_test_path}...")
    X_test = pd.read_csv(X_test_path)
    y_test = pd.read_csv(y_test_path).squeeze()

    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)

    # Load label encoders to decode target back to labels
    encoders = joblib.load(encoders_path)
    target_le = encoders["performance_rating"]
    target_classes = list(target_le.classes_)

    print(f"Test samples: {X_test.shape[0]}")
    print(f"Target classes: {target_classes}")

    # ---------------------------------------------------------
    # 2. Predict on test set
    # ---------------------------------------------------------
    y_pred = model.predict(X_test)

    # ---------------------------------------------------------
    # 3. Compute accuracy
    # ---------------------------------------------------------
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")

    # ---------------------------------------------------------
    # 4. Classification report
    # ---------------------------------------------------------
    report = classification_report(y_test, y_pred, target_names=target_classes, output_dict=True)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=target_classes))

    # ---------------------------------------------------------
    # 5. Confusion matrix
    # ---------------------------------------------------------
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)

    # ---------------------------------------------------------
    # 6. Save evaluation charts
    # ---------------------------------------------------------
    os.makedirs(output_dir, exist_ok=True)

    # Confusion matrix heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=target_classes,
        yticklabels=target_classes
    )
    plt.title("Confusion Matrix - Employee Performance Predictor")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.tight_layout()
    plt.savefig(cm_path, dpi=150)
    plt.close()
    print(f"Confusion matrix saved to {cm_path}")

    # Classification report bar chart (precision, recall, f1 per class)
    metrics_df = pd.DataFrame(report).transpose()
    plot_metrics = metrics_df.loc[target_classes, ["precision", "recall", "f1-score"]]

    plt.figure(figsize=(10, 6))
    plot_metrics.plot(kind="bar", figsize=(10, 6))
    plt.title("Classification Metrics by Performance Class")
    plt.xlabel("Performance Class")
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.legend(loc="lower right")
    plt.tight_layout()
    metrics_path = os.path.join(output_dir, "classification_metrics.png")
    plt.savefig(metrics_path, dpi=150)
    plt.close()
    print(f"Classification metrics chart saved to {metrics_path}")

    # ---------------------------------------------------------
    # 7. Save metrics to a text file
    # ---------------------------------------------------------
    metrics_path_txt = os.path.join(output_dir, "metrics.txt")
    with open(metrics_path_txt, "w") as f:
        f.write(f"Model Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)\n\n")
        f.write("Classification Report:\n")
        f.write(classification_report(y_test, y_pred, target_names=target_classes))
        f.write("\n\nConfusion Matrix:\n")
        f.write(np.array2string(cm))
    print(f"Metrics saved to {metrics_path_txt}")

    return {
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix": cm,
        "y_test": y_test,
        "y_pred": y_pred,
        "target_classes": target_classes
    }


if __name__ == "__main__":
    evaluate_model()
