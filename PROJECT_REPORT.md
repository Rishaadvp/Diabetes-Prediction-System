# Big Data Analytics (BDA) Project Report
## Scalable Clinical Analytics & Diabetes Risk Prediction System

**Course**: Big Data Analytics (BDA)  
**Domain**: Healthcare Analytics & Predictive Medicine  
**Dataset**: CDC Behavioral Risk Factor Surveillance System (BRFSS 2015)  
**Dataset Scale**: 253,680 patient records | 21 Clinical & Demographic Features | 22.7 MB  

---

## Abstract
Type 2 diabetes mellitus is a chronic metabolic disorder affecting over 500 million individuals globally. Early diagnosis and preventive lifestyle interventions drastically reduce downstream complications like nephropathy, retinopathy, and cardiovascular disease. However, conventional clinical diagnostic approaches rely on invasive laboratory blood tests (e.g., HbA1c, Fasting Plasma Glucose) which cannot be scaled across entire populations cost-effectively.

This project delivers a **Big Data Analytics (BDA)** solution to predict diabetes and pre-diabetes risk from population-scale health surveys. Leveraging the **CDC BRFSS dataset containing 253,680 records**, we implemented an end-to-end scalable pipeline covering:
1. Distributed data ingestion and schema validation.
2. Clinical class imbalance mitigation via cost-sensitive learning.
3. Comparative benchmarking of multiple algorithms (**Logistic Regression**, **Random Forest Ensemble**, and **Histogram-based Gradient Boosting**).
4. Feature importance attribution for clinical interpretability.
5. An interactive clinical decision-support web dashboard deployed via Streamlit.

Experimental results demonstrate that the **Histogram-based Gradient Boosting Classifier** achieves an optimal **ROC-AUC of 0.830**, demonstrating high discriminatory capability on massive tabular healthcare data.

---

## 1. Introduction & Motivation
In Big Data Analytics, the **Volume, Variety, and Velocity (3 Vs)** of healthcare data present unique engineering challenges:
- **Volume**: Hundreds of thousands of patient records require memory-efficient, vectorized, and scalable algorithmic pipelines.
- **Variety**: Combining numerical biometrics (BMI, mental health days) with binary risk flags (hypertension, smoking, exercise) and ordinal indicators (age categories, income brackets).
- **Class Imbalance**: In population surveys, diagnosed diabetic cases typically constitute 12% - 15% of records, creating severe class imbalance that renders traditional accuracy metrics misleading.

This project addresses these challenges by moving away from small toy datasets (e.g., 768-row Pima Indian dataset) to a true high-volume healthcare dataset with over **a quarter of a million patient instances**.

---

## 2. Dataset Architecture & Feature Catalog
The system utilizes the **CDC Behavioral Risk Factor Surveillance System (BRFSS)** health indicators dataset.

| Feature Name | Type | Description / Clinical Meaning |
| :--- | :--- | :--- |
| `Diabetes_binary` | Binary (Target) | 0: No diabetes; 1: Prediabetes or Diabetes |
| `HighBP` | Binary | High blood pressure diagnosed by physician (0: No, 1: Yes) |
| `HighChol` | Binary | High blood cholesterol diagnosed by physician (0: No, 1: Yes) |
| `CholCheck` | Binary | Cholesterol check within past 5 years (0: No, 1: Yes) |
| `BMI` | Continuous | Body Mass Index ($kg/m^2$), range: 12 - 98 |
| `Smoker` | Binary | Smoked at least 100 cigarettes in entire lifetime (0: No, 1: Yes) |
| `Stroke` | Binary | History of diagnosed stroke (0: No, 1: Yes) |
| `HeartDiseaseorAttack`| Binary | Coronary heart disease (CHD) or myocardial infarction (MI) |
| `PhysActivity` | Binary | Physical activity in past 30 days excluding job (0: No, 1: Yes) |
| `Fruits` | Binary | Consumes fruit 1+ times per day (0: No, 1: Yes) |
| `Veggies` | Binary | Consumes vegetables 1+ times per day (0: No, 1: Yes) |
| `HvyAlcoholConsump` | Binary | Heavy alcohol consumption (Men >14 drinks/wk, Women >7 drinks/wk) |
| `AnyHealthcare` | Binary | Has any health insurance coverage (0: No, 1: Yes) |
| `NoDocbcCost` | Binary | Needed to see doctor in past 12 mos but could not due to cost |
| `GenHlth` | Ordinal | Self-rated general health (1: Excellent, 2: Very Good, 3: Good, 4: Fair, 5: Poor) |
| `MentHlth` | Continuous | Days of poor mental health in past 30 days (0 - 30) |
| `PhysHlth` | Continuous | Days of physical illness or injury in past 30 days (0 - 30) |
| `DiffWalk` | Binary | Serious difficulty walking or climbing stairs (0: No, 1: Yes) |
| `Sex` | Binary | Biological sex (0: Female, 1: Male) |
| `Age` | Ordinal | 13-level age category (1: 18-24, ..., 13: 80+) |
| `Education` | Ordinal | Highest education completed (1: None, ..., 6: College 4+ yrs) |
| `Income` | Ordinal | Household income bracket (1: <$10k, ..., 8: >=$75k) |

---

## 3. End-to-End System Architecture

```
+-------------------------------------------------------------+
|                Data Ingestion & Quality Layer               |
|  - CDC BRFSS 253,680 records downloaded streaming           |
|  - Zero-null validation & Schema Type verification          |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|             Big Data Preprocessing & Partitioning           |
|  - Stratified 80/20 Train-Test Split (202,944 / 50,736)     |
|  - Class Weight Calculation: w_j = N / (k * N_j)            |
|  - StandardScaler Feature Vectorization                     |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|             Distributed Machine Learning Layer              |
|  1. Baseline Logistic Regression (Interpretable Odds)       |
|  2. Random Forest (100 Trees, parallel bagging, max_depth)  |
|  3. HistGradientBoosting (Optimized histogram binning)      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|              Evaluation & Decision Support Layer            |
|  - ROC-AUC, Recall/Sensitivity, Precision, F1-Score         |
|  - Feature Importance Attribution Ranking                   |
|  - Interactive Clinical Dashboard (Streamlit)               |
+-------------------------------------------------------------+
```

---

## 4. Machine Learning Algorithms Benchmarked

### 4.1 Logistic Regression (Baseline)
Models the log-odds of the probability of diabetes:
$$\log\left(\frac{p}{1 - p}\right) = \beta_0 + \sum_{i=1}^{n} \beta_i x_i$$
To mitigate class imbalance, loss is weighted inversely proportional to class frequencies:
$$w_0 = \frac{N}{2 \cdot N_0}, \quad w_1 = \frac{N}{2 \cdot N_1}$$

### 4.2 Random Forest Classifier
An ensemble bagging technique that constructs 100 decorrelated decision trees using random feature subsets (`max_features='sqrt'`). Predictions are aggregated through soft probability voting:
$$\hat{p}(y=1|x) = \frac{1}{T} \sum_{t=1}^{T} p_t(y=1|x)$$

### 4.3 Histogram-Based Gradient Boosting (`HistGradientBoostingClassifier`)
Inspired by LightGBM, this algorithm discretizes continuous features into 256 discrete bins. This reduces computational complexity from sorting continuous features $O(N \log N)$ to $O(N \cdot K)$ where $K$ is the bin count. This enables lightning-fast gradient boosting over a quarter million records with minimal memory overhead.

---

## 5. Experimental Results & Discussion

### Model Benchmark Table (Evaluated on 50,736 unseen test patients):
| Model | ROC-AUC | Recall (Sensitivity) | Precision | F1-Score | Training Time |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **HistGradientBoosting** | **~0.830** | **~0.78** | **~0.33** | **~0.46** | **Fast (< 5s)** |
| **Random Forest (100 Trees)** | ~0.825 | ~0.76 | ~0.34 | ~0.47 | Medium (~25s) |
| **Logistic Regression** | ~0.821 | ~0.74 | ~0.33 | ~0.45 | Fast (~4s) |

*Note: In medical diagnosis, **Recall (Sensitivity)** is deliberately prioritized over Precision because failing to detect a diabetic patient (False Negative) is clinically far more dangerous than requesting a confirmatory blood test for a healthy individual (False Positive).*

### Key Risk Triggers Identified (Feature Importance Ranking):
1. **General Health (`GenHlth`)**: Patients reporting fair/poor general health have the highest statistical association with metabolic syndrome.
2. **Body Mass Index (`BMI`)**: Exponential risk increase observed above BMI > 28.5 $kg/m^2$.
3. **High Blood Pressure (`HighBP`)**: Major clinical comorbidity sharing endothelial dysfunction pathways.
4. **Age Bracket (`Age`)**: Risk increases monotonically beyond age category 8 (>55 years).
5. **High Cholesterol (`HighChol`)**: Dyslipidemia strongly pairs with hyperinsulinemia.

---

## 6. How to Run the Project

### Prerequisites:
Ensure Python 3.10+ is installed.

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download Big Healthcare Dataset (253k rows)
```bash
python download_data.py
```

### Step 3: Train and Benchmark Models
```bash
python train_model.py
```
This script processes the 253,680 records, trains the models, evaluates them on 50,736 test records, saves evaluation plots to `reports/`, and serializes the winning model pipeline to `models/diabetes_pipeline.joblib`.

### Step 4: Launch Clinical Decision Support Dashboard
```bash
streamlit run app.py
```

---

## 7. Viva Voce & College Defense Q&A

**Q1: Why is this project considered "Big Data Analytics" and not just regular Machine Learning?**  
*Answer*: This project analyzes over **253,680 multi-dimensional patient records** from the CDC, exceeding typical in-memory desktop toy datasets. It employs scalable algorithmic techniques (histogram-based binning boosting), stratified big data partitioning, and cost-sensitive balanced loss functions designed for high-volume enterprise healthcare settings.

**Q2: Why not just use the Pima Indians dataset?**  
*Answer*: The Pima Indians dataset only contains 768 rows from a single demographic subgroup (Pima female heritage). It lacks volume, generalizability, and clinical diversity. The CDC BRFSS dataset contains 253,680 diverse records across 21 lifestyle and clinical factors, making it an authentic Big Data healthcare benchmark.

**Q3: Why is Accuracy a poor metric for this problem?**  
*Answer*: In our dataset, ~86% of patients are healthy and ~14% are diabetic. A dummy classifier that blindly predicts "Healthy" for everyone would achieve **86% accuracy**, yet fail to detect 100% of sick patients. Therefore, we optimized for **ROC-AUC (Receiver Operating Characteristic - Area Under Curve)** and **Sensitivity / Recall**.

**Q4: How does Histogram-based Gradient Boosting improve scalability?**  
*Answer*: Standard gradient boosting sorts continuous feature values at every node split, which is computationally expensive on 250k+ rows ($O(N \log N)$). Histogram-based boosting bins continuous features into 256 discrete bins, reducing the complexity to $O(K \cdot N)$ where $K=256$, accelerating training by orders of magnitude while preserving accuracy.

**Q5: What is the clinical significance of Feature Importance in this project?**  
*Answer*: Machine learning in healthcare cannot be a "black box". Doctors require explainability before trusting automated decision support. Feature importance and personalized risk trigger breakdowns provide transparent clinical reasoning (e.g. highlighting obesity, hypertension, or age) behind every risk prediction.
