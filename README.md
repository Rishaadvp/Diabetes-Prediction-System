# Big Data Health Analytics: Scalable Diabetes Risk Prediction System

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Domain](https://img.shields.io/badge/Domain-Healthcare%20Big%20Data-brightgreen.svg)
![Dataset](https://img.shields.io/badge/Dataset-CDC%20BRFSS%20(253k%2B%20records)-orange.svg)
![ROC-AUC](https://img.shields.io/badge/ROC--AUC-0.827-success.svg)

An end-to-end Big Data Analytics (BDA) project for population-scale Diabetes Risk Screening using the **CDC Behavioral Risk Factor Surveillance System (BRFSS 2015)** dataset (253,680 patient records, 21 clinical & lifestyle features).

---

## 🌟 Key Features
- **True Big Data Scale**: Analyzes 253,680 patient encounters, moving beyond small toy datasets.
- **Handling Class Imbalance**: Incorporates cost-sensitive learning to counter medical class skew (~14% diabetic prevalence).
- **Multi-Model Distributed Benchmarks**: Evaluates **Logistic Regression**, **Random Forest Ensemble (100 Trees)**, and **Histogram-based Gradient Boosting** (`HistGradientBoostingClassifier`).
- **Clinical Decision Support**: Delivers an interactive **Streamlit** clinical dashboard with real-time risk calculations, individual risk trigger breakdown, and performance visualizations.
- **Model Explainability (XAI)**: Attributes risk to biometric triggers (General Health, BMI, Hypertension, Age, and Dyslipidemia).

---

## 📊 Benchmark Results (Tested on 50,736 Unseen Patients)

| Model | ROC-AUC | Recall (Sensitivity) | Precision | F1-Score | Accuracy | Training Speed |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HistGradientBoosting** *(Optimal)* | **0.8268** | **79.46%** | **30.55%** | **0.4413** | **71.97%** | **4.39s** |
| **Random Forest (100 Trees)** | 0.8227 | 73.99% | 32.17% | 0.4484 | 74.64% | 4.07s |
| **Logistic Regression** | 0.8196 | 76.11% | 31.07% | 0.4413 | 73.15% | 0.27s |

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download CDC BRFSS Dataset (253k rows)
```bash
python download_data.py
```

### 3. Run Distributed Training & Evaluation
```bash
python train_model.py
```

### 4. Launch Interactive Web App
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Repository Structure
```
bda/
├── data/
│   └── diabetes_data.csv          # CDC BRFSS dataset (253,680 records)
├── models/
│   ├── diabetes_pipeline.joblib   # Serialized production pipeline
│   └── metrics_summary.json       # Benchmarking metrics
├── reports/
│   ├── roc_curve.png              # ROC curves for all models
│   ├── confusion_matrix.png       # Test set confusion matrix
│   └── feature_importance.png     # Feature importance ranking
├── app.py                         # Interactive Streamlit application
├── download_data.py               # Streaming dataset downloader
├── train_model.py                 # Multi-model training pipeline
├── PROJECT_REPORT.md              # Academic project report & Viva Q&A
├── requirements.txt               # Python package dependencies
└── README.md                      # Project documentation
```

---

## 📖 Academic Documentation
Detailed problem formulation, mathematical background, architectural diagrams, and university viva defense questions are available in [PROJECT_REPORT.md](PROJECT_REPORT.md).
