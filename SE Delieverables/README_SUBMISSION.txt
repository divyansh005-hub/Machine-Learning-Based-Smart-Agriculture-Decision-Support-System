================================================================================
NIIT UNIVERSITY
DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING
SOFTWARE ENGINEERING PROJECT SUBMISSION MANIFEST
Academic Year: 2026-2027
================================================================================

PROJECT TITLE:
  Machine Learning Based Smart Agriculture Decision Support System (AgriSmart)

STUDENT DETAILS (GROUP 15):
  1. Divyansh Bhatt
  2. Arush Dewangan
  3. Smera Sharma

FACULTY GUIDE:
  Dr. Shreyansh Sharma
  Department of Computer Science & Engineering, NIIT University

SUBMISSION DATE:
  November 2026

REPOSITORY LINK:
  https://github.com/divyansh005-hub/Machine-Learning-Based-Smart-Agriculture-Decision-Support-System.git

================================================================================
1. IMPLEMENTATION ARCHITECTURE (PYTHON & JAVA EXPLANATION)
================================================================================
This software engineering project delivers two complementary implementations:

A. PRIMARY PRODUCTION SYSTEM (Python 3.12 / Scikit-Learn / Streamlit):
   - Located in: `05_Source_Code/python_app/` (and at workspace root)
   - Scope: Complete, end-to-end production Machine Learning decision support
     system featuring 3 trained Scikit-learn pipelines:
       1. Crop Recommendation (Multiclass Classification, 22 classes, Macro-F1: 0.9932)
       2. Fertilizer Recommendation (Multiclass Classification, 7 classes, Macro-F1: 0.8988)
       3. Crop Yield Prediction (Regression, R²: 0.9859, RMSE: 10,756.91 hg/ha)
   - User Interface: Multi-page reactive dashboard with Plotly charts and real-time validation.
   - Test Automation: 22 automated unit, regression, and smoke tests via pytest (100% PASS).

B. ACADEMIC OOP PROTOTYPE (Java JDK 25):
   - Located in: `05_Source_Code/java_prototype/src/`
   - Scope: Developed specifically to fulfill Section 7 of the university's
     "Software Engineering Project Project Documentation & Implementation Guideline"
     ("Small Java Implementation Model").
   - Concepts Demonstrated: Layered architecture (Presentation, Validation, Service),
     strong typing, OOP composition, input boundary checking, and console menu design.

================================================================================
2. COMPLETE DELIVERABLES INVENTORY (01 TO 08)
================================================================================
The submission folder is organized according to the course guideline:

  ├── 01_Project_Proposal.docx & .pdf
  │     Project scope, motivation, problem definition, feasibility, and methodology.
  │
  ├── 02_SRS.docx & .pdf
  │     Software Requirements Specification: 15 functional requirements (FR-01 to FR-15),
  │     6 non-functional requirements (NFR-01 to NFR-06), system use cases, and actors.
  │
  ├── 03_SDD.docx & .pdf
  │     Software Design Document: High-level 3-tier architecture, component design,
  │     UML class diagrams, database/pipeline schemas, and sequence interactions.
  │
  ├── 04_Wireframes.docx & .pdf
  │     UI/UX wireframes, design mockups, input forms, and interactive visualization layouts.
  │
  ├── 05_Source_Code/
  │     ├── python_app/       (Full Python ML & Streamlit source code, models, tests)
  │     ├── java_prototype/   (Academic Java OOP prototype per Guideline Section 7)
  │     └── README.md         (Technical build, run, and architecture instructions)
  │
  ├── 06_Test_Cases.xlsx
  │     Formal traceability test matrix covering all 15 test cases (TC-01 to TC-15).
  │
  ├── 06_Testing_Report.docx & .pdf
  │     Comprehensive testing report: test methodology, automated unit test results,
  │     manual UI verification, cross-validation, and defect logging.
  │
  ├── 07_Test_Evidence/
  │     ├── TC-01_home_dashboard.png            (Live Home dashboard render)
  │     ├── TC-02_crop_recommendation.png       (Live Crop ML prediction & chart)
  │     ├── TC-05_fertilizer_recommendation.png (Live Fertilizer prediction & chart)
  │     ├── TC-08_crop_yield_prediction.png     (Live Yield regression & metric)
  │     ├── TC-10_model_performance.png         (Master comparison matrix)
  │     ├── TC-11_dataset_insights.png          (Interactive EDA distributions)
  │     ├── TC-13_about_and_limitations.png     (Architecture & disclaimers)
  │     ├── pytest_execution_log.txt            (Full CLI log: 22/22 tests passing)
  │     ├── java_compilation_and_run_log.txt    (javac / java execution output)
  │     └── README.txt                          (Evidence index & mapping)
  │
  ├── 08_Final_Report.docx & .pdf
  │     Complete academic project report including student & guide details,
  │     methodology, results, discussion, and future enhancements.
  │
  ├── 08_Presentation.pptx
  │     Project defense slides covering problem, architecture, ML models, and demo.
  │
  ├── README.md
  │     Comprehensive markdown documentation for GitHub and project viewers.
  │
  └── README_SUBMISSION.txt
        This file (Submission manifest and evaluator guide).

================================================================================
3. HOW TO RUN AND VERIFY
================================================================================

A. RUNNING THE PRIMARY PYTHON APPLICATION:
   1. Open terminal in `05_Source_Code/python_app` (or repository root).
   2. Ensure Python 3.11+ is installed.
   3. Install dependencies:
        pip install -r requirements.txt
   4. Launch the application:
        streamlit run app.py
   5. Open browser at: http://localhost:8501

B. EXECUTING THE AUTOMATED TEST SUITE:
   1. In the terminal:
        pytest tests/ -v
   2. Expected Result: 22 passed, 0 failed, 100% pass rate.

C. COMPILING AND RUNNING THE JAVA OOP PROTOTYPE:
   1. Open terminal in `05_Source_Code/java_prototype/src`.
   2. Ensure JDK is installed (JDK 17, 21, or 25).
   3. Compile:
        javac *.java
   4. Execute:
        java AgriSmartApp
   5. Use the interactive console menu (1: Crop, 2: Fertilizer, 3: Yield, 4: Exit).

================================================================================
4. VERIFICATION & ACADEMIC INTEGRITY
================================================================================
- All models were trained and evaluated on real held-out test splits.
- Preprocessing steps were fitted strictly on training data (no data leakage).
- All reported metrics reflect actual scikit-learn evaluations without fabricated figures.
- Test evidence screenshots were captured using automated browser testing on the
  live running Streamlit application.
================================================================================
