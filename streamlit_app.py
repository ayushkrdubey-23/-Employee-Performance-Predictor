"""
streamlit_app.py
Employee Performance Predictor - Interactive Dashboard

Tabs:
1. Overview - Project summary and key metrics
2. Dataset Preview - Synthetic HR dataset exploration
3. EDA & Analysis - Distributions, correlations, performance drivers
4. Model Performance - Accuracy, confusion matrix, feature importance
5. Single Prediction - Predict performance for one employee
6. Batch Prediction - Upload CSV, predict for multiple employees
7. HR Insights - At-risk employees and HR action recommendations

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import json
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Employee Performance Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------
MODEL_PATH = "models/employee_performance_model.pkl"
ENCODERS_PATH = "models/label_encoders.pkl"
SCALER_PATH = "models/scaler.pkl"
FEATURE_NAMES_PATH = "outputs/feature_names.json"
DATA_PATH = "data/employee_data.csv"
CLEANED_DATA_PATH = "data/employee_data_cleaned.csv"
PREDICTIONS_PATH = "outputs/predictions/predictions.csv"
INSIGHTS_PATH = "outputs/insights.txt"
FEATURE_IMPORTANCE_PATH = "models/feature_importance.csv"
CONFUSION_MATRIX_PATH = "outputs/evaluation/confusion_matrix.png"
METRICS_PATH = "outputs/evaluation/metrics.txt"

TARGET_CLASSES = ["High", "Low", "Medium"]


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------
@st.cache_data
def load_data(path=DATA_PATH):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


@st.cache_data
def load_cleaned_data(path=CLEANED_DATA_PATH):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


@st.cache_resource
def load_artifacts():
    if not all(os.path.exists(p) for p in [MODEL_PATH, ENCODERS_PATH, SCALER_PATH, FEATURE_NAMES_PATH]):
        return None
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    scaler = joblib.load(SCALER_PATH)
    with open(FEATURE_NAMES_PATH, "r") as f:
        feature_names = json.load(f)
    return {"model": model, "encoders": encoders, "scaler": scaler, "feature_names": feature_names}


def preprocess_input(df, artifacts):
    """Preprocess input data using saved encoders and scaler."""
    df = df.copy()
    if "employee_id" in df.columns:
        df = df.drop(columns=["employee_id"])

    encoders = artifacts["encoders"]
    scaler = artifacts["scaler"]
    feature_names = artifacts["feature_names"]

    cat_columns = ["gender", "department", "education_level", "job_level", "manager_feedback_rating"]
    for col in cat_columns:
        if col in df.columns:
            le = encoders[col]
            df[col] = df[col].astype(str)
            known_classes = set(le.classes_)
            df[col] = df[col].apply(lambda x: x if x in known_classes else le.classes_[0])
            df[col] = le.transform(df[col])

    num_columns = ["age", "experience_years", "salary", "training_hours",
                   "attendance_rate", "projects_completed", "workload_score"]
    df[num_columns] = scaler.transform(df[num_columns])

    df["salary_per_experience"] = df["salary"] / (df["experience_years"] + 1)
    df["training_per_year"] = df["training_hours"] / (df["experience_years"] + 1)
    df["projects_per_year"] = df["projects_completed"] / (df["experience_years"] + 1)
    df["engagement_score"] = (df["attendance_rate"] + df["training_hours"] + df["projects_completed"]) / 3

    df = df[feature_names]
    return df


def predict_single(employee_dict, artifacts):
    df = pd.DataFrame([employee_dict])
    df_processed = preprocess_input(df, artifacts)
    prediction = artifacts["model"].predict(df_processed)[0]
    target_le = artifacts["encoders"]["performance_rating"]
    label = target_le.inverse_transform([prediction])[0]
    probs = artifacts["model"].predict_proba(df_processed)[0]
    prob_dict = {cls: float(p) for cls, p in zip(target_le.classes_, probs)}
    return label, prob_dict


def predict_batch(df, artifacts):
    employee_ids = df["employee_id"] if "employee_id" in df.columns else None
    df_processed = preprocess_input(df, artifacts)
    predictions = artifacts["model"].predict(df_processed)
    target_le = artifacts["encoders"]["performance_rating"]
    labels = target_le.inverse_transform(predictions)
    results = pd.DataFrame({
        "employee_id": employee_ids if employee_ids is not None else range(len(labels)),
        "predicted_performance_rating": labels
    })
    return results


# ---------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------
st.sidebar.title("📊 Employee Performance Predictor")
st.sidebar.markdown("---")

tabs = [
    "Overview",
    "Dataset Preview",
    "EDA & Analysis",
    "Model Performance",
    "Single Prediction",
    "Batch Prediction",
    "HR Insights"
]

choice = st.sidebar.radio("Navigate", tabs)

st.sidebar.markdown("---")
st.sidebar.markdown("### Project Info")
st.sidebar.info("People Analytics • Random Forest • Synthetic HR Data")

# ---------------------------------------------------------
# Load shared resources
# ---------------------------------------------------------
data = load_data()
cleaned_data = load_cleaned_data()
artifacts = load_artifacts()

# ---------------------------------------------------------
# Tab 1: Overview
# ---------------------------------------------------------
if choice == "Overview":
    st.title("🏠 Employee Performance Predictor")
    st.markdown("""
    A data-driven machine learning system that predicts an employee's upcoming performance rating
    (**High / Medium / Low**) and surfaces actionable drivers to guide HR interventions.

    **Built with:** Python • Pandas • Scikit-learn • Random Forest • Streamlit
    """)

    col1, col2, col3, col4 = st.columns(4)

    if data is not None:
        col1.metric("Total Employees", len(data))
        col2.metric("Features", len(data.columns))
        high_pct = (data["performance_rating"] == "High").mean() * 100 if "performance_rating" in data.columns else 0
        med_pct = (data["performance_rating"] == "Medium").mean() * 100 if "performance_rating" in data.columns else 0
        low_pct = (data["performance_rating"] == "Low").mean() * 100 if "performance_rating" in data.columns else 0
        col3.metric("High Performers", f"{high_pct:.1f}%")
        col4.metric("At-Risk (Low)", f"{low_pct:.1f}%")

    st.markdown("---")
    st.subheader("📋 How It Works")
    st.markdown("""
    1. **Data Generation** – Synthetic HR dataset with 1,000 employees
    2. **Preprocessing** – Cleaning, encoding, scaling, train-test split
    3. **Model Training** – Random Forest Classifier (primary) + Logistic Regression (baseline)
    4. **Evaluation** – Accuracy, confusion matrix, classification report
    5. **Prediction** – Forecast High/Medium/Low for each employee
    6. **HR Insights** – Top drivers, at-risk list, action recommendations
    """)

    st.subheader("🎯 Key Performance Drivers")
    if os.path.exists(FEATURE_IMPORTANCE_PATH):
        fi = pd.read_csv(FEATURE_IMPORTANCE_PATH).head(5)
        fig = px.bar(fi, x="importance", y="feature", orientation="h",
                     title="Top 5 Performance Drivers",
                     color="importance", color_continuous_scale="Blues")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Run the pipeline (`python main.py`) to generate feature importance.")

# ---------------------------------------------------------
# Tab 2: Dataset Preview
# ---------------------------------------------------------
elif choice == "Dataset Preview":
    st.title("📁 Dataset Preview")
    st.markdown("Synthetic HR dataset used for training and prediction.")

    if data is not None:
        st.subheader("Dataset Overview")
        col1, col2 = st.columns(2)
        col1.metric("Rows", data.shape[0])
        col2.metric("Columns", data.shape[1])

        st.subheader("First 10 Rows")
        st.dataframe(data.head(10), use_container_width=True)

        st.subheader("Column Information")
        info_df = pd.DataFrame({
            "Column": data.columns,
            "Type": data.dtypes.astype(str),
            "Non-Null Count": data.notnull().sum(),
            "Unique Values": data.nunique()
        })
        st.dataframe(info_df, use_container_width=True)

        st.subheader("Performance Rating Distribution")
        if "performance_rating" in data.columns:
            dist = data["performance_rating"].value_counts().reset_index()
            dist.columns = ["Performance Rating", "Count"]
            fig = px.pie(dist, values="Count", names="Performance Rating",
                         title="Employee Performance Rating Distribution",
                         color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Dataset not found. Run `python main.py` to generate it.")

# ---------------------------------------------------------
# Tab 3: EDA & Analysis
# ---------------------------------------------------------
elif choice == "EDA & Analysis":
    st.title("🔍 EDA & Analysis")
    st.markdown("Exploratory Data Analysis of the employee dataset.")

    if data is not None:
        st.subheader("Numerical Feature Distributions")
        num_cols = ["age", "experience_years", "salary", "training_hours",
                    "attendance_rate", "projects_completed", "workload_score"]
        available_num = [c for c in num_cols if c in data.columns]
        selected_num = st.selectbox("Select feature", available_num)
        fig = px.histogram(data, x=selected_num, nbins=30,
                           title=f"Distribution of {selected_num}",
                           color_discrete_sequence=["#636efa"])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Feature vs Performance Rating")
        if "performance_rating" in data.columns:
            cat_feature = st.selectbox("Select categorical feature",
                                       ["department", "education_level", "job_level", "gender"])
            if cat_feature in data.columns:
                fig = px.box(data, x="performance_rating", y=selected_num,
                             color="performance_rating",
                             title=f"{selected_num} by Performance Rating",
                             category_orders={"performance_rating": ["Low", "Medium", "High"]})
                st.plotly_chart(fig, use_container_width=True)

        st.subheader("Correlation Heatmap")
        corr_data = data[num_cols + ["performance_rating"]] if "performance_rating" in data.columns else data[num_cols]
        # Encode target for correlation
        corr_df = corr_data.copy()
        if "performance_rating" in corr_df.columns:
            rating_map = {"Low": 0, "Medium": 1, "High": 2}
            corr_df["performance_rating"] = corr_df["performance_rating"].map(rating_map)
        corr = corr_df.corr()
        fig = px.imshow(corr, text_auto=True, aspect="auto",
                        title="Feature Correlation Heatmap",
                        color_continuous_scale="RdBu_r")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Department-wise Performance")
        if "department" in data.columns and "performance_rating" in data.columns:
            dept_perf = data.groupby(["department", "performance_rating"]).size().reset_index(name="Count")
            fig = px.bar(dept_perf, x="department", y="Count", color="performance_rating",
                         title="Performance Rating by Department",
                         barmode="group",
                         category_orders={"performance_rating": ["Low", "Medium", "High"]})
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Dataset not found. Run `python main.py` to generate it.")

# ---------------------------------------------------------
# Tab 4: Model Performance
# ---------------------------------------------------------
elif choice == "Model Performance":
    st.title("🎯 Model Performance")
    st.markdown("Evaluation metrics for the trained Random Forest model.")

    if artifacts is None:
        st.warning("Model not trained yet. Run `python main.py` to train the model.")
    else:
        col1, col2 = st.columns(2)
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, "r") as f:
                metrics_text = f.read()
            # Extract accuracy
            for line in metrics_text.split("\n"):
                if "Model Accuracy" in line:
                    acc = line.split(":")[1].strip().split(" ")[0]
                    col1.metric("Model Accuracy", f"{float(acc)*100:.2f}%")
                    break

        st.subheader("Confusion Matrix")
        if os.path.exists(CONFUSION_MATRIX_PATH):
            st.image(CONFUSION_MATRIX_PATH, caption="Confusion Matrix", use_column_width=True)
        else:
            st.info("Confusion matrix not found. Run `python main.py` to generate it.")

        st.subheader("Feature Importance")
        if os.path.exists(FEATURE_IMPORTANCE_PATH):
            fi = pd.read_csv(FEATURE_IMPORTANCE_PATH)
            fig = px.bar(fi.head(10), x="importance", y="feature", orientation="h",
                         title="Top 10 Feature Importance",
                         color="importance", color_continuous_scale="Viridis")
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Feature importance not found.")

        st.subheader("Classification Report")
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, "r") as f:
                st.text(f.read())

# ---------------------------------------------------------
# Tab 5: Single Prediction
# ---------------------------------------------------------
elif choice == "Single Prediction":
    st.title("🔮 Single Employee Prediction")
    st.markdown("Enter employee details to predict their performance rating.")

    if artifacts is None:
        st.warning("Model not available. Run `python main.py` to train the model first.")
    else:
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)

            with col1:
                age = st.number_input("Age", 22, 60, 30)
                experience = st.number_input("Experience (years)", 0, 40, 5)
                salary = st.number_input("Salary", 20000, 500000, 60000)
                training = st.number_input("Training Hours", 0, 120, 40)

            with col2:
                attendance = st.number_input("Attendance Rate (%)", 70.0, 100.0, 90.0)
                projects = st.number_input("Projects Completed", 0, 20, 5)
                feedback = st.selectbox("Manager Feedback Rating (1-5)", [1, 2, 3, 4, 5], index=2)
                workload = st.selectbox("Workload Score (1-10)", list(range(1, 11)), index=4)

            col3, col4 = st.columns(2)
            with col3:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                department = st.selectbox("Department",
                                          ["Sales", "Engineering", "HR", "Marketing", "Finance", "Operations", "IT"])
                education = st.selectbox("Education Level",
                                         ["High School", "Bachelor's", "Master's", "PhD"])

            with col4:
                job_level = st.selectbox("Job Level", ["Junior", "Mid", "Senior", "Lead", "Manager"])

            submitted = st.form_submit_button("Predict Performance")

        if submitted:
            employee_dict = {
                "age": age,
                "gender": gender,
                "department": department,
                "education_level": education,
                "job_level": job_level,
                "experience_years": experience,
                "salary": salary,
                "training_hours": training,
                "attendance_rate": attendance,
                "projects_completed": projects,
                "manager_feedback_rating": feedback,
                "workload_score": workload
            }

            label, probs = predict_single(employee_dict, artifacts)

            st.markdown("---")
            st.subheader("Prediction Result")

            color = {"High": "green", "Medium": "orange", "Low": "red"}.get(label, "blue")
            st.markdown(f"""
            <div style="padding: 20px; border-radius: 10px; background-color: {color}20; border: 2px solid {color};">
                <h2 style="color: {color}; margin: 0;">Predicted Performance: {label}</h2>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("Prediction Probabilities")
            prob_df = pd.DataFrame({
                "Performance Rating": list(probs.keys()),
                "Probability": list(probs.values())
            })
            fig = px.bar(prob_df, x="Performance Rating", y="Probability",
                         title="Prediction Confidence by Class",
                         color="Performance Rating",
                         color_discrete_map={"High": "green", "Medium": "orange", "Low": "red"})
            fig.update_yaxes(range=[0, 1])
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Employee Summary")
            st.json(employee_dict)

# ---------------------------------------------------------
# Tab 6: Batch Prediction
# ---------------------------------------------------------
elif choice == "Batch Prediction":
    st.title("📦 Batch Prediction")
    st.markdown("Upload a CSV file with employee data to get performance predictions for multiple employees.")

    if artifacts is None:
        st.warning("Model not available. Run `python main.py` to train the model first.")
    else:
        st.subheader("Upload CSV")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded data:")
            st.dataframe(df.head(), use_container_width=True)

            if st.button("Run Batch Prediction"):
                results = predict_batch(df, artifacts)
                st.success(f"Predictions generated for {len(results)} employees!")

                st.subheader("Pred Results")
                st.dataframe(results, use_container_width=True)

                st.subheader("Prediction Distribution")
                dist = results["predicted_performance_rating"].value_counts().reset_index()
                dist.columns = ["Performance Rating", "Count"]
                fig = px.pie(dist, values="Count", names="Performance Rating",
                             title="Batch Prediction Distribution",
                             color_discrete_map={"High": "green", "Medium": "orange", "Low": "red"})
                st.plotly_chart(fig, use_container_width=True)

                csv = results.to_csv(index=False)
                st.download_button(
                    label="Download Predictions CSV",
                    data=csv,
                    file_name="performance_predictions.csv",
                    mime="text/csv"
                )

        st.markdown("---")
        st.subheader("Or Run on Existing Dataset")
        if data is not None and st.button("Predict on Full Dataset"):
            results = predict_batch(data, artifacts)
            st.success(f"Predictions generated for {len(results)} employees!")
            st.dataframe(results.head(20), use_container_width=True)
            dist = results["predicted_performance_rating"].value_counts().reset_index()
            dist.columns = ["Performance Rating", "Count"]
            fig = px.bar(dist, x="Performance Rating", y="Count",
                         title="Full Dataset Prediction Distribution",
                         color="Performance Rating",
                         color_discrete_map={"High": "green", "Medium": "orange", "Low": "red"})
            st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# Tab 7: HR Insights
# ---------------------------------------------------------
elif choice == "HR Insights":
    st.title("👥 HR Insights & Recommendations")
    st.markdown("Actionable insights for HR decision-making.")

    if artifacts is None or data is None:
        st.warning("Model and data not available. Run `python main.py` first.")
    else:
        # Run predictions on full data
        results = predict_batch(data, artifacts)
        data_with_pred = data.copy()
        data_with_pred["predicted_performance"] = results["predicted_performance_rating"].values

        st.subheader("Prediction Summary")
        dist = data_with_pred["predicted_performance"].value_counts().reset_index()
        dist.columns = ["Performance Rating", "Count"]
        col1, col2, col3 = st.columns(3)
        for cls in ["High", "Medium", "Low"]:
            count = dist[dist["Performance Rating"] == cls]["Count"].sum() if cls in dist["Performance Rating"].values else 0
            if cls == "High":
                col1.metric("High Performers", int(count))
            elif cls == "Medium":
                col2.metric("Medium Performers", int(count))
            else:
                col3.metric("At-Risk (Low)", int(count))

        st.subheader("At-Risk Employees (Predicted Low)")
        at_risk = data_with_pred[data_with_pred["predicted_performance"] == "Low"]
        st.metric("Total At-Risk", len(at_risk))
        if len(at_risk) > 0:
            show_cols = [c for c in ["employee_id", "age", "department", "job_level",
                                     "experience_years", "training_hours", "attendance_rate",
                                     "projects_completed", "manager_feedback_rating", "workload_score"]
                         if c in at_risk.columns]
            st.dataframe(at_risk[show_cols].head(20), use_container_width=True)

        st.subheader("HR Action Recommendations")
        st.markdown("""
        | Performance Group | Recommended Actions |
        |-------------------|---------------------|
        | **High** | • Consider for promotion or leadership roles<br>• Include in retention and recognition programs<br>• Assign as mentors to other employees<br>• Offer stretch assignments |
        | **Medium** | • Provide targeted training to close skill gaps<br>• Set clear performance goals with quarterly check-ins<br>• Offer upskilling opportunities<br>• Monitor progress regularly |
        | **Low** | • Immediate coaching and performance improvement plan<br>• Investigate root causes (workload, skills, attendance)<br>• Provide additional training and support<br>• Re-evaluate role fit or consider reassignment |
        """)

        st.subheader("Top Performance Drivers")
        if os.path.exists(FEATURE_IMPORTANCE_PATH):
            fi = pd.read_csv(FEATURE_IMPORTANCE_PATH).head(8)
            fig = px.bar(fi, x="importance", y="feature", orientation="h",
                         title="Key Drivers of Employee Performance",
                         color="importance", color_continuous_scale="Blues")
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Insights Report")
        if os.path.exists(INSIGHTS_PATH):
            with open(INSIGHTS_PATH, "r") as f:
                st.text(f.read())
        else:
            st.info("Insights report not found. Run `python main.py` to generate it.")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Employee Performance Predictor | Built with Streamlit • Scikit-learn • Random Forest</p>
    <p>For placement portfolio &amp; internship proof of work</p>
</div>
""", unsafe_allow_html=True)
