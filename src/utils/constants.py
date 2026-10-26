"""Constants and configuration for AgriSmart."""

from pathlib import Path

# Base Paths
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DATASET_DIR = WORKSPACE_ROOT / "dataset"
MODELS_DIR = WORKSPACE_ROOT / "models"
REPORTS_DIR = WORKSPACE_ROOT / "reports"

# Canonical Dataset Paths
CROP_DATA_PATH = DATASET_DIR / "Crop recommendation" / "Crop_recommendation.csv"
FERT_DATA_PATH = DATASET_DIR / "Fertilizer Recommendation" / "fertilizer_recommendation.csv"
YIELD_DATA_PATH = DATASET_DIR / "Yield predicition" / "yield_df.csv"
CROP_YIELD_ALT_PATH = DATASET_DIR / "Yield predicition" / "crop_yield.csv"

# Module A: Crop Recommendation Constants
CROP_FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
CROP_TARGET = "label"

CROP_FEATURE_RANGES = {
    "N": {"min": 0.0, "max": 140.0, "default": 50.0, "unit": "kg/ha", "label": "Nitrogen (N)"},
    "P": {"min": 5.0, "max": 145.0, "default": 53.0, "unit": "kg/ha", "label": "Phosphorus (P)"},
    "K": {"min": 5.0, "max": 205.0, "default": 48.0, "unit": "kg/ha", "label": "Potassium (K)"},
    "temperature": {"min": 8.0, "max": 45.0, "default": 25.0, "unit": "°C", "label": "Temperature"},
    "humidity": {"min": 14.0, "max": 100.0, "default": 71.0, "unit": "%", "label": "Relative Humidity"},
    "ph": {"min": 3.5, "max": 10.0, "default": 6.5, "unit": "pH", "label": "Soil pH"},
    "rainfall": {"min": 20.0, "max": 300.0, "default": 100.0, "unit": "mm", "label": "Rainfall"},
}

CROP_DESCRIPTIONS = {
    "rice": "Staple cereal crop thriving in submerged paddy soils, warm temperatures, and high humidity.",
    "maize": "Versatile warm-season cereal requiring moderate rainfall and well-drained fertile soils.",
    "chickpea": "Cool-season leguminous pulse thriving on residual soil moisture and moderate phosphorus.",
    "kidneybeans": "Nutrient-rich pulse requiring mild temperatures and moderate soil fertility.",
    "pigeonpeas": "Drought-tolerant leguminous pulse with deep taproots suitable for semi-arid zones.",
    "mothbeans": "Extremely drought-resilient arid pulse requiring minimal rainfall.",
    "mungbean": "Short-duration leguminous crop improving soil nitrogen content via rhizobial fixation.",
    "blackgram": "Tropical pulse requiring warm climate and fertile loam/clay loam soil.",
    "lentil": "Cool-season legume preferring well-drained loam and moderate potassium levels.",
    "pomegranate": "Subtropical arid fruit shrub requiring dry seasons and neutral to slightly alkaline soil.",
    "banana": "High-potassium demanding tropical fruit requiring abundant warmth, moisture, and humus.",
    "mango": "Deep-rooted tropical fruit requiring warm weather and well-drained alluvial soil.",
    "grapes": "High potassium-demanding vine requiring temperate warm days and low humidity during ripening.",
    "watermelon": "Warm-season fruit vine thriving in sandy loam soils and warm dry climates.",
    "muskmelon": "Warm-season cucurbit fruit demanding sandy well-drained soil and plentiful sunshine.",
    "apple": "Temperate tree fruit requiring cool winter chilling hours and moist fertile soils.",
    "orange": "Citrus fruit requiring well-drained soil, moderate warmth, and balanced NPK nutrition.",
    "papaya": "Fast-growing tropical fruit requiring warm temperatures, high humidity, and fertile soil.",
    "coconut": "Coastal tropical palm requiring high humidity, plentiful rainfall, and sandy loam.",
    "cotton": "Warm-season commercial fiber crop demanding high sunshine, warmth, and moderate rainfall.",
    "jute": "Commercial bast fiber requiring warm, humid tropical conditions and heavy seasonal rainfall.",
    "coffee": "Shade-tolerant plantation crop thriving in highland tropical soils with high rainfall.",
}

# Module B: Fertilizer Recommendation Constants
FERT_NUM_FEATURES = [
    "Soil_pH",
    "Soil_Moisture",
    "Organic_Carbon",
    "Electrical_Conductivity",
    "Nitrogen_Level",
    "Phosphorus_Level",
    "Potassium_Level",
    "Temperature",
    "Humidity",
    "Rainfall",
    "Fertilizer_Used_Last_Season",
    "Yield_Last_Season",
]

FERT_CAT_FEATURES = [
    "Soil_Type",
    "Crop_Type",
    "Crop_Growth_Stage",
    "Season",
    "Irrigation_Type",
    "Previous_Crop",
    "Region",
]

FERT_TARGET = "Recommended_Fertilizer"

FERT_CATEGORIES = {
    "Soil_Type": ["Clay", "Loamy", "Sandy", "Silt"],
    "Crop_Type": ["Cotton", "Maize", "Potato", "Rice", "Sugarcane", "Tomato", "Wheat"],
    "Crop_Growth_Stage": ["Sowing", "Vegetative", "Flowering", "Harvest"],
    "Season": ["Kharif", "Rabi", "Zaid"],
    "Irrigation_Type": ["Canal", "Drip", "Rainfed", "Sprinkler"],
    "Previous_Crop": ["Cotton", "Maize", "Potato", "Rice", "Sugarcane", "Tomato", "Wheat"],
    "Region": ["Central", "East", "North", "South", "West"],
}

FERT_FEATURE_RANGES = {
    "Soil_pH": {"min": 4.5, "max": 8.5, "default": 6.5, "unit": "pH", "label": "Soil pH"},
    "Soil_Moisture": {"min": 10.0, "max": 60.0, "default": 35.0, "unit": "%", "label": "Soil Moisture"},
    "Organic_Carbon": {"min": 0.2, "max": 1.5, "default": 0.85, "unit": "%", "label": "Organic Carbon"},
    "Electrical_Conductivity": {"min": 0.1, "max": 3.0, "default": 1.5, "unit": "dS/m", "label": "Electrical Conductivity"},
    "Nitrogen_Level": {"min": 20.0, "max": 160.0, "default": 108.0, "unit": "kg/ha", "label": "Soil Nitrogen Level"},
    "Phosphorus_Level": {"min": 10.0, "max": 90.0, "default": 64.0, "unit": "kg/ha", "label": "Soil Phosphorus Level"},
    "Potassium_Level": {"min": 10.0, "max": 120.0, "default": 78.0, "unit": "kg/ha", "label": "Soil Potassium Level"},
    "Temperature": {"min": 10.0, "max": 40.0, "default": 25.0, "unit": "°C", "label": "Temperature"},
    "Humidity": {"min": 30.0, "max": 90.0, "default": 60.0, "unit": "%", "label": "Humidity"},
    "Rainfall": {"min": 200.0, "max": 3000.0, "default": 1580.0, "unit": "mm", "label": "Annual Rainfall"},
    "Fertilizer_Used_Last_Season": {"min": 50.0, "max": 300.0, "default": 175.0, "unit": "kg/ha", "label": "Fertilizer Used Last Season"},
    "Yield_Last_Season": {"min": 1.0, "max": 8.0, "default": 4.5, "unit": "tonnes/ha", "label": "Yield Last Season"},
}

FERT_DESCRIPTIONS = {
    "Urea": "High-nitrogen synthetic fertilizer (46-0-0) applied to address nitrogen deficits during rapid vegetative growth.",
    "DAP": "Diammonium Phosphate (18-46-0) providing accessible phosphorus and starter nitrogen for root development and seedling establishment.",
    "MOP": "Muriate of Potash / Potassium Chloride (0-0-60) providing potassium for drought tolerance, stomatal control, and disease resistance.",
    "NPK": "Complete balanced fertilizer supplying primary macronutrients (Nitrogen, Phosphorus, Potassium) in harmonized ratios.",
    "Compost": "Organic matter improving soil structure, water holding capacity, and cation exchange in degraded or acidic soils.",
    "Zinc Sulphate": "Micronutrient formulation providing zinc and sulfur to alleviate chlorosis, particularly in alkaline soils.",
    "SSP": "Single Super Phosphate (0-16-0 + 12% S + 20% Ca) delivering phosphorus alongside essential sulfur and calcium.",
}

# Module C: Crop Yield Prediction Constants
YIELD_NUM_FEATURES = ["Year", "average_rain_fall_mm_per_year", "pesticides_tonnes", "avg_temp"]
YIELD_CAT_FEATURES = ["Area", "Item"]
YIELD_ALL_FEATURES = YIELD_CAT_FEATURES + YIELD_NUM_FEATURES
YIELD_TARGET = "hg/ha_yield"

# Conversion constant: 1 hg = 0.1 kg = 0.0001 tonnes
HG_PER_HA_TO_TONNES_PER_HA = 1.0 / 10000.0

YIELD_FEATURE_RANGES = {
    "Year": {"min": 1990, "max": 2030, "default": 2013, "unit": "year", "label": "Harvest Year"},
    "average_rain_fall_mm_per_year": {"min": 50.0, "max": 3300.0, "default": 1100.0, "unit": "mm/year", "label": "Average Annual Rainfall"},
    "pesticides_tonnes": {"min": 0.0, "max": 370000.0, "default": 25000.0, "unit": "tonnes", "label": "Pesticide Usage"},
    "avg_temp": {"min": 1.0, "max": 32.0, "default": 17.5, "unit": "°C", "label": "Average Temperature"},
}

# Agronomic Disclaimers
AGRONOMIC_DISCLAIMER_CROP = (
    "Model recommendations are purely predictive statistical suggestions based on historical training data. "
    "They do not replace comprehensive local soil tests, certified agronomist counsel, or official extension services."
)

AGRONOMIC_DISCLAIMER_FERT = (
    "Fertilizer recommendations represent machine learning estimations derived from historical patterns. "
    "Fertilizer selection for actual farms must be verified through certified soil health card analysis and qualified agronomic consultation."
)

AGRONOMIC_DISCLAIMER_YIELD = (
    "Predicted yields reflect historical FAO macroeconomic country-level aggregates. Local microclimates, farm management, "
    "pest outbreaks, and irrigation practices cause significant variance at the individual farm parcel scale."
)
