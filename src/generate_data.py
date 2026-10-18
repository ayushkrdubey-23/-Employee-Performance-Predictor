"""
src/generate_data.py
Synthetic HR dataset generator for the Employee Performance Predictor project.

Generates a realistic synthetic employee dataset with features:
- employee_id, age, gender, department, education_level, job_level
- experience_years, salary, training_hours, attendance_rate
- projects_completed, manager_feedback_rating, workload_score
- performance_rating (target: High / Medium / Low)

The target (performance_rating) is computed using a rule-based virtual simulation
so that the dataset has realistic correlations between features and performance.
"""

import pandas as pd
import numpy as np
import os


def generate_dataset(n_samples=1000, random_seed=42, output_path="data/employee_data.csv"):
    """
    Generate a synthetic HR dataset and save it to CSV.

    Parameters
    ----------
    n_samples : int
        Number of employee records to generate.
    random_seed : int
        Seed for reproducibility.
    output_path : str
        Path to save the generated CSV file.

    Returns
    -------
    pd.DataFrame
        The generated dataset.
    """
    np.random.seed(random_seed)

    # ---------------------------------------------------------
    # 1. Generate categorical and numerical features
    # ---------------------------------------------------------
    employee_ids = [f"E{1000 + i}" for i in range(n_samples)]

    age = np.random.randint(22, 60, size=n_samples)

    gender = np.random.choice(["Male", "Female", "Other"], size=n_samples, p=[0.48, 0.48, 0.04])

    departments = ["Sales", "Engineering", "HR", "Marketing", "Finance", "Operations", "IT"]
    department = np.random.choice(departments, size=n_samples)

    education_levels = ["High School", "Bachelor's", "Master's", "PhD"]
    education_level = np.random.choice(
        education_levels, size=n_samples, p=[0.1, 0.5, 0.35, 0.05]
    )

    job_levels = ["Junior", "Mid", "Senior", "Lead", "Manager"]
    job_level = np.random.choice(
        job_levels, size=n_samples, p=[0.2, 0.35, 0.25, 0.1, 0.1]
    )

    # Experience correlated with age and job level
    experience_years = np.clip(
        age - np.random.randint(20, 24, size=n_samples) + np.random.randint(-2, 3, size=n_samples),
        0, 40
    ).astype(int)

    # Salary correlated with experience, job level, education
    base_salary = 30000
    salary = (
        base_salary
        + experience_years * 2500
        + np.where(job_level == "Junior", 0,
                   np.where(job_level == "Mid", 15000,
                            np.where(job_level == "Senior", 35000,
                                     np.where(job_level == "Lead", 55000, 80000))))
        + np.where(education_level == "Bachelor's", 5000,
                   np.where(education_level == "Master's", 12000,
                            np.where(education_level == "PhD", 20000, 0)))
        + np.random.randint(-5000, 5000, size=n_samples)
    )

    # Training hours (0 to 120)
    training_hours = np.random.randint(0, 121, size=n_samples)

    # Attendance rate (70 to 100 percent)
    attendance_rate = np.round(np.random.uniform(70, 100, size=n_samples), 2)

    # Projects completed (0 to 20)
    projects_completed = np.random.randint(0, 21, size=n_samples)

    # Manager feedback rating (1 to 5)
    manager_feedback_rating = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.05, 0.15, 0.4, 0.3, 0.1])

    # Workload score (1 to 10)
    workload_score = np.random.randint(1, 11, size=n_samples)

    # ---------------------------------------------------------
    # 2. Compute performance_rating using a rule-based simulation
    #    Higher scores in positive drivers -> High performance
    # ---------------------------------------------------------
    performance_score = (
        0.20 * (experience_years / 40)                     # experience factor
        + 0.15 * (training_hours / 120)                    # training factor
        + 0.15 * (attendance_rate / 100)                   # attendance factor
        + 0.15 * (projects_completed / 20)                 # projects factor
        + 0.20 * (manager_feedback_rating / 5)             # manager feedback factor
        + 0.10 * ((11 - workload_score) / 10)              # lower workload is better
        + 0.05 * (np.where(education_level == "Master's", 1,
                           np.where(education_level == "PhD", 1.2,
                                    np.where(education_level == "Bachelor's", 0.7, 0.4))) / 1.2)
        + np.random.normal(0, 0.08, size=n_samples)        # small noise
    )

    # Clip score to [0, 1]
    performance_score = np.clip(performance_score, 0, 1)

    # Map score to performance categories
    def score_to_rating(score):
        if score >= 0.65:
            return "High"
        elif score >= 0.40:
            return "Medium"
        else:
            return "Low"

    performance_rating = np.array([score_to_rating(s) for s in performance_score])

    # ---------------------------------------------------------
    # 3. Assemble DataFrame
    # ---------------------------------------------------------
    df = pd.DataFrame({
        "employee_id": employee_ids,
        "age": age,
        "gender": gender,
        "department": department,
        "education_level": education_level,
        "job_level": job_level,
        "experience_years": experience_years,
        "salary": salary,
        "training_hours": training_hours,
        "attendance_rate": attendance_rate,
        "projects_completed": projects_completed,
        "manager_feedback_rating": manager_feedback_rating,
        "workload_score": workload_score,
        "performance_rating": performance_rating
    })

    # ---------------------------------------------------------
    # 4. Save to CSV
    # ---------------------------------------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Dataset generated: {output_path}")
    print(f"Shape: {df.shape}")
    print(f"\nPerformance rating distribution:")
    print(df["performance_rating"].value_counts())

    return df


if __name__ == "__main__":
    generate_dataset()
