# DATA AUDIT REPORT
**Project:** Machine Learning Based Smart Agriculture Decision Support System  
**Audit Date:** October 2026  
**Auditor:** Senior ML Engineer & Software Architect  

---

## 1. Executive Summary

A comprehensive data audit was conducted on all dataset files located in the `dataset/` directory of the workspace. The audit evaluated file integrity, schemas, data types, missing values, duplicates, merge cardinalities, potential target leakage, and suitability for the three project modules:
1. **Module A — Crop Recommendation** (Multiclass Classification)
2. **Module B — Fertilizer Recommendation** (Multiclass Classification)
3. **Module C — Crop Yield Prediction** (Regression)

All source datasets in `dataset/` have been preserved without modification.

---

## 2. Inventory of Workspace Files

### 2.1 Non-Data Artifacts
- `Phase 1 Report Performa - Smart Agriculture Decision Support System.docx` (Project proposal documentation)
- `Smart_Agriculture_ML_Phase1_Presentation.pptx` (Project presentation slides)

### 2.2 Dataset Directory Structure
```
dataset/
├── Crop recommendation/
│   ├── Crop Reccomendation Dataset 2.csv  (150,034 bytes)
│   ├── Crop_recommendation 2.csv          (150,034 bytes)
│   └── Crop_recommendation.csv            (150,034 bytes)
├── Fertilizer Recommendation/
│   └── fertilizer_recommendation.csv      (1,138,691 bytes)
└── Yield predicition/
    ├── crop_yield.csv                     (1,620,945 bytes)
    ├── pesticides.csv                     (447,677 bytes)
    ├── rainfall.csv                       (136,712 bytes)
    ├── temp.csv                           (1,421,414 bytes)
    ├── yield.csv                          (4,042,934 bytes)
    └── yield_df.csv                       (1,565,376 bytes)
```

---

## 3. Module A: Crop Recommendation Dataset Audit

### 3.1 Files Examined
- `dataset/Crop recommendation/Crop Reccomendation Dataset 2.csv`
- `dataset/Crop recommendation/Crop_recommendation 2.csv`
- `dataset/Crop recommendation/Crop_recommendation.csv`

### 3.2 File Comparison & Deduplication
- **MD5 Checksum:** All 3 files produce the identical MD5 hash: `5e743dd4cf49f84d23a904cd51c9b5b8`.
- **Finding:** The three files are identical copies. `Crop_recommendation.csv` is selected as the canonical source.

### 3.3 Schema & Data Characteristics
- **Shape:** 2,200 rows × 8 columns
- **Missing Values:** 0 across all columns
- **Duplicate Rows:** 0 exact duplicates
- **Columns & Data Types:**
  - `N` (int64): Ratio of Nitrogen content in soil (range: 0 to 140 kg/ha, mean: 50.55)
  - `P` (int64): Ratio of Phosphorus content in soil (range: 5 to 145 kg/ha, mean: 53.36)
  - `K` (int64): Ratio of Potassium content in soil (range: 5 to 205 kg/ha, mean: 48.15)
  - `temperature` (float64): Ambient temperature in Celsius (range: 8.83°C to 43.68°C, mean: 25.62°C)
  - `humidity` (float64): Relative humidity in % (range: 14.26% to 99.98%, mean: 71.48%)
  - `ph` (float64): Soil pH value (range: 3.50 to 9.94, mean: 6.47)
  - `rainfall` (float64): Rainfall in mm (range: 20.21 mm to 298.56 mm, mean: 103.46 mm)
  - `label` (object): Crop recommendation target (22 unique classes)

### 3.4 Target Distribution
- Exactly 100 samples per class across all 22 classes (perfectly balanced 4.54% each):
  * Cereals/Grains: `rice`, `maize`
  * Pulses/Legumes: `chickpea`, `kidneybeans`, `pigeonpeas`, `mothbeans`, `mungbean`, `blackgram`, `lentil`
  * Fruits: `pomegranate`, `banana`, `mango`, `grapes`, `watermelon`, `muskmelon`, `apple`, `orange`, `papaya`, `coconut`
  * Commercial crops: `cotton`, `jute`, `coffee`

### 3.5 Validation & Preprocessing Recommendations
- Stratified 80:20 train-test split (`random_state=42`) preserves exactly 20 test samples per crop.
- Features are strictly bounded within sensible physiological ranges; standard scaling is appropriate for distance/gradient-based models (Logistic Regression).

---

## 4. Module B: Fertilizer Recommendation Dataset Audit

### 4.1 File Examined
- `dataset/Fertilizer Recommendation/fertilizer_recommendation.csv`

### 4.2 Schema & Data Characteristics
- **Shape:** 10,000 rows × 20 columns
- **Missing Values:** 0 across all columns
- **Duplicate Rows:** 0 exact duplicates
- **Target Column:** `Recommended_Fertilizer` (object, 7 unique classes)
- **Features Breakdown:**
  - **Numeric Features (12):**
    - `Soil_pH` (float64): 4.50 to 8.50
    - `Soil_Moisture` (float64): 10.00% to 60.00%
    - `Organic_Carbon` (float64): 0.20% to 1.50%
    - `Electrical_Conductivity` (float64): 0.10 to 3.00 dS/m
    - `Nitrogen_Level` (int64): 20 to 159 kg/ha
    - `Phosphorus_Level` (int64): 10 to 89 kg/ha
    - `Potassium_Level` (int64): 10 to 119 kg/ha
    - `Temperature` (float64): 10.00°C to 40.00°C
    - `Humidity` (float64): 30.01% to 89.99%
    - `Rainfall` (float64): 200.08 to 2999.98 mm
    - `Fertilizer_Used_Last_Season` (float64): 50.01 to 300.00 kg/ha
    - `Yield_Last_Season` (float64): 1.00 to 8.00 tonnes/ha
  - **Categorical Features (7):**
    - `Soil_Type` (4 levels): Clay, Loamy, Sandy, Silt
    - `Crop_Type` (7 levels): Cotton, Maize, Potato, Rice, Sugarcane, Tomato, Wheat
    - `Crop_Growth_Stage` (4 levels): Sowing, Vegetative, Flowering, Harvest
    - `Season` (3 levels): Kharif, Rabi, Zaid
    - `Irrigation_Type` (4 levels): Canal, Drip, Rainfed, Sprinkler
    - `Previous_Crop` (7 levels): Cotton, Maize, Potato, Rice, Sugarcane, Tomato, Wheat
    - `Region` (5 levels): Central, East, North, South, West

### 4.3 Target Distribution & Class Imbalance
| Fertilizer Class | Sample Count | Percentage | Imbalance Status |
|---|---|---|---|
| Urea | 3,101 | 31.01% | Majority class |
| DAP | 2,920 | 29.20% | Majority class |
| MOP | 1,408 | 14.08% | Moderate |
| Compost | 996 | 9.96% | Moderate |
| Zinc Sulphate | 752 | 7.52% | Minor |
| NPK | 641 | 6.41% | Minor |
| SSP | 182 | 1.82% | **Rare class** |

### 4.4 Data Leakage & Agronomic Semantics
- **No Direct Leakage:** There are no row IDs or current-season post-outcome fields. `Yield_Last_Season` and `Fertilizer_Used_Last_Season` are historical antecedent measurements available prior to the recommendation decision.
- **Rule-Engine Archetype:** Feature-to-target relationship analysis reveals deterministic decision boundaries:
  - Urea is triggered when `Nitrogen_Level` is deficient (< 50 kg/ha).
  - DAP is triggered when `Phosphorus_Level` is deficient (< 35 kg/ha).
  - MOP is triggered when `Potassium_Level` is deficient (< 40 kg/ha).
  - Compost is recommended under acidic soils (low pH ~5.3).
  - Zinc Sulphate is recommended under alkaline soils (high pH ~7.7).
  - NPK is concentrated during the Vegetative stage (453 / 641 records).
- **Modeling Implications:** Models must account for severe class imbalance on `SSP` (1.82%). Cost-sensitive weighting (`class_weight='balanced'`) and stratified 80:20 partitioning (`random_state=42`) are strictly required.
- **Agronomic Disclaimer:** The dataset reflects synthetic heuristic generation; predictions must be explicitly framed as ML decision-support suggestions rather than certified laboratory prescriptions.

---

## 5. Module C: Crop Yield Prediction Dataset Audit

### 5.1 Datasets Located in `dataset/Yield predicition/`
1. `yield_df.csv` (28,242 rows × 8 columns) — Pre-merged FAO global crop yield dataset.
2. `yield.csv` (56,717 rows × 12 columns) — FAOSTAT raw crop production & yield.
3. `rainfall.csv` (6,727 rows × 3 columns) — FAOSTAT raw rainfall records.
4. `pesticides.csv` (4,349 rows × 7 columns) — FAOSTAT raw pesticide application records.
5. `temp.csv` (71,311 rows × 3 columns) — Historical surface temperature records.
6. `crop_yield.csv` (19,689 rows × 10 columns) — Regional Indian agricultural dataset.

### 5.2 Deep Investigation of `crop_yield.csv` vs `yield_df.csv`
- **`crop_yield.csv`:** Contains `['Crop', 'Crop_Year', 'Season', 'State', 'Area', 'Production', 'Annual_Rainfall', 'Fertilizer', 'Pesticide', 'Yield']`.
  - **Severe Target Leakage Warning:** In this dataset, `Production` is total harvested tonnage and `Area` is harvested hectares. Because $\text{Yield} \equiv \frac{\text{Production}}{\text{Area}}$, including `Production` as an input feature gives $R^2 \approx 1.0$ through trivial arithmetic identity.
  - Furthermore, `crop_yield.csv` does not match the prompt's specified schema (`hg/ha_yield`, `Item`, `average_rain_fall_mm_per_year`).
- **`yield_df.csv`:** Matches the prompt's specified schema, features, and target units (`hg/ha_yield`).

### 5.3 Investigation of Repeated Area–Item–Year Combinations
Analysis of `yield_df.csv` revealed the following critical findings:
1. **Total Rows:** 28,242 rows.
2. **Exact Duplicate Rows:** 2,310 rows are identical across all feature and target columns (excluding the serial column `Unnamed: 0`).
3. **Area–Item–Year Group Cardinality:** There are 15,112 duplicate entries on `[Area, Item, Year]` across 13,130 unique groups.
4. **Root Cause Analysis via Component Merging:**
   - In `yield.csv`, `[Area, Item, Year]` combinations are strictly unique (0 duplicates).
   - In `rainfall.csv` and `pesticides.csv`, `[Area, Year]` keys are unique (0 duplicates).
   - In `temp.csv`, there are **42,797 duplicate `[country, year]` entries**! `temp.csv` aggregates multiple regional weather stations and city temperature logs per country without recording station identifiers.
   - When the creator merged `yield.csv` with `temp.csv` on `[country, year]`, a 1-to-many Cartesian multiplication occurred, replicating each crop yield observation across all temperature stations.
5. **Variance within Area–Item–Year Groups:**
   - `hg/ha_yield` distinct count per group = **1** (Zero variance).
   - `average_rain_fall_mm_per_year` distinct count = **1** (Zero variance).
   - `pesticides_tonnes` distinct count = **1** (Zero variance).
   - `avg_temp` distinct count = up to **19** distinct station temperatures.
6. **Data Preparation Action:**
   - Exact duplicate rows (2,310) must be purged to prevent identical observations from leaking between train and test splits.
   - For modeling, candidate models are evaluated on the deduplicated dataset (25,932 records) and on the aggregated station-averaged dataset (13,130 records) with documented comparative metrics.

### 5.4 Chronological Split & Unseen Category Analysis
- **Temporal Coverage:** 1990 through 2013 (24 years).
- **Split Boundary:**
  - Training Period: 1990 to 2009 (20 years, 82.2% of deduplicated data; 21,305 rows).
  - Test Period: 2010 to 2013 (4 years, 17.8% of deduplicated data; 4,627 rows).
- **Unseen Level Risk:**
  - `Items` (Crops): 100% overlap between train and test periods (0 unseen crops).
  - `Area` (Countries): The country `'Sudan'` appears in the test period (2010–2013) but was not recorded under that country identifier prior to 2010 in FAOSTAT.
  - **Mitigation:** Categorical encoding in scikit-learn must use `OneHotEncoder(handle_unknown='ignore')` so that novel countries are safely transformed without throwing runtime exceptions.
- **Unit Verification:**
  - Target is `hg/ha_yield` (hectograms per hectare).
  - Conversion: $1 \text{ hg} = 0.1 \text{ kg} = 10^{-4} \text{ metric tonnes}$. Therefore, $\text{tonnes/ha} = \frac{\text{hg/ha}}{10,000}$.
  - Target range: 50 to 501,412 hg/ha (0.005 to 50.14 tonnes/ha), which aligns with global tuber and cereal agronomic yields.

---

## 6. Synthesis and Modeling Roadmap

| Module | Canonical Dataset | Target Variable | Type | Train/Test Split | Selected Metrics |
|---|---|---|---|---|---|
| **Module A: Crop** | `dataset/Crop recommendation/Crop_recommendation.csv` | `label` | Multiclass (22 classes) | 80:20 Stratified (`random_state=42`) | Macro-F1 (primary), Accuracy |
| **Module B: Fertilizer** | `dataset/Fertilizer Recommendation/fertilizer_recommendation.csv` | `Recommended_Fertilizer` | Multiclass (7 classes) | 80:20 Stratified (`random_state=42`) | Macro-F1 (primary), Accuracy |
| **Module C: Yield** | `dataset/Yield predicition/yield_df.csv` (deduplicated) | `hg/ha_yield` | Regression | Chronological (Train ≤ 2009, Test ≥ 2010) | RMSE (primary), MAE, $R^2$ |

All modeling scripts will strictly load from verified paths, preserve original files, fit transformers exclusively on training data, and export reproducible artifacts and evaluation metrics to `models/` and `reports/`.
