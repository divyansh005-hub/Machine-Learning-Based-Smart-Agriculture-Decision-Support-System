# AgriSmart — Smart Agriculture Decision Support System

An end-to-end, reproducible academic Machine Learning Decision Support System (DSS) integrating three predictive agronomic modules:
1. **Module A — Crop Recommendation** (Multiclass Botanical Classification)
2. **Module B — Fertilizer Recommendation** (Multiclass Nutrient Formulation Classification with Imbalance Handling)
3. **Module C — Crop Yield Prediction** (Continuous Non-Linear Regression with Temporal Forecasting)

---

## 1. Project Overview & Architecture

AgriSmart provides smallholders, commercial farm operators, agricultural extension specialists, and researchers with empirical data-driven insights. Rather than relying on static rules or intuition, the system evaluates real-world soil chemistry, meteorological conditions, and historical yield patterns to generate validated recommendations.

```
Smart Agriculture/
├── dataset/                                # Source datasets (UNTOUCHED & PRESERVED)
│   ├── Crop recommendation/                # 2,200 rows, 8 features, 22 balanced crops
│   │   ├── Crop Reccomendation Dataset 2.csv
│   │   ├── Crop_recommendation 2.csv
│   │   └── Crop_recommendation.csv
│   ├── Fertilizer Recommendation/          # 10,000 rows, 20 features, 7 fertilizer classes
│   │   └── fertilizer_recommendation.csv
│   └── Yield predicition/                  # FAO global agricultural production dataset
│       ├── crop_yield.csv                  # Alternate regional dataset (documented)
│       ├── yield_df.csv                    # Canonical FAO merged dataset (28,242 rows)
│       ├── yield.csv, rainfall.csv, temp.csv, pesticides.csv
├── models/                                 # Serialized scikit-learn pipelines & JSON metadata
│   ├── crop_recommendation.joblib
│   ├── crop_recommendation_meta.json
│   ├── fertilizer_recommendation.joblib
│   ├── fertilizer_recommendation_meta.json
│   ├── yield_prediction.joblib
│   └── yield_prediction_meta.json
├── reports/                                # Empirical benchmarks and evaluation tracking
│   ├── model_comparison.csv
│   └── MODEL_EVALUATION.md
├── src/                                    # Modular Python source package
│   ├── data/
│   │   ├── __init__.py
│   │   └── loaders.py                      # Data loaders with strict schema validation
│   ├── features/
│   │   ├── __init__.py
│   │   └── preprocessing.py                # Preprocessing pipelines & ColumnTransformers
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py                        # Reproducible end-to-end training pipeline
│   │   └── predict.py                      # Inference engine with safety checks & validation
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── metrics.py                      # Classification & regression evaluation routines
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── styles.py                       # Modern styling & theme tokens
│   │   ├── home_page.py                    # Home Dashboard
│   │   ├── crop_page.py                    # Crop Recommendation UI
│   │   ├── fertilizer_page.py              # Fertilizer Recommendation UI
│   │   ├── yield_page.py                   # Crop Yield Prediction UI
│   │   ├── performance_page.py             # Empirical Model Performance UI
│   │   ├── insights_page.py                # Exploratory Data Insights & Audit UI
│   │   └── about_page.py                   # Documentation & Limitations UI
│   └── utils/
│       ├── __init__.py
│       └── constants.py                    # Configuration, feature lists, ranges, disclaimers
├── tests/                                  # Automated pytest test suite (22 tests)
│   ├── test_data_loaders.py
│   ├── test_preprocessing.py
│   ├── test_inference.py
│   ├── test_smoke.py
│   └── test_app_smoke.py
├── app.py                                  # Streamlit web application entry point
├── requirements.txt                        # Python dependencies
├── DATA_AUDIT.md                           # Comprehensive dataset audit findings
└── README.md                               # Project documentation
```

---

## 2. Dataset Inventory & Audit Findings

All datasets located in `dataset/` were audited and preserved without modification. Full audit documentation is available in [`DATA_AUDIT.md`](file:///d:/NIIT_University/Projects/Smart%20Agricultutre/DATA_AUDIT.md).

| Module | Dataset File | Rows | Features | Target | Split Strategy | Notes |
|---|---|---|---|---|---|---|
| **Module A (Crop)** | `Crop_recommendation.csv` | 2,200 | 7 numeric | `label` (22 crops) | Stratified 80:20 (`random_state=42`) | Exactly 100 samples per class. Verified 3 identical files by MD5. |
| **Module B (Fertilizer)** | `fertilizer_recommendation.csv` | 10,000 | 12 numeric, 7 categorical | `Recommended_Fertilizer` (7 classes) | Stratified 80:20 (`random_state=42`) | Severe class imbalance (SSP: 1.8%). Handled via balanced class weights. |
| **Module C (Yield)** | `yield_df.csv` | 25,932 (deduped) | 4 numeric, 2 categorical | `hg/ha_yield` (hectograms/ha) | Chronological (Train ≤ 2009, Test ≥ 2010) | Exact duplicates purged. Multi-station weather entries in `temp.csv` investigated. |

---

## 3. Empirical Model Benchmarks

Evaluation is conducted strictly on held-out test sets. Full results are recorded in [`reports/MODEL_EVALUATION.md`](file:///d:/NIIT_University/Projects/Smart%20Agricultutre/reports/MODEL_EVALUATION.md) and [`reports/model_comparison.csv`](file:///d:/NIIT_University/Projects/Smart%20Agricultutre/reports/model_comparison.csv).

### Summary Table

| Module | Model Candidate | Primary Metric | Secondary Metric | Selection Status | Selection Rationale |
|---|---|---|---|---|---|
| **Crop Recommendation** | DummyClassifier (Baseline) | Macro-F1: 0.0040 | Accuracy: 0.0455 | Baseline | Zero-information baseline |
| | Logistic Regression | Macro-F1: 0.9725 | Accuracy: 0.9727 | Candidate | Strong linear baseline |
| | **Random Forest** | **Macro-F1: 0.9955** | **Accuracy: 0.9955** | **★ SELECTED** | Superior separation across all 22 crop classes |
| **Fertilizer Recommendation** | DummyClassifier (Baseline) | Macro-F1: 0.0676 | Accuracy: 0.3100 | Baseline | Zero-information baseline |
| | Logistic Regression (Balanced) | Macro-F1: 0.6697 | Accuracy: 0.7810 | Candidate | Linear decision boundaries |
| | **Random Forest (Balanced)** | **Macro-F1: 0.7131** | **Accuracy: 0.8705** | **★ SELECTED** | Highest Macro-F1; preserves rare class recall (SSP) |
| **Crop Yield Prediction** | Mean Baseline (DummyRegressor) | RMSE: 96,284 hg/ha | MAE: 68,797 hg/ha | Baseline | Historical train mean baseline ($R^2 = -0.02$) |
| | Linear Regression | RMSE: 50,470 hg/ha | MAE: 33,809 hg/ha | Candidate | Linear baseline ($R^2 = 0.7192$) |
| | **Random Forest Regressor** | **RMSE: 20,302 hg/ha** | **MAE: 10,454 hg/ha** | **★ SELECTED** | Substantial error reduction ($R^2 = 0.9546$, 2.03 t/ha RMSE) |

---

## 4. Installation & Environment Setup

### Prerequisites
- Python 3.11 or Python 3.12 installed on your system.
- Standard terminal (PowerShell, Command Prompt, or Bash).

### Step 1: Install Dependencies
Open a terminal in the project directory (`Smart Agriculture/`):
```bash
python -m pip install -r requirements.txt
```

---

## 5. How to Train the Models

To execute the reproducible training pipeline, fit candidate models, compute baseline comparisons, serialize pipelines into `models/`, and regenerate benchmark reports:

```bash
python src/models/train.py
```
*(Or via module syntax)*:
```bash
python -m src.models.train
```

All models will be evaluated and exported without modifying any raw datasets in `dataset/`.

---

## 6. How to Run the Automated Test Suite

AgriSmart includes a comprehensive test suite (22 unit, validation, and smoke tests) covering dataset integrity, preprocessors, inference boundary conditions, unseen categories, and artifact availability:

```bash
python -m pytest tests/ -v
```

All tests execute and pass in approximately 3 to 8 seconds.

---

## 7. How to Launch the Web Application

Launch the Streamlit dashboard using:

```bash
python -m streamlit run app.py
```

Streamlit will print the local URL:
```
Local URL: http://localhost:8501
```
Open your browser and navigate to `http://localhost:8501`.

---

## 8. Navigating the Dashboard

1. **🏠 Home Dashboard:** Project architecture, verified dataset inventory, and live model health status.
2. **🌾 Crop Recommendation:** Interactive sliders and inputs for N-P-K, pH, temperature, humidity, and rainfall; returns predicted crop, top-3 candidates with confidence probabilities, and physiological descriptions.
3. **🧪 Fertilizer Recommendation:** Organizes soil chemical properties, crop developmental stage, and field history; returns recommended fertilizer formulation, deficiency explanations, and probability distributions.
4. **📈 Crop Yield Prediction:** Predicts crop yields across 101 countries and 10 crops; outputs yields in verified native units (`hg/ha`) and converted metric units (`tonnes/ha`).
5. **📊 Model Performance:** Displays empirical comparison matrices, confusion matrices, classification reports, and regression error analyses loaded dynamically from real evaluation artifacts.
6. **🔍 Dataset Insights:** Interactive data exploration featuring class distributions, correlation heatmaps, feature distributions, and detailed audit risk warnings.
7. **ℹ️ About & Limitations:** Complete methodology documentation, academic references, data provenance, and ethical guidelines.

---

## 9. Important Limitations & Responsible Use

1. **Decision Support Only:** Model outputs are predictive statistical approximations derived from historical benchmark datasets. They are meant to assist agricultural professionals and do not supersede certified laboratory soil health tests, local agronomist consultation, or agricultural extension directives.
2. **Regional Granularity:** Yield predictions are calibrated on FAO national aggregate indicators; farm-specific microclimates, pest outbreaks, and parcel management practices introduce natural variation.
3. **Synthetic Nutrient Boundaries:** Fertilizer recommendation targets reflect algorithmic simulation boundaries and must be treated as guidance rather than clinical prescription.
