import os
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "diabetes_data.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

FEATURE_COLS = [
    'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker',
    'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
    'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth',
    'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income'
]
TARGET_COL = 'Diabetes_binary'

def run_pipeline():
    print("=" * 65)
    print(" BIG DATA HEALTH ANALYTICS: DIABETES RISK PREDICTION PIPELINE")
    print("=" * 65)

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Run download_data.py first.")

    print(f"[*] Ingesting dataset from {DATA_PATH}...")
    start_t = time.time()
    df = pd.read_csv(DATA_PATH)
    print(f"[+] Loaded {len(df):,} patient records with {df.shape[1]} attributes in {time.time() - start_t:.2f}s")

    # Data Quality & Missing Value Check
    null_counts = df.isnull().sum().sum()
    print(f"[+] Missing values found: {null_counts}")
    
    # Target distribution
    target_counts = df[TARGET_COL].value_counts().to_dict()
    print(f"[+] Class distribution: Non-Diabetic (0): {int(target_counts.get(0.0, 0)):,}, Diabetic/Pre-diabetic (1): {int(target_counts.get(1.0, 0)):,}")
    prevalence = (target_counts.get(1.0, 0) / len(df)) * 100
    print(f"[+] Disease prevalence: {prevalence:.2f}%")

    X = df[FEATURE_COLS]
    y = df[TARGET_COL].astype(int)

    # Train / Test split with stratification to preserve class proportion
    print("\n[*] Performing 80/20 Stratified Split...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"[+] Training set: {len(X_train):,} samples | Testing set: {len(X_test):,} samples")

    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Model definitions
    # Note: Using class_weight='balanced' to handle medical class imbalance
    models = {
        "Logistic Regression": {
            "model": LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
            "use_scaled": True
        },
        "Random Forest (100 Trees)": {
            "model": RandomForestClassifier(n_estimators=100, max_depth=12, class_weight='balanced', random_state=42, n_jobs=-1),
            "use_scaled": False
        },
        "HistGradientBoosting": {
            "model": HistGradientBoostingClassifier(max_iter=150, max_depth=8, class_weight='balanced', random_state=42),
            "use_scaled": False
        }
    }

    results = {}
    roc_data = {}
    best_model_name = None
    best_roc_auc = -1.0

    print("\n" + "-" * 65)
    print(" BENCHMARKING DISTRIBUTED / ENSEMBLE MACHINE LEARNING MODELS")
    print("-" * 65)

    for name, config in models.items():
        print(f"\n[>] Training {name}...")
        m_start = time.time()
        m = config["model"]
        
        train_features = X_train_scaled if config["use_scaled"] else X_train
        test_features = X_test_scaled if config["use_scaled"] else X_test

        m.fit(train_features, y_train)
        train_time = time.time() - m_start
        print(f"    Completed training in {train_time:.2f} seconds")

        # Predictions
        y_pred = m.predict(test_features)
        y_prob = m.predict_proba(test_features)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_data[name] = {"fpr": fpr, "tpr": tpr, "auc": auc}

        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(auc), 4),
            "train_time_sec": round(float(train_time), 2)
        }

        print(f"    ROC-AUC: {auc:.4f} | Recall: {rec:.4f} | Precision: {prec:.4f} | F1: {f1:.4f} | Accuracy: {acc:.4f}")

        if auc > best_roc_auc:
            best_roc_auc = auc
            best_model_name = name

    print("\n" + "=" * 65)
    print(f"[BEST MODEL] Optimal Classifier: {best_model_name} (ROC-AUC: {best_roc_auc:.4f})")
    print("=" * 65)

    # Save Metrics JSON
    metrics_path = os.path.join(MODELS_DIR, "metrics_summary.json")
    with open(metrics_path, "w") as f:
        json.dump({
            "dataset_records": len(df),
            "features": FEATURE_COLS,
            "best_model": best_model_name,
            "benchmark_results": results
        }, f, indent=4)
    print(f"[+] Benchmark metrics saved to: {metrics_path}")

    # Plot & Save ROC Curves
    plt.figure(figsize=(8, 6))
    for name, r in roc_data.items():
        plt.plot(r["fpr"], r["tpr"], lw=2, label=f"{name} (AUC = {r['auc']:.3f})")
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--', label='Random Chance (AUC = 0.500)')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=12)
    plt.ylabel('True Positive Rate (Sensitivity / Recall)', fontsize=12)
    plt.title('ROC Curves Comparison - Diabetes Risk Prediction', fontsize=14, fontweight='bold')
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(alpha=0.3)
    roc_plot_path = os.path.join(REPORTS_DIR, "roc_curve.png")
    plt.tight_layout()
    plt.savefig(roc_plot_path, dpi=300)
    plt.close()
    print(f"[+] Saved ROC curve comparison to: {roc_plot_path}")

    # Best Model Confusion Matrix
    best_config = models[best_model_name]
    best_model = best_config["model"]
    test_feat = X_test_scaled if best_config["use_scaled"] else X_test
    best_preds = best_model.predict(test_feat)
    cm = confusion_matrix(y_test, best_preds)

    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Healthy (0)', 'Diabetic (1)'],
                yticklabels=['Healthy (0)', 'Diabetic (1)'])
    plt.xlabel('Predicted Class', fontsize=12)
    plt.ylabel('Actual Class', fontsize=12)
    plt.title(f'Confusion Matrix ({best_model_name})', fontsize=14, fontweight='bold')
    cm_plot_path = os.path.join(REPORTS_DIR, "confusion_matrix.png")
    plt.tight_layout()
    plt.savefig(cm_plot_path, dpi=300)
    plt.close()
    print(f"[+] Saved Confusion Matrix to: {cm_plot_path}")

    # Feature Importance Plot (From Random Forest or Tree-based model)
    rf_model = models["Random Forest (100 Trees)"]["model"]
    importances = rf_model.feature_importances_
    feat_series = pd.Series(importances, index=FEATURE_COLS).sort_values(ascending=True)

    plt.figure(figsize=(9, 7))
    feat_series.plot(kind='barh', color='#2b5c8f')
    plt.xlabel('Relative Feature Importance Score', fontsize=12)
    plt.title('Clinical & Lifestyle Feature Importance (Random Forest)', fontsize=14, fontweight='bold')
    plt.grid(axis='x', alpha=0.3)
    fi_plot_path = os.path.join(REPORTS_DIR, "feature_importance.png")
    plt.tight_layout()
    plt.savefig(fi_plot_path, dpi=300)
    plt.close()
    print(f"[+] Saved Feature Importance chart to: {fi_plot_path}")

    # Serialize Best Pipeline Artifact
    pipeline_artifact = {
        "model_name": best_model_name,
        "model": best_model,
        "scaler": scaler,
        "use_scaled": best_config["use_scaled"],
        "feature_names": FEATURE_COLS,
        "feature_importances": feat_series.to_dict()
    }
    model_save_path = os.path.join(MODELS_DIR, "diabetes_pipeline.joblib")
    joblib.dump(pipeline_artifact, model_save_path)
    print(f"\n[SUCCESS] Production model pipeline saved successfully to: {model_save_path}")
    print("[SUCCESS] Model training and evaluation successfully completed!")

if __name__ == "__main__":
    run_pipeline()
