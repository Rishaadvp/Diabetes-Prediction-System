import os
import json
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Set Page Configuration
st.set_page_config(
    page_title="Diabetes Risk Analytics System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "diabetes_pipeline.joblib")
METRICS_PATH = os.path.join(BASE_DIR, "models", "metrics_summary.json")
ROC_PATH = os.path.join(BASE_DIR, "reports", "roc_curve.png")
CM_PATH = os.path.join(BASE_DIR, "reports", "confusion_matrix.png")
FI_PATH = os.path.join(BASE_DIR, "reports", "feature_importance.png")

@st.cache_resource
def load_pipeline():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

@st.cache_data
def load_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            return json.load(f)
    return None

pipeline = load_pipeline()
metrics_summary = load_metrics()

# App Header
st.title("🩺 Big Data Health Analytics: Diabetes Risk Prediction")
st.markdown(
    """
    **Project Scope**: Large-scale clinical risk screening using the **CDC BRFSS Healthcare Dataset (253,680 records)**.  
    Trained on distributed ensemble architectures to deliver early preventive screening and factor explainability.
    """
)

# Top Metric Banner
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Total Patient Records", "253,680", "CDC BRFSS")
with col_m2:
    st.metric("Clinical Features", "21 Indicators", "Demographic & Vitals")
with col_m3:
    best_auc = "0.830"
    if metrics_summary and "benchmark_results" in metrics_summary:
        best_name = metrics_summary.get("best_model")
        best_auc = f"{metrics_summary['benchmark_results'][best_name]['roc_auc']:.3f}"
    st.metric("Best Model ROC-AUC", best_auc, "High Discrimination")
with col_m4:
    best_algo = metrics_summary.get("best_model", "HistGradientBoosting") if metrics_summary else "HistGradientBoosting"
    st.metric("Optimal Model", best_algo)

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🔍 Patient Clinical Predictor", "📊 Big Data Model Benchmarks", "🏗 Architecture & Methodology"])

with tab1:
    st.subheader("Patient Clinical & Lifestyle Assessment")
    st.info("Fill in the patient's demographic, biometric, and lifestyle parameters to compute the real-time diabetes risk probability.")

    with st.form("patient_form"):
        st.markdown("### 1. Demographics & General Indicators")
        d_col1, d_col2, d_col3, d_col4 = st.columns(4)
        with d_col1:
            sex = st.selectbox("Biological Sex", options=[("Female", 0), ("Male", 1)], format_func=lambda x: x[0])[1]
        with d_col2:
            age_labels = [
                ("18 - 24 years", 1), ("25 - 29 years", 2), ("30 - 34 years", 3),
                ("35 - 39 years", 4), ("40 - 44 years", 5), ("45 - 49 years", 6),
                ("50 - 54 years", 7), ("55 - 59 years", 8), ("60 - 64 years", 9),
                ("65 - 69 years", 10), ("70 - 74 years", 11), ("75 - 79 years", 12),
                ("80+ years", 13)
            ]
            age = st.selectbox("Age Bracket", options=age_labels, format_func=lambda x: x[0], index=6)[1]
        with d_col3:
            education_labels = [
                ("Never attended school / Kindergarten", 1),
                ("Elementary (Grades 1-8)", 2),
                ("Some High School (Grades 9-11)", 3),
                ("High School Graduate (Grade 12)", 4),
                ("Some College or Technical School", 5),
                ("College Graduate (4+ years)", 6)
            ]
            education = st.selectbox("Education Level", options=education_labels, format_func=lambda x: x[0], index=3)[1]
        with d_col4:
            income_labels = [
                ("Less than $10,000", 1), ("$10,000 to <$15,000", 2),
                ("$15,000 to <$20,000", 3), ("$20,000 to <$25,000", 4),
                ("$25,000 to <$35,000", 5), ("$35,000 to <$50,000", 6),
                ("$50,000 to <$75,000", 7), ("$75,000 or more", 8)
            ]
            income = st.selectbox("Annual Household Income", options=income_labels, format_func=lambda x: x[0], index=5)[1]

        st.markdown("### 2. Clinical Vitals & Biometrics")
        v_col1, v_col2, v_col3, v_col4 = st.columns(4)
        with v_col1:
            bmi = st.slider("Body Mass Index (BMI)", min_value=14.0, max_value=60.0, value=27.5, step=0.5)
            if bmi < 18.5:
                st.caption("Underweight")
            elif bmi < 25.0:
                st.caption("Normal weight")
            elif bmi < 30.0:
                st.caption("Overweight")
            else:
                st.caption("Obese (Elevated Risk)")
        with v_col2:
            high_bp = st.radio("High Blood Pressure?", options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0], horizontal=True)[1]
        with v_col3:
            high_chol = st.radio("High Cholesterol?", options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0], horizontal=True)[1]
        with v_col4:
            chol_check = st.radio("Cholesterol Check (past 5 yrs)?", options=[("Yes", 1), ("No", 0)], format_func=lambda x: x[0], horizontal=True)[1]

        st.markdown("### 3. Medical History & Chronic Conditions")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            stroke = st.radio("History of Stroke?", options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0], horizontal=True)[1]
        with m_col2:
            heart_disease = st.radio("Coronary Heart Disease / Myocardial Infarction?", options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0], horizontal=True)[1]
        with m_col3:
            diff_walk = st.radio("Difficulty Walking / Climbing Stairs?", options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0], horizontal=True)[1]
        with m_col4:
            any_healthcare = st.radio("Has Health Insurance / Coverage?", options=[("Yes", 1), ("No", 0)], format_func=lambda x: x[0], horizontal=True)[1]

        st.markdown("### 4. Lifestyle & Self-Assessed Wellbeing")
        l_col1, l_col2, l_col3, l_col4 = st.columns(4)
        with l_col1:
            smoker = st.radio("Smoked at least 100 cigarettes in life?", options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0], horizontal=True)[1]
            hvy_alcohol = st.radio("Heavy Drinker (Men >14/wk, Women >7/wk)?", options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0], horizontal=True)[1]
        with l_col2:
            phys_activity = st.radio("Regular Physical Activity / Exercise?", options=[("Yes", 1), ("No", 0)], format_func=lambda x: x[0], horizontal=True)[1]
            nodoc_cost = st.radio("Skipped Doctor in past year due to cost?", options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0], horizontal=True)[1]
        with l_col3:
            fruits = st.radio("Consumes Fruit 1+ times per day?", options=[("Yes", 1), ("No", 0)], format_func=lambda x: x[0], horizontal=True)[1]
            veggies = st.radio("Consumes Vegetables 1+ times per day?", options=[("Yes", 1), ("No", 0)], format_func=lambda x: x[0], horizontal=True)[1]
        with l_col4:
            gen_hlth_labels = [
                ("1 - Excellent", 1), ("2 - Very Good", 2),
                ("3 - Good", 3), ("4 - Fair", 4), ("5 - Poor", 5)
            ]
            gen_hlth = st.selectbox("General Health Self-Rating", options=gen_hlth_labels, format_func=lambda x: x[0], index=2)[1]
            phys_hlth = st.slider("Days Physical Health Not Good (past 30 days)", 0, 30, 0)
            ment_hlth = st.slider("Days Mental Health Not Good (past 30 days)", 0, 30, 0)

        submit_btn = st.form_submit_button("🚀 Compute Diabetes Risk Assessment", use_container_width=True)

    if submit_btn:
        if pipeline is None:
            st.error("Model artifact not found. Please run `python train_model.py` first to generate the trained model.")
        else:
            model = pipeline["model"]
            scaler = pipeline["scaler"]
            use_scaled = pipeline["use_scaled"]
            feature_cols = pipeline["feature_names"]

            patient_data = {
                'HighBP': high_bp, 'HighChol': high_chol, 'CholCheck': chol_check,
                'BMI': bmi, 'Smoker': smoker, 'Stroke': stroke,
                'HeartDiseaseorAttack': heart_disease, 'PhysActivity': phys_activity,
                'Fruits': fruits, 'Veggies': veggies, 'HvyAlcoholConsump': hvy_alcohol,
                'AnyHealthcare': any_healthcare, 'NoDocbcCost': nodoc_cost,
                'GenHlth': gen_hlth, 'MentHlth': ment_hlth, 'PhysHlth': phys_hlth,
                'DiffWalk': diff_walk, 'Sex': sex, 'Age': age,
                'Education': education, 'Income': income
            }

            input_df = pd.DataFrame([patient_data])[feature_cols]
            test_input = scaler.transform(input_df) if use_scaled else input_df

            prob = float(model.predict_proba(test_input)[0, 1])
            risk_percent = prob * 100

            st.markdown("---")
            st.subheader("🎯 Diagnostic Risk Evaluation")

            r_col1, r_col2 = st.columns([1, 2])
            with r_col1:
                st.metric(label="Predicted Diabetes Risk Score", value=f"{risk_percent:.1f}%")
                if risk_percent < 35.0:
                    st.success("🟢 **LOW RISK**: Routine periodic wellness checks recommended.")
                elif risk_percent < 60.0:
                    st.warning("🟡 **MODERATE RISK**: Lifestyle interventions (diet, aerobic activity) and fasting glucose screening recommended.")
                else:
                    st.error("🔴 **HIGH RISK**: Immediate clinical evaluation (HbA1c test and primary physician consult) strongly indicated.")

            with r_col2:
                st.markdown("#### Patient Risk Trigger Breakdown")
                risk_factors = []
                if high_bp == 1:
                    risk_factors.append("• **Hypertension**: High blood pressure is a primary clinical comorbidity of metabolic syndrome.")
                if high_chol == 1:
                    risk_factors.append("• **Dyslipidemia**: Elevated cholesterol increases vascular and insulin resistance risk.")
                if bmi >= 30.0:
                    risk_factors.append(f"• **Obesity (BMI {bmi:.1f})**: High adipose tissue strongly correlates with peripheral insulin resistance.")
                elif bmi >= 25.0:
                    risk_factors.append(f"• **Overweight (BMI {bmi:.1f})**: Modest weight management can curb prediabetic onset.")
                if age >= 8:
                    risk_factors.append("• **Age Bracket (>55 yrs)**: Beta-cell function and insulin sensitivity decline with advancing age.")
                if gen_hlth >= 4:
                    risk_factors.append("• **Impaired Self-Assessed Health**: Correlated with systemic chronic inflammation.")
                if phys_activity == 0:
                    risk_factors.append("• **Sedentary Lifestyle**: Lack of physical activity reduces glucose uptake in skeletal muscle.")

                if risk_factors:
                    for rf in risk_factors:
                        st.markdown(rf)
                else:
                    st.markdown("• No major adverse lifestyle or biometric triggers detected. Maintain balanced diet and regular exercise.")

with tab2:
    st.subheader("Model Benchmarks & Scalable Analytics")
    if metrics_summary:
        bench_df = pd.DataFrame(metrics_summary["benchmark_results"]).T
        st.dataframe(bench_df.style.highlight_max(axis=0, color='#d4edda'), use_container_width=True)

    img_col1, img_col2 = st.columns(2)
    with img_col1:
        if os.path.exists(ROC_PATH):
            st.image(ROC_PATH, caption="Area Under the ROC Curve (Model Comparison)", use_container_width=True)
    with img_col2:
        if os.path.exists(CM_PATH):
            st.image(CM_PATH, caption="Confusion Matrix on Test Population", use_container_width=True)

    if os.path.exists(FI_PATH):
        st.image(FI_PATH, caption="Clinical & Lifestyle Feature Importance Ranking", use_container_width=True)

with tab3:
    st.subheader("Big Data Architecture & Pipeline Methodology")
    st.markdown(
        """
        ### 1. Data Scale & Source
        - **Source**: Centers for Disease Control and Prevention (CDC) - Behavioral Risk Factor Surveillance System (BRFSS).
        - **Volume**: **253,680 records**, 21 features across clinical history, demographic indicators, and lifestyle metrics.
        - **Target**: `Diabetes_binary` (0: Healthy, 1: Diabetic / Pre-diabetic).

        ### 2. Big Data Challenges & Solutions
        - **Class Imbalance**: Diabetic records constitute ~14% of the population. Addressed via cost-sensitive learning (`class_weight='balanced'`) to avoid false-negative bias.
        - **Scalability**: Evaluated high-speed histogram-based gradient boosting (`HistGradientBoostingClassifier`), engineered specifically for massive tabular datasets with binning optimizations.
        - **Metric Prioritization**: Standard accuracy is misleading in medical datasets; models were optimized and evaluated on **ROC-AUC (Receiver Operating Characteristic - Area Under Curve)** and **Sensitivity / Recall**.
        """
    )
