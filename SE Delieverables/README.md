# AgriSmart — Software Engineering Project Deliverables

**Institution:** NIIT University  
**Course:** Software Engineering (Academic Year 2026–2027)  
**Project Title:** Machine Learning Based Smart Agriculture Decision Support System (AgriSmart)  
**Group Number:** 15  
**Faculty Guide:** Dr. Shreyansh Sharma  

---

## 1. Project Team Members

| Name | Enrollment Number | Role |
|---|---|---|
| **Divyansh Bhatt** | BT24GC119 | Team Lead / ML Engineering & Full-Stack Architecture |
| **Arush Dewangan** | BT24GCS447 | Software Design, Testing & Quality Assurance |
| **Smera Sharma** | BT24GCS001 | Requirements Engineering & User Interface Design |

---

## 2. Deliverables Inventory (Aligned with SE Project Guideline v1.0)

This deliverable folder strictly follows the structure specified in **Section 12 (Final Submission Structure)** and **Section 2 (Expected Project Deliverables)** of the *Software Engineering Project Documentation & Implementation Guideline*:

| Deliverable Name | File Format(s) | Description | Guideline Section |
|---|---|---|---|
| **01_Project_Proposal** | `.pdf`, `.docx` | Problem definition, stakeholders, scope, exclusions, and technology stack (2 pages). | Section 2 |
| **02_SRS** | `.pdf`, `.docx` | Software Requirements Specification covering Functional Requirements (FR-01 to FR-13), NFRs, interfaces, and Use Cases (UC-01 to UC-03) (3 pages). | Section 4 |
| **03_SDD** | `.pdf`, `.docx` | Software Design Document detailing layered modular architecture, component responsibilities, data models, and traceability matrix (2 pages). | Section 5 |
| **04_Wireframes** | `.pdf`, `.docx` | Structural UI wireframes for Home Dashboard, three ML prediction modules, Model Performance, Dataset Insights, and About/Disclaimers. | Section 6 |
| **05_Source_Code** | Folder (`src/`, `README.md`) | Java OOP academic prototype demonstrating OOP principles (separation of concerns, validator, service, interactive console menu) without external dependencies. | Section 7 |
| **06_Test_Cases** | `.xlsx` | Executed test matrix covering 16 test cases (positive, negative, boundary, Java prototype, and artifact safety) with 100% PASS status. | Section 8 |
| **06_Testing_Report** | `.pdf`, `.docx` | Quality assurance report detailing test plan, scope, environment, requirements traceability, and execution integrity. | Section 8 |
| **07_Test_Evidence** | Folder (26 files) | Complete evidence register with authentic terminal execution logs (`.log`), visual UI screenshots (`.png`), and Pytest automated test results (`TC_pytest_suite_results.log`). | Section 9 |
| **08_Presentation** | `.pptx` | Presentation slide deck detailing project problem, ML methodology, architecture, and demonstration walkthrough. | Section 12 |
| **08_Final_Report** | `.pdf`, `.docx` | Comprehensive consolidation combining problem definition, requirements, design, dataset audits, held-out ML evaluations, and limitations. | Section 2 |
| **README.md** | Markdown | Top-level submission guide, reproduction commands, and directory index. | Section 12 |

---

## 3. Technology Stack & Dual Implementation Architecture

### 3.1 Primary Production Application (Python + Streamlit + scikit-learn)
The full operational application is located in the root workspace repository:
- **Presentation Layer:** Streamlit multi-page interactive web application (`app.py`, `src/ui/*`) with responsive Plotly charts and custom agronomic styling.
- **Machine Learning Core:** Three scikit-learn pipelines with column transformers, standard scalers, and one-hot encoders:
  - **Module A (Crop Recommendation):** Random Forest Classifier (Macro-F1: 0.9955, Accuracy: 0.9955).
  - **Module B (Fertilizer Recommendation):** Balanced Random Forest Classifier with cost-sensitive class weights (Macro-F1: 0.7131, Accuracy: 0.8705).
  - **Module C (Crop Yield Prediction):** Random Forest Regressor calibrated on historical FAO data (RMSE: 20,302.37 hg/ha = 2.03 t/ha, $R^2$: 0.9546).
- **Inference Engine:** `src/models/predict.py` with strict input boundary validation, probability rankings, and dual-unit conversions.

### 3.2 Academic Java OOP Prototype (`05_Source_Code`)
As recommended in **Section 7 of the SE Guideline**, a clean Java OOP console prototype is provided to demonstrate software engineering object-oriented principles:
- **Separation of Concerns:**
  - `AgriSmartApp.java`: Presentation layer managing menu interaction and user prompts.
  - `InputValidator.java`: Dedicated input validation utility enforcing numeric bounds and handling `NumberFormatException`.
  - `AgricultureService.java`: Business service encapsulating demonstration rules for crop suitability, fertilizer deficiencies, and yield estimations.
- **Compilation & Execution:**
  ```bash
  cd 05_Source_Code/src
  javac *.java
  java AgriSmartApp
  ```

---

## 4. Test Verification & Evidence Register (`07_Test_Evidence`)

All 16 test cases defined in `06_Test_Cases.xlsx` and the automated 22-test Pytest suite have been executed and verified. The pass rate is **100% (22/22 pytest, 16/16 manual & integration)**.

### Evidence Mapping Table

| Test ID | Mapped Requirement | Test Description | Status | Evidence File(s) in `07_Test_Evidence/` |
|---|---|---|---|---|
| **TC-01** | FR-01 | Sidebar page navigation across all 7 sections | **PASS** | `TC-01_navigation_test.log`, `TC-01_home_dashboard.png` |
| **TC-02** | FR-02, FR-04 | Valid crop recommendation inference | **PASS** | `TC-02_crop_valid.log`, `TC-02_crop_recommendation.png` |
| **TC-03** | FR-03 | Out-of-range soil pH rejection (pH=12.0) | **PASS** | `TC-03_crop_invalid_ph.log` |
| **TC-04** | FR-03 | Missing feature rejection (omitted rainfall) | **PASS** | `TC-04_crop_missing_feature.log` |
| **TC-05** | FR-05, FR-07 | Valid fertilizer recommendation (low N) | **PASS** | `TC-05_fertilizer_valid.log`, `TC-05_fertilizer_recommendation.png` |
| **TC-06** | FR-06 | Unsupported category rejection (`Martian_Regolith`) | **PASS** | `TC-06_fertilizer_invalid_category.log` |
| **TC-07** | FR-06 | Out-of-range numeric rejection (Soil_pH=14.0) | **PASS** | `TC-07_fertilizer_range_validation.log` |
| **TC-08** | FR-08, FR-09 | Valid crop yield regression & dual-unit conversion | **PASS** | `TC-08_yield_valid.log`, `TC-08_crop_yield_prediction.png` |
| **TC-09** | FR-08, FR-12 | Out-of-range future year rejection (Year=2055) | **PASS** | `TC-09_yield_invalid_year.log` |
| **TC-10** | FR-10 | Master model comparison table rendering | **PASS** | `TC-10_performance_check.log`, `TC-10_model_performance.png` |
| **TC-11** | FR-11 | Audited dataset summary metrics rendering | **PASS** | `TC-11_insights_check.log`, `TC-11_dataset_insights.png` |
| **TC-12** | FR-12 | Graceful missing model artifact error handling | **PASS** | `TC-12_missing_artifact_handling.log` |
| **TC-13** | FR-13 | Agronomic limitations & disclaimers audit | **PASS** | `TC-13_disclaimer_audit.log`, `TC-13_about_and_limitations.png` |
| **TC-14** | Java Prototype | Prototype compilation with `javac *.java` | **PASS** | `TC-14_java_compilation.log` |
| **TC-15** | Java Prototype | Non-numeric input trapping (`abc` -> recovery) | **PASS** | `TC-15_java_invalid_numeric.log` |
| **TC-16** | Java Prototype | Minimum and maximum boundary input validation | **PASS** | `TC-16_java_boundary_inputs.log`, `TC_java_interactive_session.log` |
| **Pytest** | Full Suite | 22 automated unit, schema, and smoke tests | **PASS** | `TC_pytest_suite_results.log` |

---

## 5. Execution & Demonstration Commands

### 5.1 Running the Production Streamlit Application
```powershell
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Run automated tests (22 tests)
python -m pytest tests/ -v

# 3. Launch Streamlit web dashboard
python -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 5.2 Running the Java OOP Prototype
```powershell
cd "SE Delieverables\05_Source_Code\src"
javac *.java
java AgriSmartApp
```

---

## 6. Academic Compliance & Integrity Statement

1. **No Fabricated Evidence:** All test execution outputs, logs, and screenshots reflect actual runs executed in the local environment on November 24, 2026.
2. **Methodological Transparency:** All performance metrics reported in `03_SDD`, `08_Final_Report`, and `reports/model_comparison.csv` represent held-out test splits (Stratified 80:20 for classification; chronological 2010–2013 for yield regression).
3. **Agronomic Responsibility:** The software includes explicit disclaimers across all prediction interfaces explaining that outputs are empirical decision-support approximations and not clinical or legal agronomic guarantees.
