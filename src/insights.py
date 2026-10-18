"""
src/insights.py
Insights module for the Employee Performance Predictor.

Generates:
- Top performance drivers from feature importance
- At-risk employee list (predicted Low performance)
- HR action recommendations per performance category
- Saves insights report to outputs/insights.txt
"""

import pandas as pd
import numpy as np
import os
import joblib
import json


def generate_insights(
    model_path="models/employee_performance_model.pkl",
    feature_names_path="outputs/feature_names.json",
    predictions_path="outputs/predictions/predictions.csv",
    cleaned_data_path="data/employee_data_cleaned.csv",
    encoders_path="models/label_encoders.pkl",
    output_path="outputs/insights.txt"
):
    """
    Generate HR insights from the trained model and predictions.

    Parameters
    ----------
    model_path : str
        Path to trained model (.pkl).
    feature_names_path : str
        Path to feature names JSON.
    predictions_path : str
        Path to predictions CSV.
    cleaned_data_path : str
        Path to cleaned dataset CSV.
    encoders_path : str
        Path to label encoders (.pkl).
    output_path : str
        Path to save insights report.

    Returns
    -------
    dict
        Dictionary containing insights.
    """
    # ---------------------------------------------------------
    # 1. Load model and feature importance
    # ---------------------------------------------------------
    model = joblib.load(model_path)

    with open(feature_names_path, "r") as f:
        feature_names = json.load(f)

    encoders = joblib.load(encoders_path)
    target_le = encoders["performance_rating"]
    target_classes = list(target_le.classes_)

    # Feature importance
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    # ---------------------------------------------------------
    # 2. Load predictions and merge with employee data
    # ---------------------------------------------------------
    predictions = pd.read_csv(predictions_path)
    df = pd.read_csv(cleaned_data_path)

    # Decode cleaned data back to readable labels for reporting
    for col, le in encoders.items():
        if col in df.columns and col != "performance_rating":
            try:
                df[col] = le.inverse_transform(df[col])
            except Exception:
                pass

    # Merge predictions with employee data (by index alignment)
    df["predicted_performance"] = predictions["predicted_performance_rating"].values

    # ---------------------------------------------------------
    # 3. Top performance drivers
    # ---------------------------------------------------------
    top_drivers = importance_df.head(8)

    # ---------------------------------------------------------
    # 4. At-risk employees (predicted Low performance)
    # ---------------------------------------------------------
    at_risk = df[df["predicted_performance"] == "Low"]

    # ---------------------------------------------------------
    # 5. HR action recommendations
    # ---------------------------------------------------------
    high_performers = df[df["predicted_performance"] == "High"]
    medium_performers = df[df["predicted_performance"] == "Medium"]
    low_performers = df[df["predicted_performance"] == "Low"]

    recommendations = {
        "High": [
            "Consider for promotion or leadership roles.",
            "Include in retention and recognition programs.",
            "Assign as mentors to medium/low performers.",
            "Offer stretch assignments to maintain engagement."
        ],
        "Medium": [
            "Provide targeted training to close skill gaps.",
            "Set clear performance goals with manager check-ins.",
            "Offer upskilling opportunities in weak areas.",
            "Monitor progress quarterly."
        ],
        "Low": [
            "Immediate coaching and performance improvement plan.",
            "Investigate root causes (workload, skills, attendance).",
            "Provide additional training and support.",
            "Re-evaluate role fit or consider reassignment."
        ]
    }

    # ---------------------------------------------------------
    # 6. Build insights report
    # ---------------------------------------------------------
    lines = []
    lines.append("=" * 60)
    lines.append("EMPLOYEE PERFORMANCE PREDICTOR - HR INSIGHTS REPORT")
    lines.append("=" * 60)
    lines.append("")

    lines.append("1. TOP PERFORMANCE DRIVERS (Feature Importance)")
    lines.append("-" * 60)
    for _, row in top_drivers.iterrows():
        lines.append(f"   {row['feature']}: {row['importance']:.4f}")
    lines.append("")

    lines.append("2. PREDICTION DISTRIBUTION")
    lines.append("-" * 60)
    dist = df["predicted_performance"].value_counts()
    for cls in target_classes:
        count = dist.get(cls, 0)
        pct = (count / len(df)) * 100
        lines.append(f"   {cls}: {count} employees ({pct:.1f}%)")
    lines.append("")

    lines.append("3. AT-RISK EMPLOYEES (Predicted Low Performance)")
    lines.append("-" * 60)
    lines.append(f"   Total at-risk employees: {len(low_performers)}")
    if len(at_risk) > 0:
        # Show a few sample at-risk employees (anonymized)
        sample = at_risk.head(5)
        for _, emp in sample.iterrows():
            lines.append(f"   Employee {emp.get('employee_id', 'N/A')}: "
                         f"predicted={emp['predicted_performance']}")
    lines.append("")

    lines.append("4. HR ACTION RECOMMENDATIONS")
    lines.append("-" * 60)
    for cls in target_classes:
        lines.append(f"   {cls} Performers ({len(df[df['predicted_performance'] == cls])} employees):")
        for rec in recommendations[cls]:
            lines.append(f"      - {rec}")
        lines.append("")

    lines.append("=" * 60)
    lines.append("END OF INSIGHTS REPORT")
    lines.append("=" * 60)

    report = "\n".join(lines)

    # ---------------------------------------------------------
    # 7. Save insights report
    # ---------------------------------------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(report)

    print(report)
    print(f"\nInsights report saved to {output_path}")

    return {
        "top_drivers": top_drivers,
        "at_risk_count": len(low_performers),
        "prediction_distribution": dist.to_dict(),
        "report": report
    }


if __name__ == "__main__":
    generate_insights()
