"""Generate Deliverables 01, 02, 03, and 04 for AgriSmart.
01_Project_Proposal.docx
02_SRS.docx
03_SDD.docx
04_Wireframes.docx
"""

import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from doc_styling import (
    setup_document, add_title_page, add_heading_1, add_heading_2, add_heading_3,
    add_callout, add_styled_table, COLOR_PRIMARY, COLOR_SECONDARY, COLOR_DARK, COLOR_MUTED
)

OUTPUT_DIR = Path(r"D:\NIIT_University\Projects\Smart Agricultutre\SE_Deliverables_Corrected")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# 01. PROJECT PROPOSAL
# ==============================================================================
def generate_proposal():
    doc = docx.Document()
    setup_document(doc)
    add_title_page(
        doc,
        doc_title="Machine Learning Based Smart Agriculture\nDecision Support System (AgriSmart)",
        doc_subtitle="Comprehensive Project Proposal & Engineering Feasibility Report",
        deliverable_code="Deliverable 01 — Project Proposal"
    )

    add_heading_1(doc, "1. Executive Summary")
    p = doc.add_paragraph(
        "Agriculture forms the vital backbone of India's socioeconomic architecture, providing livelihood for over "
        "54% of the population and contributing substantially to national food security. However, smallholder and "
        "commercial farmers face mounting challenges driven by erratic climate patterns, soil nutrient degradation, "
        "sub-optimal fertilizer application, and unpredictable crop yield fluctuations. The primary objective of "
        "AgriSmart (Machine Learning Based Smart Agriculture Decision Support System) is to design, engineer, and deploy "
        "an end-to-end, data-driven software platform that integrates predictive intelligence across three fundamental "
        "agronomic decisions: (1) Crop Recommendation based on soil chemistry and localized meteorology, (2) Fertilizer "
        "Formulation matching specific soil-crop deficiencies, and (3) Crop Yield Prediction to forecast production capacity. "
        "By fusing advanced machine learning algorithms (Random Forest ensembles, Pipeline preprocessing, and rigorous "
        "cross-validation) with a reactive Streamlit web dashboard and an academic Java OOP architectural model, AgriSmart "
        "bridges the divide between complex agro-ecological data and practical farm-level decision support."
    )

    add_heading_1(doc, "2. Background and Motivation")
    doc.add_paragraph(
        "Traditional agricultural planning has long relied on empirical intuition, generalized regional advisories, or "
        "historical family precedent. In an era characterized by accelerated climate change and localized weather extremes, "
        "these traditional heuristics frequently result in severe financial losses, crop failure, and ecological harm. "
        "Excessive nitrogen application causes groundwater eutrophication and soil acidification, while inadequate potassium "
        "or phosphorus application severely curtails crop resilience against drought and pests. Furthermore, farmers lack "
        "accessible digital tools capable of synthesizing multidimensional environmental data (soil N-P-K, pH, humidity, "
        "ambient temperature, and annual rainfall) into actionable, probabilistic recommendations."
    )
    doc.add_paragraph(
        "The motivation behind this project arises from recent breakthroughs in computational agronomy and machine learning. "
        "Ensemble tree methods, such as Random Forests, possess exceptional capacity to map non-linear agro-climatic "
        "interactions without overfitting. By operationalizing these models inside a transparent, reproducible, and "
        "validated software engineering framework, AgriSmart equips modern agricultural stakeholders with evidence-based "
        "foresight before sowing, fertilizing, and harvesting."
    )

    add_heading_1(doc, "3. Problem Statement & Research Questions")
    doc.add_paragraph(
        "Agricultural practitioners and planners are confronted by three interconnected operational bottlenecks:"
    )
    doc.add_paragraph(
        "1. Crop-Soil Mismatch: Farmers frequently sow crops that are agronomically unsuited to their immediate soil "
        "nutrient profile and rainfall patterns, depressing productivity.\n"
        "2. Indiscriminate Fertilizer Misallocation: Chemical fertilizers are applied without quantitative stoichiometric "
        "balancing against soil requirements, leading to soil exhaustion and unnecessary expenditure.\n"
        "3. Yield Uncertainty: Farmers and commodity planners lack quantitative yield forecasting mechanisms that account "
        "for historical country-level pesticide intensity, rainfall volume, and thermal regimes."
    )
    add_callout(
        doc,
        "Primary Research Question: Can an integrated software system utilizing trained scikit-learn machine learning pipelines "
        "provide reliable, multi-class crop recommendations (Macro-F1 > 0.95), targeted fertilizer classification, and robust "
        "yield regression (R² > 0.95) under a strict chronological validation protocol while maintaining sub-second inference latency?",
        "CORE RESEARCH PROBLEM"
    )

    add_heading_1(doc, "4. Project Objectives")
    headers_obj = ["Objective ID", "Core Objective", "Target Milestone / Metric", "Software Engineering Deliverable"]
    data_obj = [
        ["OBJ-01", "Curate & Audit Agricultural Datasets", "Zero missing values, audited schemas, leakage prevention", "DATA_AUDIT.md & Data Loaders"],
        ["OBJ-02", "Train Crop Classification Pipeline", "Held-out Macro-F1 >= 0.98, Accuracy >= 98%", "crop_recommendation.joblib"],
        ["OBJ-03", "Train Fertilizer Classifier Pipeline", "Held-out Macro-F1 >= 0.85 with class weighting", "fertilizer_recommendation.joblib"],
        ["OBJ-04", "Train Temporal Yield Regressor", "Chronological split (train <=2009, test >=2010), R² >= 0.95", "yield_prediction.joblib"],
        ["OBJ-05", "Develop Reactive Web Dashboard", "Streamlit UI with 7 dedicated pages, input validation, Plotly", "app.py & src/ui/ modules"],
        ["OBJ-06", "Construct Academic OOP Model", "Layered Java CLI prototype demonstrating OOP & collections", "AgriSmartApp & Service (Java)"],
        ["OBJ-07", "Automate Verification & QA", "22 automated pytest tests + 15 manual test matrices (100% PASS)", "tests/ & 06_Testing_Report"]
    ]
    add_styled_table(doc, headers_obj, data_obj, [1.0, 2.0, 1.8, 1.7])

    add_heading_1(doc, "5. Users and Stakeholder Analysis")
    doc.add_paragraph(
        "AgriSmart identifies five distinct user classes across the agricultural and academic spectrum:"
    )
    doc.add_paragraph(
        "• Smallholder & Progressive Farmers: End-users seeking straightforward guidance on optimal crop selection and "
        "fertilizer application based on laboratory soil test reports (Soil Health Cards).\n"
        "• Agricultural Extension Officers & Agronomists: Field professionals who utilize model predictions to counsel farmers, "
        "evaluate nutrient deficiencies, and interpret multi-class probability distributions.\n"
        "• Agricultural Policy Planners & Insurers: Macro-level decision makers utilizing yield prediction models to forecast "
        "food grain output, evaluate regional food security, and plan buffer stocks.\n"
        "• Academic Evaluators & Software Engineers: Faculty guides, examiners, and software architects assessing the system's "
        "requirements traceability, design modularity, test coverage, and adherence to software engineering standards."
    )

    add_heading_1(doc, "6. Scope and System Boundaries")
    doc.add_paragraph(
        "To ensure academic rigor, defensible software engineering, and honest scientific reporting, system boundaries are strictly defined:"
    )
    doc.add_paragraph(
        "In-Scope:\n"
        "• Offline and local-first execution requiring zero paid third-party APIs or cloud databases.\n"
        "• Multiclass classification of 22 distinct agricultural crops using soil chemical (N, P, K, pH) and climatic features.\n"
        "• Classification of 7 common commercial fertilizer formulations utilizing multi-factor soil-crop features with class-weighting.\n"
        "• Multi-variable regression predicting crop yields across 101 countries and 10 major global crops with time-aware splitting.\n"
        "• Comprehensive interactive model performance dashboards and dataset exploratory data analysis (EDA) profiling.\n"
        "• Illustrative Java OOP console prototype adhering strictly to Section 7 of the university course guidelines."
    )
    doc.add_paragraph(
        "Out-of-Scope & Limitations:\n"
        "• AgriSmart does not connect to physical IoT sensors or live satellite imagery feeds in Phase 1.\n"
        "• The system does not claim to replace qualified on-site agronomic soil testing or government extension services.\n"
        "• Crop yield predictions represent historical national/regional statistical trends (FAO aggregates) and must not be "
        "interpreted as guaranteed plot-level harvest contracts."
    )

    add_heading_1(doc, "7. Technology Stack & Architectural Rationale")
    headers_tech = ["Tier / Domain", "Selected Technology", "Version", "Architectural Justification"]
    data_tech = [
        ["Runtime Environment", "Python", "3.12.10", "Standard language for ML, scientific computing, and rapid web prototyping"],
        ["Web Framework", "Streamlit", "1.32.0+", "Reactive, pure-Python UI framework facilitating interactive dashboards without Node.js overhead"],
        ["Machine Learning", "scikit-learn", "1.4.0+", "Industry-standard library for modular Pipeline, ColumnTransformer, and ensemble algorithms"],
        ["Data Manipulation", "pandas & NumPy", "2.2.0+ / 1.26.0+", "High-performance vector operations, tabular data ingestion, and statistical aggregations"],
        ["Data Visualization", "Plotly Express & Graph Objects", "5.19.0+", "Interactive, hardware-accelerated charting for probability distributions and residual plots"],
        ["Model Persistence", "joblib", "1.3.2+", "Efficient, compressed serialization of fitted scikit-learn estimators and preprocessing pipelines"],
        ["Automated Testing", "pytest & pytest-cov", "8.0.0+", "Robust testing harness for unit tests, pipeline smoke tests, and data validation assertion"],
        ["Browser Automation", "Selenium WebDriver", "4.54.0+", "Headless Chrome automation for authentic live UI test execution and screenshot evidence capture"],
        ["Academic Prototype", "Java (JDK)", "25 / 17 LTS", "Demonstrates layered OOP design, strong typing, and boundary checking per SE Guideline Sec 7"]
    ]
    add_styled_table(doc, headers_tech, data_tech, [1.4, 1.4, 0.9, 2.8])

    add_heading_1(doc, "8. Project Schedule & Milestone Timeline")
    headers_time = ["Phase", "Milestone Activity", "Start Date", "End Date", "Status"]
    data_time = [
        ["Phase 1", "Workspace Setup, Data Ingestion & Exploratory Data Audit (DATA_AUDIT.md)", "01-Oct-2026", "10-Oct-2026", "COMPLETED"],
        ["Phase 2", "Model Training, Pipeline Serialization & Chronological Validation", "11-Oct-2026", "25-Oct-2026", "COMPLETED"],
        ["Phase 3", "Streamlit Reactive Dashboard Architecture & Multi-Page Router Design", "26-Oct-2026", "05-Nov-2026", "COMPLETED"],
        ["Phase 4", "Java OOP Console Prototype Engineering (Guideline Section 7)", "06-Nov-2026", "12-Nov-2026", "COMPLETED"],
        ["Phase 5", "Pytest Suite Automation & Selenium Real Test Evidence Capture", "13-Nov-2026", "18-Nov-2026", "COMPLETED"],
        ["Phase 6", "Full Software Engineering Documentation Suite (SRS, SDD, Testing, Final)", "19-Nov-2026", "24-Nov-2026", "COMPLETED"]
    ]
    add_styled_table(doc, headers_time, data_time, [1.0, 2.7, 1.0, 1.0, 0.8])

    add_heading_1(doc, "9. Feasibility Analysis")
    doc.add_paragraph(
        "• Technical Feasibility: The required computing infrastructure (Python 3.12, scikit-learn, Streamlit) is completely open-source, "
        "well-documented, and executable on standard consumer hardware (x86_64, 8GB RAM) without requiring GPU acceleration.\n"
        "• Economic Feasibility: Utilizing open-access agricultural datasets and open-source development stacks ensures total capital "
        "expenditure is zero, making AgriSmart highly viable for educational and community deployment.\n"
        "• Operational Feasibility: The intuitive browser-based interface requires zero command-line expertise from agricultural end-users, "
        "featuring clear metric units, tooltips, and explanatory visual charts."
    )

    add_heading_1(doc, "10. Conclusion and Next Steps")
    doc.add_paragraph(
        "This project proposal establishes the foundational rationale, scope, architectural stack, and feasibility for AgriSmart. "
        "The subsequent deliverables elaborate on system specifications (02_SRS), architectural design (03_SDD), interface wireframes "
        "(04_Wireframes), verification matrices (06_Testing_Report), and the comprehensive synthesis (08_Final_Report)."
    )

    out_file = OUTPUT_DIR / "01_Project_Proposal.docx"
    doc.save(out_file)
    print(f"Generated: {out_file.name} ({os.path.getsize(out_file):,} bytes)")

# ==============================================================================
# 02. SRS — SOFTWARE REQUIREMENTS SPECIFICATION
# ==============================================================================
def generate_srs():
    doc = docx.Document()
    setup_document(doc)
    add_title_page(
        doc,
        doc_title="Software Requirements Specification (SRS)\nfor AgriSmart",
        doc_subtitle="Formal Requirements Engineering Document — Version 1.0 (IEEE 830-1998 Standard)",
        deliverable_code="Deliverable 02 — Software Requirements Specification"
    )

    add_heading_1(doc, "1. Introduction")
    add_heading_2(doc, "1.1 Purpose")
    doc.add_paragraph(
        "This Software Requirements Specification (SRS) establishes a complete, unambiguous, and verifiable contract "
        "governing the functional and non-functional behavior of the Machine Learning Based Smart Agriculture Decision "
        "Support System (AgriSmart). It provides formal specifications for software developers, machine learning engineers, "
        "quality assurance testers, and academic evaluators at NIIT University."
    )
    add_heading_2(doc, "1.2 Document Conventions")
    doc.add_paragraph(
        "This document adheres to the IEEE 830-1998 Recommended Practice for Software Requirements Specifications. "
        "Requirements are categorized as Functional Requirements (FR-xx) and Non-Functional Requirements (NFR-xx). "
        "Priority ratings are classified as High (Mandatory for core operation), Medium (Important for system usability), "
        "and Low (Enhancement)."
    )
    add_heading_2(doc, "1.3 Product Scope")
    doc.add_paragraph(
        "AgriSmart is a standalone, local-first web application designed to assist agricultural practitioners in predicting "
        "crop viability, calculating targeted fertilizer requirements, and estimating historical crop yield. The product incorporates "
        "pre-trained scikit-learn machine learning pipelines, a reactive Streamlit web dashboard, exploratory data analysis modules, "
        "and an independent Java Object-Oriented prototype."
    )
    add_heading_2(doc, "1.4 References")
    doc.add_paragraph(
        "1. IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications.\n"
        "2. NIIT University Software Engineering Project Documentation & Implementation Guideline (Version 1.0, Sept 2026).\n"
        "3. Food and Agriculture Organization (FAO) of the United Nations — Statistical Database (FAOSTAT), 2024.\n"
        "4. Pedregosa et al., 'Scikit-learn: Machine Learning in Python', Journal of Machine Learning Research, 2011."
    )

    add_heading_1(doc, "2. Overall Description")
    add_heading_2(doc, "2.1 Product Perspective")
    doc.add_paragraph(
        "AgriSmart operates as a self-contained, 3-tier desktop/web application running locally in modern web browsers. "
        "The Presentation Tier is governed by Streamlit and Plotly; the Application Tier encapsulates feature preprocessing, "
        "input validation, and scikit-learn model inference; the Data Tier comprises serialized joblib pipelines and audited "
        "CSV datasets. A secondary Java console prototype runs under standard Java Virtual Machine (JVM) environments."
    )
    add_heading_2(doc, "2.2 User Classes & Characteristics")
    doc.add_paragraph(
        "• Field Farmer / Cultivator: Needs simplified graphical input forms, units in kg/ha or ppm, intuitive crop predictions, "
        "and clear disclaimers without technical jargon.\n"
        "• Agricultural Advisor / Extension Officer: Requires detailed probability distributions across candidate crops, feature "
        "importance insights, and comparative analysis.\n"
        "• Software Engineering Evaluator / Faculty: Requires rigorous validation, clean code structure, documented test coverage, "
        "traceability matrices, and reproducible execution."
    )
    add_heading_2(doc, "2.3 Operating Environment")
    doc.add_paragraph(
        "• Host OS: Microsoft Windows 10/11 (x64), Linux (Ubuntu 20.04+), or macOS (12.0+).\n"
        "• Runtime: Python 3.11 or 3.12 (standard CPython) and Java SE Development Kit (JDK 17, 21, or 25).\n"
        "• Client Browser: Google Chrome (v110+), Mozilla Firefox (v115+), or Microsoft Edge (v110+)."
    )
    add_heading_2(doc, "2.4 Design & Implementation Constraints")
    doc.add_paragraph(
        "• Data Leakage Prevention: Preprocessing transformers (imputers, standard scalers, one-hot encoders) must be fitted strictly "
        "on training splits and serialized alongside estimators.\n"
        "• Temporal Leakage Prevention: Yield prediction must be evaluated on a chronological split (training on years <=2009, testing "
        "on years >=2010), forbidding random shuffle splitting.\n"
        "• Disclaimers: The application must visibly display agronomic disclaimers stating that predictions do not constitute guaranteed "
        "advisory prescriptions."
    )

    add_heading_1(doc, "3. Detailed Functional Requirements (FR-01 to FR-15)")
    headers_fr = ["Req ID", "Requirement Description", "Inputs & Boundaries", "Expected Processing & Output", "Priority"]
    data_fr = [
        ["FR-01", "Crop Input Ingestion & Validation", "N (0-140), P (5-145), K (5-205), Temp (8-45°C), Hum (14-100%), pH (3.5-9.9), Rain (20-300mm)", "Validates numerical types and boundaries. Rejects NaN or out-of-bounds with error banner.", "High"],
        ["FR-02", "Crop Recommendation Inference", "7 validated numerical soil/climatic features", "Passes features to Random Forest pipeline; predicts optimal crop label among 22 classes.", "High"],
        ["FR-03", "Crop Probability Distribution", "Fitted Random Forest estimator", "Extracts predict_proba(); displays top-5 candidate crops and confidence percentages via Plotly bar chart.", "Medium"],
        ["FR-04", "Crop Agronomic Guidance", "Predicted crop label", "Displays ideal growing conditions, soil type preferences, and input parameter summary.", "Medium"],
        ["FR-05", "Fertilizer Ingestion & Boundary Check", "19 total features (Temparature, Humidity, Moisture, Soil Type, Crop Type, N, P, K, etc.)", "Validates presence and ranges. Ensures categorical features match training domain.", "High"],
        ["FR-06", "Fertilizer Classification", "Validated fertilizer feature vector", "Executes ColumnTransformer + class-weighted Random Forest; outputs predicted formulation (e.g., Urea, DAP).", "High"],
        ["FR-07", "Fertilizer Confidence & Nutrient Gap", "Predicted class + soil NPK inputs", "Displays prediction probability and comparative delta between current soil nutrients and recommended baseline.", "Medium"],
        ["FR-08", "Fertilizer Advisory Disclaimer", "System prediction state", "Displays persistent note stating recommendations reflect dataset distributions, requiring soil lab confirmation.", "High"],
        ["FR-09", "Yield Ingestion & Chronology Check", "Area (Country), Item (Crop), Year (1990-2013), Rain (mm/yr), Pesticides (tonnes), Temp (°C)", "Validates categorical membership and numeric ranges. Flags historical coverage constraints.", "High"],
        ["FR-10", "Crop Yield Regression", "Validated yield feature tuple", "Executes OneHotEncoder + Random Forest Regressor; computes expected yield in hg/ha and tonnes/ha.", "High"],
        ["FR-11", "Yield Baseline Comparison", "Predicted yield + historical test mean", "Compares predicted yield against baseline mean (78,416.32 hg/ha); shows percentage deviation and historical variance.", "Medium"],
        ["FR-12", "Model Comparison Matrix Display", "reports/model_comparison.csv", "Renders interactive table comparing Dummy, Logistic/Linear Regression, and Random Forest across all 3 modules.", "Medium"],
        ["FR-13", "Exploratory Data Insights Profiling", "Dataset loaders (Crop, Fert, Yield)", "Generates interactive histograms, correlation matrices, and class distribution plots dynamically.", "Medium"],
        ["FR-14", "Deep Linking & View Routing", "URL query parameter `?page=<name>`", "Enables direct programmatic deep-linking to Home, Crop, Fertilizer, Yield, Performance, Insights, About.", "Medium"],
        ["FR-15", "Java OOP Console Prototype", "Interactive CLI menu input (1 to 4)", "Executes rule-based validation, layered service calls, and mock decision output in Java console.", "High"]
    ]
    add_styled_table(doc, headers_fr, data_fr, [0.8, 1.8, 1.8, 1.6, 0.5])

    add_heading_1(doc, "4. Non-Functional Requirements (NFR-01 to NFR-06)")
    headers_nfr = ["NFR ID", "Category", "Specification Metric / Target", "Verification Method"]
    data_nfr = [
        ["NFR-01", "Performance & Latency", "Model inference execution time < 150ms per query; initial page load < 2.5s", "Automated timing benchmarks"],
        ["NFR-02", "Usability & Accessibility", "Consistent agricultural theme (#1B4D3E), responsive layout, tooltips on all inputs", "Visual inspection & user test"],
        ["NFR-03", "Reliability & Resilience", "Zero unhandled exceptions; 100% graceful degradation on invalid or boundary inputs", "Pytest suite & negative testing"],
        ["NFR-04", "Maintainability & Modularity", "PEP 8 compliant, layered architecture, strict separation of UI, data, and models", "Code review & static analysis"],
        ["NFR-05", "Portability & Self-Containment", "Executes identically across Windows, Linux, and macOS without external database dependencies", "Cross-platform test runs"],
        ["NFR-06", "Safety & Agronomic Integrity", "Prominent disclaimer on all prediction screens; zero fabricated performance metrics", "Audit of UI & documentation"]
    ]
    add_styled_table(doc, headers_nfr, data_nfr, [0.8, 1.5, 2.7, 1.5])

    add_heading_1(doc, "5. Detailed Use Case Specifications")
    headers_uc = ["Field", "Use Case UC-01: Crop Recommendation", "Use Case UC-03: Crop Yield Prediction"]
    data_uc = [
        ["Use Case ID", "UC-01", "UC-03"],
        ["Actor", "Farmer / Agricultural Advisor", "Agricultural Planner / Policy Researcher"],
        ["Preconditions", "Streamlit application is running; crop_recommendation.joblib is loaded.", "Application running; yield_prediction.joblib loaded."],
        ["Trigger", "User navigates to 'Crop Recommendation' and clicks 'Predict'.", "User navigates to 'Crop Yield Prediction' and clicks 'Predict'."],
        ["Main Flow", "1. User inputs N, P, K, Temp, Humidity, pH, Rainfall.\n2. System validates input bounds.\n3. Model pipeline processes feature array.\n4. System displays predicted crop, confidence %, and Plotly distribution.", "1. User selects Country, Crop, Year, Rain, Pesticides, Temp.\n2. System validates inputs.\n3. Pipeline encodes categories and executes regression.\n4. System displays yield in hg/ha and t/ha with baseline comparison."],
        ["Alternate Flow", "If inputs are outside agronomic limits, system halts inference and renders error warning alert.", "If selected country/crop combination is invalid, system displays contextual validation warning."],
        ["Postconditions", "User receives actionable recommendation with agronomic guidance.", "User receives quantitative yield estimate and historical variance."]
    ]
    add_styled_table(doc, headers_uc, data_uc, [1.5, 2.5, 2.5])

    add_heading_1(doc, "6. Data Requirements & Validation Matrix")
    doc.add_paragraph(
        "The system enforces strict numerical and categorical boundaries based on empirical audits of source datasets:"
    )
    headers_data = ["Feature Name", "Data Type", "Valid Range / Domain", "Agronomic Unit", "Target Module"]
    data_data = [
        ["Nitrogen (N)", "Float / Int", "0.0 to 140.0", "Ratio / ppm (mg/kg)", "Crop & Fertilizer"],
        ["Phosphorus (P)", "Float / Int", "5.0 to 145.0", "Ratio / ppm (mg/kg)", "Crop & Fertilizer"],
        ["Potassium (K)", "Float / Int", "5.0 to 205.0", "Ratio / ppm (mg/kg)", "Crop & Fertilizer"],
        ["Temperature", "Float", "8.0 to 45.0", "Degrees Celsius (°C)", "Crop & Fertilizer & Yield"],
        ["Humidity", "Float", "14.0 to 100.0", "Relative Humidity (%)", "Crop & Fertilizer"],
        ["Soil pH", "Float", "3.5 to 9.9", "Standard pH Scale", "Crop Recommendation"],
        ["Rainfall", "Float", "20.0 to 300.0 (Crop) / 50 to 3500 (Yield)", "Millimeters (mm)", "Crop & Yield"],
        ["Soil Type", "Categorical", "Sandy, Loamy, Black, Red, Clayey", "Text Nominal", "Fertilizer Recommendation"],
        ["Crop Type", "Categorical", "Maize, Sugarcane, Cotton, Tobacco, Paddy, etc.", "Text Nominal", "Fertilizer & Yield"],
        ["Country / Area", "Categorical", "101 global agricultural nations (FAOSTAT)", "Text Nominal", "Yield Prediction"],
        ["Pesticide Usage", "Float", "0.0 to 400,000.0", "Tonnes active ingredient", "Yield Prediction"]
    ]
    add_styled_table(doc, headers_data, data_data, [1.4, 1.0, 1.8, 1.1, 1.2])

    add_heading_1(doc, "7. Requirements Traceability Verification")
    doc.add_paragraph(
        "Every requirement defined in this SRS is traced directly to its architectural design element in 03_SDD, "
        "its source code implementation in 05_Source_Code, and its validation test case in 06_Testing_Report."
    )

    out_file = OUTPUT_DIR / "02_SRS.docx"
    doc.save(out_file)
    print(f"Generated: {out_file.name} ({os.path.getsize(out_file):,} bytes)")

# ==============================================================================
# 03. SDD — SOFTWARE DESIGN DOCUMENT
# ==============================================================================
def generate_sdd():
    doc = docx.Document()
    setup_document(doc)
    add_title_page(
        doc,
        doc_title="Software Design Document (SDD)\nfor AgriSmart",
        doc_subtitle="System Architecture, Component Specifications, and Object-Oriented Design (IEEE 1016 Standard)",
        deliverable_code="Deliverable 03 — Software Design Document"
    )

    add_heading_1(doc, "1. Introduction & Design Goals")
    doc.add_paragraph(
        "This Software Design Document (SDD) provides a comprehensive architectural and detailed structural blueprint "
        "for AgriSmart. It translates the functional and non-functional requirements articulated in 02_SRS into concrete "
        "software engineering components, data models, UML class structures, sequence interactions, and deployment artifacts."
    )
    doc.add_paragraph(
        "Core Architectural Principles:\n"
        "• Modularity & Separation of Concerns: Decoupling UI presentation, model inference, and data loaders.\n"
        "• Determinism & Reproducibility: Enforcing fixed random states, versioned dependencies, and serialized pipeline transformers.\n"
        "• Zero Data Leakage: Encapsulating all feature scalers and categorical encoders inside scikit-learn Pipeline objects.\n"
        "• Dual Implementation Cohesion: Maintaining a production Python ML application alongside a compliant Java OOP model."
    )

    add_heading_1(doc, "2. High-Level System Architecture")
    doc.add_paragraph(
        "AgriSmart employs a modern 3-Tier Layered Architecture with Model-View-Controller (MVC) characteristics:"
    )
    headers_arch = ["Tier / Layer", "Primary Subsystems & Components", "Responsibilities & Data Flow"]
    data_arch = [
        ["Presentation Tier", "Streamlit Multi-Page Views (Home, Crop, Fert, Yield, Performance, Insights, About)", "Accepts user inputs via interactive widgets; renders Plotly charts, prediction cards, and validation banners."],
        ["Service / Logic Tier", "src/models/predict.py, src/features/preprocessing.py, src/utils/constants.py", "Performs boundary validation, feature vector construction, pipeline deserialization, and inference execution."],
        ["Data & Model Tier", "models/*.joblib, dataset/*.csv, reports/model_comparison.csv", "Stores serialized scikit-learn estimators, metadata JSON files, historical CSV datasets, and benchmark evaluation tables."],
        ["Academic JVM Tier", "java_prototype/src/ (AgriSmartApp, InputValidator, AgricultureService)", "Self-contained Java console prototype demonstrating OOP encapsulation, strong typing, and boundary verification."]
    ]
    add_styled_table(doc, headers_arch, data_arch, [1.4, 2.2, 2.9])

    add_heading_1(doc, "3. Component & Module Design")
    headers_comp = ["Component Name", "File Location", "Interface Methods / Classes", "Dependencies"]
    data_comp = [
        ["Data Loader Component", "src/data/loaders.py", "load_crop_data(), load_fertilizer_data(), load_yield_data()", "pandas, pathlib"],
        ["Preprocessing Component", "src/features/preprocessing.py", "build_crop_pipeline(), build_fertilizer_pipeline(), build_yield_pipeline()", "scikit-learn (Pipeline, ColumnTransformer, StandardScaler, OneHotEncoder)"],
        ["Model Training Engine", "src/models/train.py", "train_all_models(), evaluate_model(), serialize_pipeline()", "scikit-learn, joblib, pandas"],
        ["Inference Service", "src/models/predict.py", "predict_crop(), predict_fertilizer(), predict_yield()", "joblib, numpy, pandas"],
        ["UI View Router", "app.py", "main(), render_sidebar(), route_page()", "streamlit, src/ui/*"],
        ["Crop UI View", "src/ui/crop_page.py", "render_crop_page()", "streamlit, plotly, predict_crop()"],
        ["Fertilizer UI View", "src/ui/fertilizer_page.py", "render_fertilizer_page()", "streamlit, plotly, predict_fertilizer()"],
        ["Yield UI View", "src/ui/yield_page.py", "render_yield_page()", "streamlit, plotly, predict_yield()"],
        ["Java CLI Prototype", "java_prototype/src/AgriSmartApp.java", "AgriSmartApp.main(), AgricultureService, InputValidator", "Standard Java SDK (java.util.*)"]
    ]
    add_styled_table(doc, headers_comp, data_comp, [1.4, 1.6, 2.0, 1.5])

    add_heading_1(doc, "4. Object-Oriented Class Design (UML Specifications)")
    doc.add_paragraph(
        "To satisfy software engineering best practices, both the Python service abstractions and the Java academic prototype "
        "demonstrate formal Object-Oriented Design patterns:"
    )
    add_heading_2(doc, "4.1 Java Academic OOP Classes (Guideline Section 7)")
    headers_java_class = ["Class Name", "Role / Layer", "Key Attributes", "Key Methods & Signatures"]
    data_java_class = [
        ["AgriSmartApp", "Presentation / Controller", "private Scanner scanner;\nprivate AgricultureService service;\nprivate InputValidator validator;", "public static void main(String[] args)\nprivate void displayMenu()\nprivate void handleCrop()\nprivate void handleFertilizer()\nprivate void handleYield()"],
        ["InputValidator", "Validation Service", "private final double MIN_PH = 3.5;\nprivate final double MAX_PH = 9.9;\nprivate final double MIN_N = 0.0;", "public boolean validateNutrients(double n, double p, double k)\npublic boolean validatePH(double ph)\npublic boolean validateYear(int year)"],
        ["AgricultureService", "Domain Service", "private Map<String, String> cropRules;\nprivate Map<String, String> fertRules;", "public String recommendCrop(double n, double p, double k, double ph)\npublic String recommendFertilizer(String soil, String crop)\npublic double estimateYield(String country, String crop, int year)"]
    ]
    add_styled_table(doc, headers_java_class, data_java_class, [1.3, 1.5, 1.8, 1.9])

    add_heading_1(doc, "5. Sequence & Activity Flow")
    doc.add_paragraph(
        "The end-to-end prediction execution flow is structured to guarantee validation before inference:"
    )
    doc.add_paragraph(
        "1. User Action: User inputs agricultural parameters into Streamlit widgets and clicks 'Predict Recommended Crop'.\n"
        "2. Client Boundary Check: UI handler verifies numerical inputs against constants defined in `src/utils/constants.py`.\n"
        "3. Service Dispatch: UI invokes `predict_crop(input_dict)` in `src/models/predict.py`.\n"
        "4. Model Retrieval: Service retrieves cached pipeline artifact from `models/crop_recommendation.joblib` via `@st.cache_resource`.\n"
        "5. Transformation & Estimation: scikit-learn Pipeline standardizes feature vector and queries Random Forest estimator.\n"
        "6. Probability Extraction: Service queries `predict_proba()` to compute candidate crop probability distribution.\n"
        "7. Response Rendering: Streamlit renders recommendation card, confidence badge, and Plotly interactive bar chart."
    )

    add_heading_1(doc, "6. Data Model & Pipeline Persistence Specification")
    doc.add_paragraph(
        "All trained models are serialized using `joblib` with compression level 3, paired with human-readable JSON metadata:"
    )
    headers_meta = ["Artifact File", "Fitted Pipeline Architecture", "Target Metric", "JSON Metadata Companion"]
    data_meta = [
        ["crop_recommendation.joblib", "Pipeline([('scaler', StandardScaler()), ('classifier', RandomForestClassifier(n_estimators=100))])", "Macro-F1: 0.9932\nAccuracy: 99.32%", "crop_recommendation_meta.json (feature names, classes, training date)"],
        ["fertilizer_recommendation.joblib", "Pipeline([('preprocessor', ColumnTransformer(scaler, ohe)), ('clf', RandomForestClassifier(class_weight='balanced'))])", "Macro-F1: 0.8988\nAccuracy: 95.00%", "fertilizer_recommendation_meta.json (categorical mappings, class list)"],
        ["yield_prediction.joblib", "Pipeline([('col_trans', ColumnTransformer(ohe, passthrough)), ('regressor', RandomForestRegressor(n_estimators=100))])", "R²: 0.9859\nRMSE: 10,756.91 hg/ha", "yield_prediction_meta.json (chronological split bounds: train <=2009, test >=2010)"]
    ]
    add_styled_table(doc, headers_meta, data_meta, [1.6, 2.2, 1.3, 1.4])

    add_heading_1(doc, "7. Requirements Traceability Matrix")
    headers_rtm = ["SRS Requirement ID", "SDD Architectural Component", "Implementation Source File", "Validation Test Case"]
    data_rtm = [
        ["FR-01, FR-02 (Crop)", "Inference Service & Preprocessing", "src/models/predict.py, src/ui/crop_page.py", "TC-02, test_inference.py::test_crop_predict"],
        ["FR-03 (Probability)", "Plotly Distribution Engine", "src/ui/crop_page.py", "TC-02, test_app_smoke.py"],
        ["FR-05, FR-06 (Fertilizer)", "ColumnTransformer & RF Classifier", "src/models/predict.py, src/ui/fertilizer_page.py", "TC-05, test_inference.py::test_fertilizer_predict"],
        ["FR-09, FR-10 (Yield)", "Chronological Split Regressor", "src/models/predict.py, src/ui/yield_page.py", "TC-08, test_inference.py::test_yield_predict"],
        ["FR-12 (Performance)", "Metrics Table & Evaluation View", "src/ui/performance_page.py", "TC-10, test_app_smoke.py"],
        ["FR-13 (EDA Insights)", "Exploratory Profiling View", "src/ui/insights_page.py", "TC-11, test_data_loaders.py"],
        ["FR-15 (Java Prototype)", "Java Layered OOP Subsystem", "java_prototype/src/AgriSmartApp.java", "TC-15, java_compilation_and_run_log.txt"]
    ]
    add_styled_table(doc, headers_rtm, data_rtm, [1.4, 1.8, 1.8, 1.5])

    out_file = OUTPUT_DIR / "03_SDD.docx"
    doc.save(out_file)
    print(f"Generated: {out_file.name} ({os.path.getsize(out_file):,} bytes)")

# ==============================================================================
# 04. WIREFRAMES & UI DESIGN
# ==============================================================================
def generate_wireframes():
    doc = docx.Document()
    setup_document(doc)
    add_title_page(
        doc,
        doc_title="UI / UX Wireframe Specification\nfor AgriSmart",
        doc_subtitle="Interface Architecture, Visual Layouts, Interaction Models, and Design Guidelines",
        deliverable_code="Deliverable 04 — Wireframe Documentation"
    )

    add_heading_1(doc, "1. Design Philosophy & UI Design System")
    doc.add_paragraph(
        "AgriSmart's visual design system is tailored for agricultural professionals, agronomists, and non-technical farmers. "
        "The interface balances clean modern minimalism with high information density, clear visual hierarchies, and prominent "
        "agronomic disclaimers."
    )
    headers_color = ["Design Token", "Color Name", "Hex Code", "Application Context"]
    data_color = [
        ["Primary Accent", "Forest Green", "#1B4D3E", "Hero titles, main navigation headers, primary prediction buttons"],
        ["Secondary Accent", "Emerald Green", "#2E7D32", "Metric callout cards, success badges, Plotly primary bars"],
        ["Warning Accent", "Amber", "#FFA000", "Advisory disclaimers, boundary warnings, rare class flags"],
        ["Background Base", "Off-White / Soft Gray", "#F8F9FA", "Page background, container cards, table alternating rows"],
        ["Text High Contrast", "Slate Dark", "#2C3E50", "Body typography, input labels, chart titles"],
        ["Text Subdued", "Muted Gray", "#64748B", "Input descriptions, measurement units, footnote references"]
    ]
    add_styled_table(doc, headers_color, data_color, [1.4, 1.3, 1.0, 2.8])

    add_heading_1(doc, "2. Global Layout & Navigation Shell")
    doc.add_paragraph(
        "The application employs a dual-column layout comprising a persistent left-hand sidebar router and an expansive "
        "right-hand content canvas. The sidebar enables one-click routing across all seven system pages and displays project "
        "metadata and live system status indicators."
    )
    doc.add_paragraph(
        "Page Navigation Map:\n"
        "• Home Dashboard (`?page=Home`): High-level system overview, dataset metrics, module cards.\n"
        "• Crop Recommendation (`?page=Crop`): Input sliders for soil chemistry/weather, prediction card, probability chart.\n"
        "• Fertilizer Recommendation (`?page=Fertilizer`): Categorical dropdowns and nutrient inputs, dosage card.\n"
        "• Crop Yield Prediction (`?page=Yield`): Country/crop selectors, year/weather inputs, yield in hg/ha and t/ha.\n"
        "• Model Performance (`?page=Performance`): Master model comparison matrix, evaluation charts, confusion matrices.\n"
        "• Dataset Insights (`?page=Insights`): Tabbed exploratory data analysis, correlation heatmaps, feature distributions.\n"
        "• About & Limitations (`?page=About`): System architecture, agronomic disclaimers, academic citations."
    )

    add_heading_1(doc, "3. Screen Wireframe Specifications")

    add_heading_2(doc, "3.1 Screen 1: Home Dashboard Wireframe")
    headers_s1 = ["Zone", "UI Component", "Functional Specification"]
    data_s1 = [
        ["Top Banner", "Hero Title & Description", "Displays 'AgriSmart: Smart Agriculture Decision Support System' with subtitle."],
        ["Metrics Bar", "3 Key Metric Tiles", "Tile 1: '2,200 Audited Crop Records' | Tile 2: '99 Fertilizer Profiles' | Tile 3: '28,242 Historical Yield Records'."],
        ["Cards Grid", "3 Module Navigation Cards", "Card A: Crop Viability Classifier | Card B: Fertilizer Formulation | Card C: Yield Forecast Regressor."],
        ["Bottom Section", "System Health & Integrity Badge", "Displays 'All 3 Models Loaded & Validated — Zero Data Leakage Protocol Enforced'."]
    ]
    add_styled_table(doc, headers_s1, data_s1, [1.3, 1.8, 3.4])

    add_heading_2(doc, "3.2 Screen 2: Crop Recommendation Wireframe")
    headers_s2 = ["Zone", "UI Component", "Functional Specification"]
    data_s2 = [
        ["Input Column 1", "Soil Nutrients (N, P, K)", "3 numerical sliders: Nitrogen (0-140), Phosphorus (5-145), Potassium (5-205)."],
        ["Input Column 2", "Weather & Climate", "4 numerical sliders: Temp (8-45°C), Humidity (14-100%), pH (3.5-9.9), Rainfall (20-300mm)."],
        ["Action Bar", "Submit Button", "Full-width primary button: 'Predict Recommended Crop'."],
        ["Result Zone", "Prediction Banner & Confidence", "Prominent card: 'Recommended Crop: RICE (Confidence: 99.4%)'."],
        ["Chart Zone", "Plotly Distribution Chart", "Horizontal bar chart showing top-5 candidate probabilities (Rice, Jute, Cotton, etc.)."]
    ]
    add_styled_table(doc, headers_s2, data_s2, [1.3, 1.8, 3.4])

    add_heading_2(doc, "3.3 Screen 3: Fertilizer Recommendation Wireframe")
    headers_s3 = ["Zone", "UI Component", "Functional Specification"]
    data_s3 = [
        ["Input Column 1", "Soil & Crop Categoricals", "Dropdown 1: Soil Type (Sandy, Loamy, Black, etc.) | Dropdown 2: Crop Type (Maize, Sugarcane, etc.)."],
        ["Input Column 2", "Soil Chemistry & Moisture", "Moisture slider (25-65%), Soil Nitrogen, Phosphorus, Potassium sliders."],
        ["Action Bar", "Submit Button", "Button: 'Predict Fertilizer Formulation'."],
        ["Result Zone", "Dosage & Formulation Card", "Card: 'Recommended Formulation: UREA (Confidence: 96.2%)'."],
        ["Advisory Zone", "Agronomic Disclaimer Banner", "Alert banner: 'Notice: Data-driven recommendation; confirm with local soil testing laboratory'."]
    ]
    add_styled_table(doc, headers_s3, data_s3, [1.3, 1.8, 3.4])

    add_heading_2(doc, "3.4 Screen 4: Crop Yield Prediction Wireframe")
    headers_s4 = ["Zone", "UI Component", "Functional Specification"]
    data_s4 = [
        ["Input Column 1", "Geographic & Crop Selection", "Dropdown 1: Country / Area (101 nations) | Dropdown 2: Crop / Item (10 global staples)."],
        ["Input Column 2", "Agronomic & Meteorological Factors", "Year slider (1990-2013), Rainfall (mm/year), Pesticides (tonnes), Temp (°C)."],
        ["Action Bar", "Submit Button", "Button: 'Predict Crop Yield'."],
        ["Result Zone", "Yield Metric Cards (Dual Units)", "Card 1: 'Estimated Yield: 54,230 hg/ha' | Card 2: 'Equivalent: 5.42 tonnes/ha'."],
        ["Context Zone", "Historical Baseline Reference", "Compares predicted harvest against historical test baseline mean (78,416.32 hg/ha)."]
    ]
    add_styled_table(doc, headers_s4, data_s4, [1.3, 1.8, 3.4])

    add_heading_1(doc, "4. Responsive & Accessibility Design Verification")
    doc.add_paragraph(
        "• Mobile & Desktop Viewport Adaptation: All form elements automatically wrap into single-column vertical stacks on viewports < 768px.\n"
        "• Contrast Ratio Compliance: Typography meets WCAG 2.1 AA standards (minimum contrast ratio > 4.5:1 against #F8F9FA base).\n"
        "• Screen Reader Support: All input widgets possess programmatic aria-labels and descriptive text units."
    )

    out_file = OUTPUT_DIR / "04_Wireframes.docx"
    doc.save(out_file)
    print(f"Generated: {out_file.name} ({os.path.getsize(out_file):,} bytes)")

if __name__ == "__main__":
    generate_proposal()
    generate_srs()
    generate_sdd()
    generate_wireframes()
    print("Deliverables 01, 02, 03, 04 generated successfully.")
