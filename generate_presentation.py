import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PPTX = os.path.join(BASE_DIR, "Big_Data_Diabetes_Prediction_Presentation.pptx")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Color Palette
NAVY = RGBColor(27, 54, 93)        # #1B365D
TEAL = RGBColor(13, 148, 136)      # #0D9488
DARK_GRAY = RGBColor(55, 65, 81)   # #374151
LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
BOX_BG = RGBColor(241, 245, 249)   # #F1F5F9
WHITE = RGBColor(255, 255, 255)
ACCENT_BLUE = RGBColor(37, 99, 235)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]

def create_header(slide, title_text, category_text="BIG DATA ANALYTICS (BDA) HEALTHCARE PROJECT"):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = TEAL
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY

def add_rationale_box(slide, why_text, relevance_text):
    left = Inches(0.8)
    top = Inches(5.8)
    width = Inches(11.7)
    height = Inches(1.3)
    
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = BOX_BG
    shape.line.color.rgb = TEAL
    shape.line.width = Pt(1.5)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.15)
    tf.margin_right = Inches(0.2)
    
    p1 = tf.paragraphs[0]
    p1.text = "WHY THIS IS HERE: " + why_text
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = NAVY
    
    p2 = tf.add_paragraph()
    p2.text = "BDA RELEVANCE: " + relevance_text
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = TEAL

# ==============================================================================
# SLIDE 1: Title Slide
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)

bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = NAVY
bg1.line.color.rgb = NAVY

tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.8))
tf1 = tb1.text_frame
tf1.word_wrap = True

p_sub = tf1.paragraphs[0]
p_sub.text = "BIG DATA ANALYTICS (BDA) | HEALTHCARE DECISION SUPPORT"
p_sub.font.size = Pt(14)
p_sub.font.bold = True
p_sub.font.color.rgb = TEAL

p_main = tf1.add_paragraph()
p_main.text = "Scalable Diabetes Risk Prediction\n& Clinical Analytics System"
p_main.font.size = Pt(36)
p_main.font.bold = True
p_main.font.color.rgb = WHITE

p_desc = tf1.add_paragraph()
p_desc.text = "Population-Scale Predictive Screening on 253,680 CDC Patient Encounters using Distributed Machine Learning & Explainable AI"
p_desc.font.size = Pt(16)
p_desc.font.color.rgb = RGBColor(203, 213, 225)

p_author = tf1.add_paragraph()
p_author.text = "\nPresenter: Rishaadvp  |  Dataset: CDC BRFSS 2015 (253k rows, 21 attributes)  |  Target: BDA Project"
p_author.font.size = Pt(14)
p_author.font.bold = True
p_author.font.color.rgb = WHITE

notes1 = slide1.notes_slide.notes_text_frame
notes1.text = "Speaker Notes:\nWelcome professors and evaluators. Today I am presenting our Big Data Analytics project: Scalable Diabetes Risk Prediction and Clinical Analytics. We developed an end-to-end distributed screening system trained on over a quarter of a million real-world patient records from the CDC."

# ==============================================================================
# SLIDE 2: Clinical Problem & Big Data Motivation
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
create_header(slide2, "Clinical Problem & Big Data Motivation")

c_box = slide2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.9))
tf2 = c_box.text_frame
tf2.word_wrap = True

def add_bullet(tf, heading, text):
    p = tf.add_paragraph()
    p.text = heading + ": "
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = NAVY
    p.level = 0
    
    p2 = tf.add_paragraph()
    p2.text = text
    p2.font.size = Pt(13)
    p2.font.color.rgb = DARK_GRAY
    p2.level = 1

tf2.paragraphs[0].text = "Why Traditional Healthcare Systems Struggle With Metabolic Screening:"
tf2.paragraphs[0].font.size = Pt(15)
tf2.paragraphs[0].font.bold = True
tf2.paragraphs[0].font.color.rgb = TEAL

add_bullet(tf2, "1. Global Disease Epidemic", "Over 537 million adults live with diabetes globally. Early detection reduces irreversible complications like kidney failure, blindness, and cardiovascular disease.")
add_bullet(tf2, "2. Invasive Lab Tests Cannot Scale", "Standard clinical diagnosis relies on venous blood draws (HbA1c / Fasting Plasma Glucose), which are expensive, invasive, and impossible to administer universally.")
add_bullet(tf2, "3. The Big Data Opportunity", "Routine public health behavioral surveys (CDC BRFSS) collect demographic and biometric indicators at massive scale, enabling automated non-invasive risk screening.")

add_rationale_box(
    slide2,
    "Clearly establishes the high-stakes clinical necessity and why Big Data is the only feasible paradigm to solve population-level screening.",
    "Maps directly to the 3 Vs of Big Data: High Volume (250k+ records), High Variety (biometric, survey, ordinal), and Clinical Value."
)

notes2 = slide2.notes_slide.notes_text_frame
notes2.text = "Speaker Notes:\nExplain that testing every citizen with blood tests is logistically impossible. Big Data gives us the ability to use behavioral, demographic, and physical indicators to flag high-risk citizens before severe symptoms manifest."

# ==============================================================================
# SLIDE 3: Dataset Choice: CDC BRFSS vs Toy Pima Dataset
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
create_header(slide3, "Dataset Architecture: Why CDC BRFSS (253k+ Records)?")

table_shape = slide3.shapes.add_table(3, 4, Inches(0.8), Inches(1.7), Inches(11.7), Inches(2.2))
table = table_shape.table
table.columns[0].width = Inches(2.7)
table.columns[1].width = Inches(2.5)
table.columns[2].width = Inches(3.2)
table.columns[3].width = Inches(3.3)

headers = ["Evaluation Metric", "Pima Indians (Toy Dataset)", "CDC BRFSS Dataset (Our Project)", "Evaluation Impact"]
for idx, h in enumerate(headers):
    cell = table.cell(0, idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = WHITE

rows_data = [
    ["Data Volume", "768 rows (tiny sample)", "253,680 rows (22 MB big data)", "True Big Data scale vs toy project"],
    ["Demographic Scope", "Single female indigenous tribe", "National population-wide diversity", "High generalizability & clinical validity"]
]

for r_idx, row in enumerate(rows_data, start=1):
    for c_idx, val in enumerate(row):
        cell = table.cell(r_idx, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BOX_BG if r_idx % 2 == 1 else WHITE
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_GRAY

desc_box = slide3.shapes.add_textbox(Inches(0.8), Inches(4.1), Inches(11.7), Inches(1.4))
tf3_desc = desc_box.text_frame
tf3_desc.word_wrap = True
p = tf3_desc.paragraphs[0]
p.text = "Key Dataset Attributes (21 Features):"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = NAVY

p_sub = tf3_desc.add_paragraph()
p_sub.text = "• Clinical/Biometrics: BMI, High Blood Pressure (HighBP), High Cholesterol (HighChol), Stroke, Heart Disease.\n• Lifestyle & Demographics: Physical Activity, Smoking, Fruit/Veg Consumption, Alcohol, Age (1-13), Income, Education, General Health."
p_sub.font.size = Pt(12)
p_sub.font.color.rgb = DARK_GRAY

add_rationale_box(
    slide3,
    "Proves why we rejected the 768-row Pima Indians dataset that most college students use, avoiding instant rejection from BDA evaluators.",
    "Satisfies the core BDA course prerequisite: processing large-scale, heterogeneous, real-world data volume."
)

notes3 = slide3.notes_slide.notes_text_frame
notes3.text = "Speaker Notes:\nEmphasize strongly that 768 rows is NOT Big Data. Point out that our project uses a verified 253,680-row dataset across 21 multi-dimensional features, giving authentic enterprise scale."

# ==============================================================================
# SLIDE 4: End-to-End System Architecture
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
create_header(slide4, "End-to-End BDA System Pipeline Architecture")

# Draw 4 sequential architecture blocks
steps = [
    ("1. Data Ingestion & Quality", "• 253,680 records ingested\n• Zero-null validation\n• Schema verification (21 features)\n• Binary target definition"),
    ("2. Preprocessing & Partitioning", "• Stratified 80/20 train-test split\n• Cost-sensitive class weighting\n• StandardScaler normalization\n• Distributed vectorization"),
    ("3. Multi-Model Benchmark", "• Logistic Regression (Linear)\n• Random Forest (Bagging)\n• HistGradientBoosting (Boosting)\n• Parallel multi-core training"),
    ("4. Serving & Clinical UI", "• Pipeline serialization (.joblib)\n• Streamlit decision support UI\n• Real-time risk probability\n• Personalized factor triggers")
]

for idx, (title, details) in enumerate(steps):
    left = Inches(0.8 + idx * 2.95)
    top = Inches(1.7)
    width = Inches(2.8)
    height = Inches(3.7)
    
    box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = TEAL if idx == 2 else NAVY
    box.line.width = Pt(1.5)
    
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.15)
    
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = TEAL if idx == 2 else NAVY
    
    p_d = tf.add_paragraph()
    p_d.text = "\n" + details
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = DARK_GRAY

add_rationale_box(
    slide4,
    "Illustrates the complete operational flow from raw streaming data to clinical user interface.",
    "Mirrors enterprise Big Data pipelines (Ingestion -> ETL -> Distributed ML Training -> Serialized Inference)."
)

# ==============================================================================
# SLIDE 5: Healthcare Class Imbalance & Cost-Sensitive Learning
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
create_header(slide5, "Critical Healthcare Challenge: Severe Class Imbalance")

tb5 = slide5.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.9))
tf5 = tb5.text_frame
tf5.word_wrap = True

add_bullet(tf5, "1. The Skew in Population Data", "Healthy population: 218,334 (86.07%)  |  Diabetic/Prediabetic: 35,346 (13.93%). This severe 6:1 imbalance distorts standard machine learning algorithms.")
add_bullet(tf5, "2. The Accuracy Paradox", "A naive model that predicts 'Healthy' for 100% of patients achieves an impressive 86% accuracy, but detects ZERO sick patients (100% False Negative rate). In clinical medicine, this is disastrous.")
add_bullet(tf5, "3. Our BDA Solution: Cost-Sensitive Balanced Weighting", "We computed inverse class weights dynamically: w_j = N / (2 * N_j). This heavily penalizes the loss function when a diabetic patient is misclassified, forcing the models to achieve ~79.5% Sensitivity/Recall.")

add_rationale_box(
    slide5,
    "Explains the mathematical reason why accuracy is rejected in favor of ROC-AUC and Recall in clinical AI systems.",
    "Addressing heavy class skew is a hallmark requirement in Big Data predictive modeling."
)

# ==============================================================================
# SLIDE 6: Distributed Algorithmic Benchmarking
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
create_header(slide6, "Algorithmic Benchmarking: Why Three Models?")

cards = [
    ("Logistic Regression", "Baseline Linear Classifier", "• Evaluates log-odds linear relationships\n• Incredibly fast (0.27s on 200k rows)\n• Provides interpretable baseline odds ratios\n• ROC-AUC: 0.8196 | Recall: 76.11%"),
    ("Random Forest (100 Trees)", "Parallel Bagging Ensemble", "• 100 decorrelated decision trees\n• Mitigates overfitting via bootstrap aggregation\n• Computes non-linear feature importances\n• ROC-AUC: 0.8227 | Recall: 73.99%"),
    ("HistGradientBoosting", "Optimal Scalable Boosting", "• Bins continuous values into 256 discrete bins\n• Reduces split complexity from O(N log N) to O(K*N)\n• Lightning-fast (< 5s for 200k rows)\n• ROC-AUC: 0.8268 | Recall: 79.46% (WINNER)")
]

for idx, (m_name, subtitle, desc) in enumerate(cards):
    left = Inches(0.8 + idx * 3.95)
    top = Inches(1.7)
    width = Inches(3.8)
    height = Inches(3.7)
    
    box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = TEAL if idx == 2 else NAVY
    box.line.width = Pt(2.0 if idx == 2 else 1.0)
    
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.15)
    
    p_t = tf.paragraphs[0]
    p_t.text = m_name
    p_t.font.size = Pt(14)
    p_t.font.bold = True
    p_t.font.color.rgb = TEAL if idx == 2 else NAVY
    
    p_s = tf.add_paragraph()
    p_s.text = subtitle
    p_s.font.size = Pt(11)
    p_s.font.italic = True
    p_s.font.color.rgb = DARK_GRAY
    
    p_d = tf.add_paragraph()
    p_d.text = "\n" + desc
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = DARK_GRAY

add_rationale_box(
    slide6,
    "Rigorous comparative study rather than picking an arbitrary algorithm without empirical justification.",
    "Compares algorithmic complexity (linear vs bagging vs histogram-boosting) over large tabular datasets."
)

# ==============================================================================
# SLIDE 7: Experimental Performance & Results
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
create_header(slide7, "Experimental Results & Model Evaluation")

# Embed ROC plot and Confusion Matrix
roc_img = os.path.join(REPORTS_DIR, "roc_curve.png")
cm_img = os.path.join(REPORTS_DIR, "confusion_matrix.png")

if os.path.exists(roc_img):
    slide7.shapes.add_picture(roc_img, Inches(0.8), Inches(1.6), Inches(4.5), Inches(3.8))
if os.path.exists(cm_img):
    slide7.shapes.add_picture(cm_img, Inches(5.6), Inches(1.6), Inches(3.8), Inches(3.8))

res_box = slide7.shapes.add_textbox(Inches(9.6), Inches(1.6), Inches(2.9), Inches(3.8))
tf7 = res_box.text_frame
tf7.word_wrap = True
tf7.margin_left = tf7.margin_right = tf7.margin_top = 0

p = tf7.paragraphs[0]
p.text = "Benchmark Summary:"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = NAVY

bullets = [
    "Evaluated on 50,736 test records.",
    "Best Model: HistGradientBoosting.",
    "ROC-AUC: 0.8268 (Superb class separation).",
    "Recall / Sensitivity: 79.46% (Captures 4 out of 5 diabetic patients early).",
    "Training latency: Under 5 seconds on 200,000+ training instances."
]
for b in bullets:
    p_b = tf7.add_paragraph()
    p_b.text = "• " + b
    p_b.font.size = Pt(11)
    p_b.font.color.rgb = DARK_GRAY

add_rationale_box(
    slide7,
    "Provides visual empirical validation (ROC Curves & Confusion Matrix) demonstrating high diagnostic power.",
    "Uses distributed evaluation metrics (ROC-AUC, Precision, Recall) standard in Big Data benchmarking."
)

# ==============================================================================
# SLIDE 8: Explainable AI (XAI) & Feature Importance
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
create_header(slide8, "Explainable AI (XAI): Clinical Feature Importance")

fi_img = os.path.join(REPORTS_DIR, "feature_importance.png")
if os.path.exists(fi_img):
    slide8.shapes.add_picture(fi_img, Inches(0.8), Inches(1.6), Inches(5.5), Inches(3.9))

xai_box = slide8.shapes.add_textbox(Inches(6.6), Inches(1.6), Inches(5.9), Inches(3.9))
tf8 = xai_box.text_frame
tf8.word_wrap = True

add_bullet(tf8, "1. Eliminating the 'Black Box'", "Clinicians will never adopt an opaque prediction. Feature importance ranking reveals exactly why a patient is identified as high risk.")
add_bullet(tf8, "2. Top 5 Clinical Risk Drivers", "1. General Health (GenHlth): Strongest correlation with chronic disease.\n2. Body Mass Index (BMI): Exponential surge in insulin resistance.\n3. High Blood Pressure (HighBP): Vascular comorbidity.\n4. Age Bracket: Beta-cell decline in older demographics.\n5. High Cholesterol: Metabolic syndrome lipid profiles.")

add_rationale_box(
    slide8,
    "Demonstrates that the system is clinically sound and medically interpretable, not just a black-box formula.",
    "Dimensionality analysis and feature importance extraction are core Big Data Analytics competencies."
)

# ==============================================================================
# SLIDE 9: Interactive Clinical Decision Support App
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
create_header(slide9, "Interactive Clinical Decision Support Dashboard (Streamlit)")

app_box = slide9.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.9))
tf9 = app_box.text_frame
tf9.word_wrap = True

add_bullet(tf9, "1. Real-Time Patient Risk Calculator", "Physicians or triage nurses enter patient vitals (BMI, blood pressure, age, cholesterol, lifestyle factors) via sliders and toggles to receive an instant probability score.")
add_bullet(tf9, "2. Color-Coded Risk Triage Tiers", "• Green (< 35%): Low risk - routine periodic checkup.\n• Amber (35% - 60%): Moderate risk - lifestyle & diet intervention.\n• Red (> 60%): High risk - urgent lab confirmation (HbA1c test).")
add_bullet(tf9, "3. Personalized Trigger Explanations", "Dynamically highlights the specific biometric drivers (e.g. 'Obesity + Hypertension + Advancing Age') that elevated the patient's individual score.")

add_rationale_box(
    slide9,
    "Proves the machine learning model is translated into an actionable real-world software product.",
    "Demonstrates end-user consumption of Big Data models via low-latency interactive dashboards."
)

# ==============================================================================
# SLIDE 10: Conclusion & Future Scope
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
create_header(slide10, "Conclusion & Future Scope")

tb10 = slide10.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.9))
tf10 = tb10.text_frame
tf10.word_wrap = True

add_bullet(tf10, "Summary of Achievements", "• Built a complete BDA healthcare pipeline on 253,680 real CDC records.\n• Achieved 0.827 ROC-AUC and 79.5% Recall using Histogram Gradient Boosting.\n• Delivered transparent Explainable AI risk factors and an interactive Streamlit UI.")
add_bullet(tf10, "Future Big Data Enhancements", "• Streaming Ingestion: Ingest real-time vitals using Apache Kafka and Spark Structured Streaming.\n• Deep Learning at Scale: Deploy PySpark MLlib or distributed neural networks for multi-morbidity prediction.\n• EHR Integration: Interoperate with HL7 / FHIR electronic hospital records.")

add_rationale_box(
    slide10,
    "Provides a strong concluding summary showing clear business/healthcare impact and an architectural roadmap.",
    "Shows examiners a deep understanding of future enterprise distributed streaming technologies."
)

prs.save(OUTPUT_PPTX)
print(f"[SUCCESS] PowerPoint presentation saved successfully to: {OUTPUT_PPTX}")
