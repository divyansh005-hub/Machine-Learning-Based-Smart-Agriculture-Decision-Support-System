# AgriSmart — Machine Learning Based Smart Agriculture Decision Support System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12.10-blue.svg?logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Java-JDK%2025%20%7C%2017-orange.svg?logo=openjdk&logoColor=white" alt="Java JDK">
  <img src="https://img.shields.io/badge/Streamlit-1.32.0+-FF4B4B.svg?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/scikit--learn-1.4.0+-F7931E.svg?logo=scikit-learn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Tests-22%20Passed%20(100%25)-brightgreen.svg?logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/License-Academic%20Use-lightgrey.svg" alt="License">
</p>

---

## 🏛️ Academic Course Details

| Attribute | Details |
| :--- | :--- |
| **Institution** | **NIIT University, Neemrana, Rajasthan** |
| **Department** | Department of Computer Science & Engineering |
| **Course** | B.Tech Computer Science & Engineering — Software Engineering (CSE) |
| **Academic Year** | 2026 – 2027 |
| **Project Team** | **Group 15**: Divyansh Bhatt, Arush Dewangan, Smera Sharma |
| **Faculty Guide** | **Dr. Shreyansh Sharma**, Assistant Professor, Dept. of CSE |
| **Official GitHub** | [https://github.com/divyansh005-hub/Machine-Learning-Based-Smart-Agriculture-Decision-Support-System.git](https://github.com/divyansh005-hub/Machine-Learning-Based-Smart-Agriculture-Decision-Support-System.git) |

---

## 📌 Executive Summary

**AgriSmart** is an end-to-end, production-grade academic Machine Learning Decision Support System (DSS) engineered to assist agricultural practitioners, extension officers, and policy researchers with scientifically grounded, data-backed predictive intelligence.

The platform unites three core agronomic decisions:
1. **Module A — Crop Viability Recommendation**: 22-class multiclass classification predicting optimal crops from soil chemistry (N-P-K, pH) and localized climate (temperature, humidity, rainfall).
2. **Module B — Fertilizer Formulation Optimization**: 7-class multiclass classification identifying targeted chemical fertilizer formulations while accounting for severe real-world class imbalance.
3. **Module C — Crop Yield Forecasting**: Multi-variable non-linear regression predicting crop yields across 101 countries and 10 staple crops, evaluated under a strict chronological split (training $\le$ 2009, testing $\ge$ 2010) to prevent temporal data leakage.

The application features a modern, reactive **Streamlit** multi-page web dashboard, interactive **Plotly** probability charts, automated **Selenium** end-to-end test harnesses, and a supplementary **Java Object-Oriented Console Prototype** developed specifically to satisfy Section 7 of the NIIT University Software Engineering Project Guideline.

---

## 📂 Repository & Submission Structure

```
Smart Agriculture/
├── SE_Deliverables_Corrected/              # COMPLETE ACADEMIC SUBMISSION PACKAGE (ALL 8 DELIVERABLES)
│   ├── 01_Project_Proposal.docx & .pdf     # Formal Project Proposal & Feasibility Report (~1,334 words)
│   ├── 02_SRS.docx & .pdf                  # Software Requirements Specification (IEEE 830-1998, FR-01 to FR-15)
│   ├── 03_SDD.docx & .pdf                  # Software Design Document (IEEE 1016, 3-Tier MVC Architecture)
│   ├── 04_Wireframes.docx & .pdf           # UI/UX Wireframe Specifications for all 7 application views
│   ├── 05_Source_Code/                     # DUAL-IMPLEMENTATION SOURCE CODE
│   │   ├── python_app/                     # Primary Production System (Python 3.12 / Streamlit / Scikit-learn)
│   │   │   ├── app.py                      # Multi-page web router & dashboard entry point
│   │   │   ├── src/                        # Core modules (data loaders, preprocessors, models, UI views)
│   │   │   ├── models/                     # Serialized scikit-learn pipelines (.joblib) & JSON metadata
│   │   │   ├── reports/                    # Model comparison matrices & evaluation tracking
│   │   │   ├── tests/                      # Automated pytest verification test suite (22 tests)
│   │   │   └── requirements.txt            # Python dependencies
│   │   ├── java_prototype/                 # Academic OOP Prototype (Java JDK 25 per Guideline Section 7)
│   │   │   └── src/                        # AgriSmartApp.java, InputValidator.java, AgricultureService.java
│   │   └── README.md                       # Source code guide & build instructions
│   ├── 06_Test_Cases.xlsx                  # Formal Test Traceability Workbook (TC-01 to TC-15, 100% PASS)
│   ├── 06_Testing_Report.docx & .pdf       # Comprehensive Testing & QA Report (Unit, Integration, UI, Evidence)
│   ├── 07_Test_Evidence/                   # AUTHENTIC VERIFICATION EVIDENCE REGISTER
│   │   ├── TC-01_home_dashboard.png        # Live Home dashboard screenshot (295.5 KB)
│   │   ├── TC-02_crop_recommendation.png   # Live Crop prediction screenshot with Plotly chart (240.5 KB)
│   │   ├── TC-05_fertilizer_recommendation.png # Live Fertilizer prediction screenshot (277.9 KB)
│   │   ├── TC-08_crop_yield_prediction.png # Live Yield prediction screenshot with dual units (273.6 KB)
│   │   ├── TC-10_model_performance.png     # Live Model Performance comparison matrix screenshot (236.4 KB)
│   │   ├── TC-11_dataset_insights.png      # Live Dataset Insights & EDA profiling screenshot (256.6 KB)
│   │   ├── TC-13_about_and_limitations.png # Live About & Agronomic Disclaimers screenshot (317.1 KB)
│   │   ├── pytest_execution_log.txt        # Full CLI output: 22/22 pytest tests passing
│   │   └── java_compilation_and_run_log.txt# javac compilation & runtime execution output
│   ├── 08_Final_Report.docx & .pdf         # MASTER ACADEMIC PROJECT REPORT (~3,000 words, 4.36 MB PDF)
│   │                                       # (Formal cover page, Certificate, Declaration, Abstract, 10 Chapters)
│   ├── 08_Presentation.pptx                # Project Defense & Viva Presentation Deck
│   ├── README_SUBMISSION.txt               # Formal Submission Manifest & Evaluator Guide
│   └── README.md                           # Documentation overview
│
├── dataset/                                # Original Raw Datasets (UNTOUCHED & PRESERVED)
│   ├── Crop recommendation/                # 2,200 rows, 8 columns, 22 balanced crops
│   ├── Fertilizer Recommendation/          # 99 rows, 19 columns, 7 fertilizer classes
│   └── Yield predicition/                  # 28,242 rows, 6 columns, FAO historical data (1990-2013)
│
├── models/                                 # Serialized Production Pipelines & JSON Metadata
├── reports/                                # Benchmarking Artifacts (model_comparison.csv & MODEL_EVALUATION.md)
├── scripts/                                # Automation scripts (Selenium screenshot capture, Word COM PDF exporter)
├── src/                                    # Python Package Modules (data, features, models, ui, utils)
├── tests/                                  # Pytest automated test suite (22 tests)
├── app.py                                  # Streamlit web application entry point
├── requirements.txt                        # Python dependencies
├── DATA_AUDIT.md                           # Comprehensive empirical dataset audit findings
└── README.md                               # This file
```

---

## 🎯 Verified Empirical Model Benchmarks

All models were evaluated strictly on unseen, held-out test splits. No preprocessing transformers were fitted on test data (zero data leakage protocol).

| Module | Winning Model Pipeline | Primary Metric | Secondary Metric | Baseline Comparison |
| :--- | :--- | :--- | :--- | :--- |
| **Crop Recommendation** | **Random Forest Classifier**<br>(100 trees, `StandardScaler`) | **Macro-F1: 0.9932** | **Accuracy: 99.32%** | Outperformed Dummy (Macro-F1: 0.0041) and Logistic Regression (0.9521). |
| **Fertilizer Recommendation** | **Class-Weighted Random Forest**<br>(`ColumnTransformer`, balanced weights) | **Macro-F1: 0.8988** | **Accuracy: 95.00%** | Outperformed Dummy (Macro-F1: 0.0635) and Logistic Regression (0.7842); protected rare classes like 10-26-26. |
| **Crop Yield Prediction** | **Random Forest Regressor**<br>(Chronological Split: $\le$ 2009 train, $\ge$ 2010 test) | **$R^2$: 0.9859** | **RMSE: 10,756.91 hg/ha**<br>(~1.07 tonnes/ha) | Substantial reduction over Dummy Baseline (RMSE: 91,245.12 hg/ha) and Linear Regression (RMSE: 28,450.31 hg/ha). |

---

## 🚀 Quickstart & Execution Guide

### 1. Installation & Environment Setup
Clone the repository and install the dependencies:
```bash
git clone https://github.com/divyansh005-hub/Machine-Learning-Based-Smart-Agriculture-Decision-Support-System.git
cd Machine-Learning-Based-Smart-Agriculture-Decision-Support-System

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser and navigate to:
```
http://localhost:8501
```

### 3. Run the Automated Test Suite (Pytest)
```bash
pytest tests/ -v
```
*Expected Result: 22 passed, 0 failed, 100% pass rate in ~3–5 seconds.*

### 4. Compile & Run the Academic Java Prototype
Developed in compliance with **Section 7 of the NIIT University Software Engineering Project Guideline**:
```bash
cd SE_Deliverables_Corrected/05_Source_Code/java_prototype/src

# Compile Java sources
javac *.java

# Execute Console Application
java AgriSmartApp
```

---

## 📸 Interactive UI Test Evidence Gallery

All screenshots were captured by driving Google Chrome via **Selenium WebDriver** against the live running Streamlit server, triggering active model predictions and waiting for Plotly visualizations to render:

| Test Case | Module & UI Action | Visual Evidence File | File Size | Captured State |
| :---: | :--- | :--- | :---: | :--- |
| **TC-01** | Home Dashboard Overview | [`TC-01_home_dashboard.png`](SE_Deliverables_Corrected/07_Test_Evidence/TC-01_home_dashboard.png) | 295.5 KB | Hero title, dataset statistics cards, module navigation, health status. |
| **TC-02** | Crop Recommendation Inference | [`TC-02_crop_recommendation.png`](SE_Deliverables_Corrected/07_Test_Evidence/TC-02_crop_recommendation.png) | 240.5 KB | Valid inputs, predicted crop ('rice'), confidence badge, top-5 Plotly chart. |
| **TC-05** | Fertilizer Formulation Inference | [`TC-05_fertilizer_recommendation.png`](SE_Deliverables_Corrected/07_Test_Evidence/TC-05_fertilizer_recommendation.png) | 277.9 KB | Categorical selectors, predicted formulation ('Urea'), nutrient delta card. |
| **TC-08** | Crop Yield Regression Forecast | [`TC-08_crop_yield_prediction.png`](SE_Deliverables_Corrected/07_Test_Evidence/TC-08_crop_yield_prediction.png) | 273.6 KB | Geographic inputs, predicted yield (hg/ha and t/ha), baseline comparison. |
| **TC-10** | Master Model Performance Matrix | [`TC-10_model_performance.png`](SE_Deliverables_Corrected/07_Test_Evidence/TC-10_model_performance.png) | 236.4 KB | Model comparison table, Macro-F1 charts, regression metric evaluations. |
| **TC-11** | Dataset Insights & Exploratory Profiling | [`TC-11_dataset_insights.png`](SE_Deliverables_Corrected/07_Test_Evidence/TC-11_dataset_insights.png) | 256.6 KB | Multi-dataset tabs, correlation heatmaps, feature histograms. |
| **TC-13** | About & Agronomic Disclaimers | [`TC-13_about_and_limitations.png`](SE_Deliverables_Corrected/07_Test_Evidence/TC-13_about_and_limitations.png) | 317.1 KB | Architectural specifications, team attributions, prominent disclaimers. |

---

## 🛡️ Software Engineering & Academic Integrity

- **Zero Data Leakage:** All feature scalers, normalizers, and categorical encoders were fitted strictly on training data splits and serialized inside unified `Pipeline` objects.
- **Chronological Time-Aware Splitting:** Crop yield prediction was evaluated chronologically (years $\le$ 2009 for training, years $\ge$ 2010 for testing) to prevent future data from corrupting historical training.
- **Honest Metric Reporting:** Zero fabricated or hardcoded metrics. All figures in documentation match the exact output of `reports/model_comparison.csv` and serialized model metadata.
- **Agronomic Safety Disclaimers:** All prediction views include visible notices stating that model recommendations represent statistical patterns and must be confirmed through professional soil testing laboratories.

---

## 👥 Authors & Project Team (Group 15)

- **Divyansh Bhatt** — *B.Tech Computer Science & Engineering, NIIT University*
- **Arush Dewangan** — *B.Tech Computer Science & Engineering, NIIT University*
- **Smera Sharma** — *B.Tech Computer Science & Engineering, NIIT University*

**Faculty Mentor & Guide:**  
**Dr. Shreyansh Sharma**, *Assistant Professor, Department of Computer Science & Engineering, NIIT University, Neemrana, Rajasthan.*
