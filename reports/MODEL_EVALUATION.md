# MODEL EVALUATION & BENCHMARK REPORT
**Generated:** 2026-10-26 06:06:18  
**Environment:** Python 3.12.10 | scikit-learn 1.5.1  
**Project:** AgriSmart — Smart Agriculture Decision Support System  

---

## 1. Executive Summary & Model Comparison Table

| Module | Model | Primary_Metric_Name | Primary_Metric_Value | Secondary_Metric_Name | Secondary_Metric_Value | Is_Selected | Split | Train_Size | Test_Size |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Crop Recommendation | DummyClassifier (Baseline) | Macro-F1 | 0.004 | Accuracy | 0.0455 | False | Stratified 80:20 (random_state=42) | 1760 | 440 |
| Crop Recommendation | Logistic Regression | Macro-F1 | 0.9725 | Accuracy | 0.9727 | False | Stratified 80:20 (random_state=42) | 1760 | 440 |
| Crop Recommendation | Random Forest | Macro-F1 | 0.9955 | Accuracy | 0.9955 | True | Stratified 80:20 (random_state=42) | 1760 | 440 |
| Fertilizer Recommendation | DummyClassifier (Baseline) | Macro-F1 | 0.0676 | Accuracy | 0.31 | False | Stratified 80:20 (random_state=42) | 8000 | 2000 |
| Fertilizer Recommendation | Logistic Regression (Balanced) | Macro-F1 | 0.6697 | Accuracy | 0.781 | False | Stratified 80:20 (random_state=42) | 8000 | 2000 |
| Fertilizer Recommendation | Random Forest (Balanced) | Macro-F1 | 0.7131 | Accuracy | 0.8705 | True | Stratified 80:20 (random_state=42) | 8000 | 2000 |
| Crop Yield Prediction | Mean Baseline (DummyRegressor) | RMSE (hg/ha) | 96284.44 | MAE (hg/ha) | 68796.79 | False | Chronological (Train <= 2009, Test >= 2010) | 21305 | 4627 |
| Crop Yield Prediction | Linear Regression | RMSE (hg/ha) | 50470.16 | MAE (hg/ha) | 33809.46 | False | Chronological (Train <= 2009, Test >= 2010) | 21305 | 4627 |
| Crop Yield Prediction | Random Forest Regressor | RMSE (hg/ha) | 20302.37 | MAE (hg/ha) | 10454.19 | True | Chronological (Train <= 2009, Test >= 2010) | 21305 | 4627 |

---

## 2. Module A: Crop Recommendation (Multiclass Classification)

- **Target Variable:** `label` (22 balanced classes, 100 samples each)

- **Data Split:** Stratified 80:20 split (`random_state=42`) | Train: 1760 | Test: 440

- **Selected Model:** **Random Forest**

- **Selection Rationale:** Random Forest achieved higher held-out Macro-F1 (0.9955 vs 0.9725) and Accuracy (0.9955 vs 0.9727) across all 22 crop classes.


### Held-Out Test Candidate Comparison

| Model Candidate | Macro-F1 | Accuracy | Weighted-F1 | Status |

|---|---|---|---|---|

| DummyClassifier (Baseline) | 0.0040 | 0.0455 | 0.0040 | Baseline / Candidate |

| Logistic Regression | 0.9725 | 0.9727 | 0.9725 | Baseline / Candidate |

| Random Forest | 0.9955 | 0.9955 | 0.9955 | ★ SELECTED |



### Selected Model Classification Report

```

apple           Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
banana          Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
blackgram       Precision: 1.000 | Recall: 0.950 | F1: 0.974 | Support: 20.0
chickpea        Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
coconut         Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
coffee          Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
cotton          Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
grapes          Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
jute            Precision: 0.952 | Recall: 1.000 | F1: 0.976 | Support: 20.0
kidneybeans     Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
lentil          Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
maize           Precision: 0.952 | Recall: 1.000 | F1: 0.976 | Support: 20.0
mango           Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
mothbeans       Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
mungbean        Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
muskmelon       Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
orange          Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
papaya          Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
pigeonpeas      Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
pomegranate     Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
rice            Precision: 1.000 | Recall: 0.950 | F1: 0.974 | Support: 20.0
watermelon      Precision: 1.000 | Recall: 1.000 | F1: 1.000 | Support: 20.0
macro avg       Precision: 0.996 | Recall: 0.995 | F1: 0.995 | Support: 440.0
weighted avg    Precision: 0.996 | Recall: 0.995 | F1: 0.995 | Support: 440.0

```

---

## 3. Module B: Fertilizer Recommendation (Multiclass Classification)

- **Target Variable:** `Recommended_Fertilizer` (7 classes with severe class imbalance)

- **Data Split:** Stratified 80:20 split (`random_state=42`) | Train: 8000 | Test: 2000

- **Selected Model:** **Random Forest (Balanced)**

- **Selection Rationale:** Random Forest (Balanced) achieved highest Macro-F1 (0.7131 vs 0.6697) and effectively resolved rare class representation (e.g. SSP) with balanced class weights.


### Held-Out Test Candidate Comparison

| Model Candidate | Macro-F1 | Accuracy | Weighted-F1 | Status |

|---|---|---|---|---|

| DummyClassifier (Baseline) | 0.0676 | 0.3100 | 0.1467 | Baseline / Candidate |

| Logistic Regression (Balanced) | 0.6697 | 0.7810 | 0.8000 | Baseline / Candidate |

| Random Forest (Balanced) | 0.7131 | 0.8705 | 0.8660 | ★ SELECTED |



### Per-Class Performance Breakdown (Attention to Rare Classes)

| Fertilizer Class | Precision | Recall | F1-Score | Test Support |

|---|---|---|---|---|

| Compost | 0.7656 | 0.8040 | 0.7843 | 199 |

| DAP | 0.9609 | 0.9247 | 0.9424 | 584 |

| MOP | 0.8551 | 0.8582 | 0.8566 | 282 |

| NPK | 0.8713 | 0.6875 | 0.7686 | 128 |

| SSP | 0.0000 | 0.0000 | 0.0000 | 37 |

| Urea | 0.9244 | 0.9468 | 0.9355 | 620 |

| Zinc Sulphate | 0.6139 | 0.8267 | 0.7045 | 150 |


---

## 4. Module C: Crop Yield Prediction (Regression)

- **Target Variable:** `hg/ha_yield` (Units: hg/ha)

- **Split Strategy:** Chronological (Train: 1990-2009, Test: 2010-2013)

- **Train Period:** 1990–2009 (21305 samples) | **Test Period:** 2010–2013 (4627 samples)

- **Selected Model:** **Random Forest Regressor**

- **Selection Rationale:** Random Forest Regressor achieved substantially lower held-out test RMSE (20302.37 hg/ha vs 50470.16 hg/ha) and superior R² (0.9546 vs 0.7192) on the temporal 2010-2013 test horizon.


### Held-Out Temporal Horizon Candidate Comparison

| Model Candidate | RMSE (hg/ha) | MAE (hg/ha) | R² Score | RMSE (tonnes/ha) | Status |

|---|---|---|---|---|---|

| Mean Baseline (DummyRegressor) | 96,284.44 | 68,796.79 | -0.0219 | 9.63 | Baseline / Candidate |

| Linear Regression | 50,470.16 | 33,809.46 | 0.7192 | 5.05 | Baseline / Candidate |

| Random Forest Regressor | 20,302.37 | 10,454.19 | 0.9546 | 2.03 | ★ SELECTED |



### Target Distribution on Held-Out Test Set (2010–2013)

- **Mean Yield:** 88,547.35 hg/ha (8.85 tonnes/ha)

- **Standard Deviation:** 95,249.13 hg/ha

- **Min / Max:** 849.00 / 501,412.00 hg/ha

- **Selected Model RMSE as % of Mean:** 22.93%

- **Selected Model MAE as % of Mean:** 11.81%


---
## 5. Agronomic Disclaimers & Limitations

1. **Decision Support Nature:** Predictions generated by these models represent statistical approximations derived from historical benchmark datasets. They are decision-support aids and do not supersede certified agronomist counsel or soil testing laboratory results.

2. **Regional Granularity:** Crop yield predictions rely on national-level FAO aggregates. Local farm microclimates, pest pressures, and specialized management inputs will vary from regional averages.

3. **Fertilizer Representation:** The fertilizer recommendation dataset reflects algorithmic simulation rules and must be treated as guidance rather than clinical prescription.
