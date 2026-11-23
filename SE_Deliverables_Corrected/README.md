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

## 📂 Deliverables Inventory (`SE_Deliverables_Corrected/`)

| Deliverable | DOCX Document | High-Resolution PDF | Description |
| :--- | :--- | :--- | :--- |
| **01 Project Proposal** | [`01_Project_Proposal.docx`](01_Project_Proposal.docx) | [`01_Project_Proposal.pdf`](01_Project_Proposal.pdf) | Project motivation, feasibility, stakeholder analysis, Gantt timeline. |
| **02 SRS Specification** | [`02_SRS.docx`](02_SRS.docx) | [`02_SRS.pdf`](02_SRS.pdf) | Formal IEEE 830-1998 standard: FR-01 to FR-15, NFR-01 to NFR-06, Use Cases. |
| **03 SDD Design** | [`03_SDD.docx`](03_SDD.docx) | [`03_SDD.pdf`](03_SDD.pdf) | IEEE 1016 standard: 3-tier architecture, ML pipelines, UML class design, RTM. |
| **04 Wireframes** | [`04_Wireframes.docx`](04_Wireframes.docx) | [`04_Wireframes.pdf`](04_Wireframes.pdf) | UI/UX design tokens, global layout, wireframe cards for all 7 application views. |
| **05 Source Code** | [`05_Source_Code/`](05_Source_Code/) | *(Codebase)* | Full Python production app (`python_app/`) + Java OOP model (`java_prototype/`). |
| **06 Test Workbook** | [`06_Test_Cases.xlsx`](06_Test_Cases.xlsx) | *(Excel)* | Formal test traceability workbook covering TC-01 to TC-15 (100% PASS). |
| **06 Testing Report** | [`06_Testing_Report.docx`](06_Testing_Report.docx) | [`06_Testing_Report.pdf`](06_Testing_Report.pdf) | QA strategy, 15 manual test matrices, 22 automated Pytest test breakdown. |
| **07 Test Evidence** | [`07_Test_Evidence/`](07_Test_Evidence/) | *(Evidence)* | 7 authentic full-resolution live Selenium UI prediction screenshots + execution logs. |
| **08 Master Final Report** | [`08_Final_Report.docx`](08_Final_Report.docx) | [`08_Final_Report.pdf`](08_Final_Report.pdf) | **Definitive project report**: Cover page, Certificate, Declaration, Abstract, 10 Chapters. |
| **08 Presentation** | [`08_Presentation.pptx`](08_Presentation.pptx) | *(PowerPoint)* | Slide deck for project defense and viva examination. |
| **Submission Manifest** | [`README_SUBMISSION.txt`](README_SUBMISSION.txt) | *(Text Manifest)* | Evaluator guide, academic integrity statement, and run instructions. |

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
cd 05_Source_Code/java_prototype/src

# Compile Java sources
javac *.java

# Execute Console Application
java AgriSmartApp
```

---

## 👥 Authors & Project Team (Group 15)

- **Divyansh Bhatt** — *B.Tech Computer Science & Engineering, NIIT University*
- **Arush Dewangan** — *B.Tech Computer Science & Engineering, NIIT University*
- **Smera Sharma** — *B.Tech Computer Science & Engineering, NIIT University*

**Faculty Mentor & Guide:**  
**Dr. Shreyansh Sharma**, *Assistant Professor, Department of Computer Science & Engineering, NIIT University, Neemrana, Rajasthan.*
