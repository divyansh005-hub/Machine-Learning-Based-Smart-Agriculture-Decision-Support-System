AgriSmart — Software Engineering Test Evidence Register
Module: 07_Test_Evidence
Institution: NIIT University | Group 15 | September–November 2026

This directory contains authentic empirical verification artifacts, execution logs, and user interface screenshots for all test cases (TC-01 through TC-16) mapped to SRS Functional Requirements (FR-01 through FR-13) and Java prototype requirements.

================================================================================
EVIDENCE DIRECTORY INDEX
================================================================================

1. Automated Test Suite Results
   - TC_pytest_suite_results.log: Complete execution trace of the 22 automated unit, integration, and smoke tests (Pytest). All 22 tests passing (100% pass rate).

2. Streamlit Web Application Evidence (TC-01 through TC-13)
   - TC-01:
     * TC-01_navigation_test.log: Route accessibility and verification log for all 7 sidebar navigation pages.
     * TC-01_home_dashboard.png: Rendered screenshot of the Home Dashboard, model status cards, and audited dataset metrics.
   - TC-02:
     * TC-02_crop_valid.log: Execution trace of valid crop inference (N=90, P=42, K=43, temp=20.8, humidity=82.0, pH=6.5, rainfall=202.9).
     * TC-02_crop_recommendation.png: Screenshot of Crop Recommendation page showing input sliders, recommendation box (RICE), and top candidate probabilities.
   - TC-03:
     * TC-03_crop_invalid_ph.log: Intercepted InputValidationError trace for out-of-range soil pH (pH=12.0; permitted: 3.5 - 10.0).
   - TC-04:
     * TC-04_crop_missing_feature.log: Intercepted InputValidationError trace for missing required feature ('rainfall').
   - TC-05:
     * TC-05_fertilizer_valid.log: Execution trace of valid fertilizer recommendation with 19 soil/crop features (Low N=35 kg/ha -> Urea).
     * TC-05_fertilizer_recommendation.png: Screenshot of Fertilizer Recommendation page showing tabbed configuration and recommendation output.
   - TC-06:
     * TC-06_fertilizer_invalid_category.log: Intercepted InputValidationError trace for unrecognized category (Soil_Type='Martian_Regolith').
   - TC-07:
     * TC-07_fertilizer_range_validation.log: Intercepted InputValidationError trace for out-of-range numeric input (Soil_pH=14.0).
   - TC-08:
     * TC-08_yield_valid.log: Execution trace of crop yield regression (India, Wheat, Year=2013, rainfall=1083 mm, pesticides=50000 t, temp=24.5°C).
     * TC-08_crop_yield_prediction.png: Screenshot of Crop Yield Prediction page displaying dual units: hg/ha and tonnes/ha.
   - TC-09:
     * TC-09_yield_invalid_year.log: Intercepted InputValidationError trace for extreme year extrapolation (Year=2055; permitted: 1960 - 2050).
   - TC-10:
     * TC-10_performance_check.log: Empirical benchmark artifact verification (reports/model_comparison.csv).
     * TC-10_model_performance.png: Screenshot of Model Performance dashboard displaying master comparison table and confusion matrices.
   - TC-11:
     * TC-11_insights_check.log: Audit profile verification of canonical datasets (Crop, Fertilizer, FAO Yield).
     * TC-11_dataset_insights.png: Screenshot of Dataset Insights page with class distribution and feature correlation charts.
   - TC-12:
     * TC-12_missing_artifact_handling.log: Exception trace verifying ModelArtifactNotFoundError handling without system crash.
   - TC-13:
     * TC-13_disclaimer_audit.log: Verification log of agronomic disclaimers across all prediction endpoints.
     * TC-13_about_and_limitations.png: Screenshot of About & Limitations page showing methodology and ethical notice.

3. Java OOP Academic Prototype Evidence (TC-14 through TC-16)
   - TC-14:
     * TC-14_java_compilation.log: Compiler output from 'javac AgricultureService.java AgriSmartApp.java InputValidator.java' (Exit code: 0).
   - TC-15:
     * TC-15_java_invalid_numeric.log: Terminal session log verifying non-numeric input ('abc') trapping and graceful recovery.
   - TC-16:
     * TC-16_java_boundary_inputs.log: Terminal session log verifying minimum boundary (N=0, rain=20) and maximum boundary (N=140, rain=300) handling.
   - TC_java_interactive_session.log: Full end-to-end interactive CLI demonstration transcript across all menu options.

Execution Environment:
- OS: Windows 11 / Windows Server
- Python: 3.12.10
- Java: OpenJDK / Oracle JDK 25 LTS (build 25+37-LTS-3491)
- Timestamp: November 2026
- Status across all test cases: 100% PASS
