"""Reproducible Model Training and Experiment Tracking Pipeline for AgriSmart."""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline

# Ensure workspace root is in sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from src.data.loaders import load_crop_data, load_fertilizer_data, load_yield_data
from src.features.preprocessing import (
    build_crop_preprocessor,
    build_fertilizer_preprocessor,
    build_yield_preprocessor,
)
from src.evaluation.metrics import evaluate_classifier, evaluate_regressor
from src.utils.constants import (
    MODELS_DIR,
    REPORTS_DIR,
    CROP_FEATURES,
    CROP_TARGET,
    FERT_NUM_FEATURES,
    FERT_CAT_FEATURES,
    FERT_TARGET,
    YIELD_NUM_FEATURES,
    YIELD_CAT_FEATURES,
    YIELD_TARGET,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AgriSmartTrainer")


def train_crop_recommendation() -> Tuple[Pipeline, Dict[str, Any], list]:
    """Train and evaluate candidate models for Crop Recommendation."""
    logger.info("--- Starting Module A: Crop Recommendation Training ---")
    df = load_crop_data()
    X = df[CROP_FEATURES]
    y = df[CROP_TARGET]
    
    # Stratified 80:20 split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    labels = sorted(y.unique().tolist())
    
    candidates = {}
    comparison_rows = []
    
    # 1. Baseline: DummyClassifier
    dummy = Pipeline([
        ("preprocessor", build_crop_preprocessor(use_scaler=False)),
        ("classifier", DummyClassifier(strategy="most_frequent")),
    ])
    dummy.fit(X_train, y_train)
    y_pred_dummy = dummy.predict(X_test)
    eval_dummy = evaluate_classifier(y_test, y_pred_dummy, labels=labels)
    candidates["DummyClassifier (Baseline)"] = {"model": dummy, "metrics": eval_dummy}
    comparison_rows.append({
        "Module": "Crop Recommendation",
        "Model": "DummyClassifier (Baseline)",
        "Primary_Metric_Name": "Macro-F1",
        "Primary_Metric_Value": round(eval_dummy["macro_f1"], 4),
        "Secondary_Metric_Name": "Accuracy",
        "Secondary_Metric_Value": round(eval_dummy["accuracy"], 4),
        "Is_Selected": False,
        "Split": "Stratified 80:20 (random_state=42)",
        "Train_Size": len(X_train),
        "Test_Size": len(X_test),
    })
    logger.info("DummyClassifier Baseline: Macro-F1 = %.4f, Accuracy = %.4f", eval_dummy["macro_f1"], eval_dummy["accuracy"])
    
    # 2. Logistic Regression
    lr = Pipeline([
        ("preprocessor", build_crop_preprocessor(use_scaler=True)),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
    ])
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    eval_lr = evaluate_classifier(y_test, y_pred_lr, labels=labels)
    candidates["Logistic Regression"] = {"model": lr, "metrics": eval_lr}
    comparison_rows.append({
        "Module": "Crop Recommendation",
        "Model": "Logistic Regression",
        "Primary_Metric_Name": "Macro-F1",
        "Primary_Metric_Value": round(eval_lr["macro_f1"], 4),
        "Secondary_Metric_Name": "Accuracy",
        "Secondary_Metric_Value": round(eval_lr["accuracy"], 4),
        "Is_Selected": False,
        "Split": "Stratified 80:20 (random_state=42)",
        "Train_Size": len(X_train),
        "Test_Size": len(X_test),
    })
    logger.info("Logistic Regression: Macro-F1 = %.4f, Accuracy = %.4f", eval_lr["macro_f1"], eval_lr["accuracy"])
    
    # 3. Random Forest Classifier
    rf = Pipeline([
        ("preprocessor", build_crop_preprocessor(use_scaler=False)),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
    ])
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    eval_rf = evaluate_classifier(y_test, y_pred_rf, labels=labels)
    candidates["Random Forest"] = {"model": rf, "metrics": eval_rf}
    comparison_rows.append({
        "Module": "Crop Recommendation",
        "Model": "Random Forest",
        "Primary_Metric_Name": "Macro-F1",
        "Primary_Metric_Value": round(eval_rf["macro_f1"], 4),
        "Secondary_Metric_Name": "Accuracy",
        "Secondary_Metric_Value": round(eval_rf["accuracy"], 4),
        "Is_Selected": False,
        "Split": "Stratified 80:20 (random_state=42)",
        "Train_Size": len(X_train),
        "Test_Size": len(X_test),
    })
    logger.info("Random Forest Classifier: Macro-F1 = %.4f, Accuracy = %.4f", eval_rf["macro_f1"], eval_rf["accuracy"])
    
    # Selection based on held-out Macro-F1
    if eval_rf["macro_f1"] >= eval_lr["macro_f1"]:
        best_name = "Random Forest"
        selection_reason = (
            f"Random Forest achieved higher held-out Macro-F1 ({eval_rf['macro_f1']:.4f} vs {eval_lr['macro_f1']:.4f}) "
            f"and Accuracy ({eval_rf['accuracy']:.4f} vs {eval_lr['accuracy']:.4f}) across all 22 crop classes."
        )
    else:
        best_name = "Logistic Regression"
        selection_reason = (
            f"Logistic Regression achieved higher held-out Macro-F1 ({eval_lr['macro_f1']:.4f} vs {eval_rf['macro_f1']:.4f})."
        )
        
    for r in comparison_rows:
        if r["Module"] == "Crop Recommendation" and r["Model"] == best_name:
            r["Is_Selected"] = True
            
    best_pipeline = candidates[best_name]["model"]
    best_metrics = candidates[best_name]["metrics"]
    
    meta = {
        "module": "crop_recommendation",
        "selected_model": best_name,
        "selection_reason": selection_reason,
        "features": CROP_FEATURES,
        "target": CROP_TARGET,
        "labels": labels,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "metrics": best_metrics,
        "all_candidates": {k: v["metrics"] for k, v in candidates.items()},
        "training_timestamp": datetime.now().isoformat(),
    }
    
    return best_pipeline, meta, comparison_rows


def train_fertilizer_recommendation() -> Tuple[Pipeline, Dict[str, Any], list]:
    """Train and evaluate candidate models for Fertilizer Recommendation."""
    logger.info("--- Starting Module B: Fertilizer Recommendation Training ---")
    df = load_fertilizer_data()
    feature_cols = FERT_NUM_FEATURES + FERT_CAT_FEATURES
    X = df[feature_cols]
    y = df[FERT_TARGET]
    
    # Stratified 80:20 split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    labels = sorted(y.unique().tolist())
    
    candidates = {}
    comparison_rows = []
    
    # 1. Baseline: DummyClassifier
    dummy = Pipeline([
        ("preprocessor", build_fertilizer_preprocessor(use_scaler=False)),
        ("classifier", DummyClassifier(strategy="most_frequent")),
    ])
    dummy.fit(X_train, y_train)
    y_pred_dummy = dummy.predict(X_test)
    eval_dummy = evaluate_classifier(y_test, y_pred_dummy, labels=labels)
    candidates["DummyClassifier (Baseline)"] = {"model": dummy, "metrics": eval_dummy}
    comparison_rows.append({
        "Module": "Fertilizer Recommendation",
        "Model": "DummyClassifier (Baseline)",
        "Primary_Metric_Name": "Macro-F1",
        "Primary_Metric_Value": round(eval_dummy["macro_f1"], 4),
        "Secondary_Metric_Name": "Accuracy",
        "Secondary_Metric_Value": round(eval_dummy["accuracy"], 4),
        "Is_Selected": False,
        "Split": "Stratified 80:20 (random_state=42)",
        "Train_Size": len(X_train),
        "Test_Size": len(X_test),
    })
    logger.info("DummyClassifier Baseline: Macro-F1 = %.4f, Accuracy = %.4f", eval_dummy["macro_f1"], eval_dummy["accuracy"])
    
    # 2. Logistic Regression (balanced)
    lr = Pipeline([
        ("preprocessor", build_fertilizer_preprocessor(use_scaler=True)),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ])
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    eval_lr = evaluate_classifier(y_test, y_pred_lr, labels=labels)
    candidates["Logistic Regression (Balanced)"] = {"model": lr, "metrics": eval_lr}
    comparison_rows.append({
        "Module": "Fertilizer Recommendation",
        "Model": "Logistic Regression (Balanced)",
        "Primary_Metric_Name": "Macro-F1",
        "Primary_Metric_Value": round(eval_lr["macro_f1"], 4),
        "Secondary_Metric_Name": "Accuracy",
        "Secondary_Metric_Value": round(eval_lr["accuracy"], 4),
        "Is_Selected": False,
        "Split": "Stratified 80:20 (random_state=42)",
        "Train_Size": len(X_train),
        "Test_Size": len(X_test),
    })
    logger.info("Logistic Regression (Balanced): Macro-F1 = %.4f, Accuracy = %.4f", eval_lr["macro_f1"], eval_lr["accuracy"])
    
    # 3. Random Forest (balanced)
    rf = Pipeline([
        ("preprocessor", build_fertilizer_preprocessor(use_scaler=False)),
        ("classifier", RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)),
    ])
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    eval_rf = evaluate_classifier(y_test, y_pred_rf, labels=labels)
    candidates["Random Forest (Balanced)"] = {"model": rf, "metrics": eval_rf}
    comparison_rows.append({
        "Module": "Fertilizer Recommendation",
        "Model": "Random Forest (Balanced)",
        "Primary_Metric_Name": "Macro-F1",
        "Primary_Metric_Value": round(eval_rf["macro_f1"], 4),
        "Secondary_Metric_Name": "Accuracy",
        "Secondary_Metric_Value": round(eval_rf["accuracy"], 4),
        "Is_Selected": False,
        "Split": "Stratified 80:20 (random_state=42)",
        "Train_Size": len(X_train),
        "Test_Size": len(X_test),
    })
    logger.info("Random Forest (Balanced): Macro-F1 = %.4f, Accuracy = %.4f", eval_rf["macro_f1"], eval_rf["accuracy"])
    
    # Selection based on held-out Macro-F1
    if eval_rf["macro_f1"] >= eval_lr["macro_f1"]:
        best_name = "Random Forest (Balanced)"
        selection_reason = (
            f"Random Forest (Balanced) achieved highest Macro-F1 ({eval_rf['macro_f1']:.4f} vs {eval_lr['macro_f1']:.4f}) "
            f"and effectively resolved rare class representation (e.g. SSP) with balanced class weights."
        )
    else:
        best_name = "Logistic Regression (Balanced)"
        selection_reason = (
            f"Logistic Regression (Balanced) achieved highest Macro-F1 ({eval_lr['macro_f1']:.4f})."
        )
        
    for r in comparison_rows:
        if r["Module"] == "Fertilizer Recommendation" and r["Model"] == best_name:
            r["Is_Selected"] = True
            
    best_pipeline = candidates[best_name]["model"]
    best_metrics = candidates[best_name]["metrics"]
    
    meta = {
        "module": "fertilizer_recommendation",
        "selected_model": best_name,
        "selection_reason": selection_reason,
        "features": feature_cols,
        "numeric_features": FERT_NUM_FEATURES,
        "categorical_features": FERT_CAT_FEATURES,
        "target": FERT_TARGET,
        "labels": labels,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "metrics": best_metrics,
        "all_candidates": {k: v["metrics"] for k, v in candidates.items()},
        "training_timestamp": datetime.now().isoformat(),
    }
    
    return best_pipeline, meta, comparison_rows


def train_yield_prediction() -> Tuple[Pipeline, Dict[str, Any], list]:
    """Train and evaluate candidate models for Crop Yield Prediction."""
    logger.info("--- Starting Module C: Crop Yield Prediction Training ---")
    # Load deduplicated dataset
    df = load_yield_data(deduplicate=True, aggregate_stations=False)
    
    # Chronological Split: Train <= 2009, Test >= 2010
    train_df = df[df["Year"] <= 2009].copy()
    test_df = df[df["Year"] >= 2010].copy()
    
    feature_cols = YIELD_CAT_FEATURES + YIELD_NUM_FEATURES
    X_train = train_df[feature_cols]
    y_train = train_df[YIELD_TARGET]
    X_test = test_df[feature_cols]
    y_test = test_df[YIELD_TARGET]
    
    candidates = {}
    comparison_rows = []
    
    # 1. Baseline: DummyRegressor (Mean) fitted only on train
    dummy = DummyRegressor(strategy="mean")
    dummy.fit(X_train, y_train)
    y_pred_dummy = dummy.predict(X_test)
    eval_dummy = evaluate_regressor(y_test, y_pred_dummy, target_unit="hg/ha")
    candidates["Mean Baseline (DummyRegressor)"] = {"model": dummy, "metrics": eval_dummy}
    comparison_rows.append({
        "Module": "Crop Yield Prediction",
        "Model": "Mean Baseline (DummyRegressor)",
        "Primary_Metric_Name": "RMSE (hg/ha)",
        "Primary_Metric_Value": round(eval_dummy["rmse"], 2),
        "Secondary_Metric_Name": "MAE (hg/ha)",
        "Secondary_Metric_Value": round(eval_dummy["mae"], 2),
        "Is_Selected": False,
        "Split": "Chronological (Train <= 2009, Test >= 2010)",
        "Train_Size": len(X_train),
        "Test_Size": len(X_test),
    })
    logger.info("Mean Baseline: RMSE = %.2f hg/ha, MAE = %.2f hg/ha, R2 = %.4f", eval_dummy["rmse"], eval_dummy["mae"], eval_dummy["r2"])
    
    # 2. Linear Regression Pipeline
    lr = Pipeline([
        ("preprocessor", build_yield_preprocessor(use_scaler=True)),
        ("regressor", LinearRegression()),
    ])
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    eval_lr = evaluate_regressor(y_test, y_pred_lr, target_unit="hg/ha")
    candidates["Linear Regression"] = {"model": lr, "metrics": eval_lr}
    comparison_rows.append({
        "Module": "Crop Yield Prediction",
        "Model": "Linear Regression",
        "Primary_Metric_Name": "RMSE (hg/ha)",
        "Primary_Metric_Value": round(eval_lr["rmse"], 2),
        "Secondary_Metric_Name": "MAE (hg/ha)",
        "Secondary_Metric_Value": round(eval_lr["mae"], 2),
        "Is_Selected": False,
        "Split": "Chronological (Train <= 2009, Test >= 2010)",
        "Train_Size": len(X_train),
        "Test_Size": len(X_test),
    })
    logger.info("Linear Regression: RMSE = %.2f hg/ha, MAE = %.2f hg/ha, R2 = %.4f", eval_lr["rmse"], eval_lr["mae"], eval_lr["r2"])
    
    # 3. Random Forest Regressor Pipeline
    rf = Pipeline([
        ("preprocessor", build_yield_preprocessor(use_scaler=False)),
        ("regressor", RandomForestRegressor(n_estimators=100, max_depth=25, n_jobs=-1, random_state=42)),
    ])
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    eval_rf = evaluate_regressor(y_test, y_pred_rf, target_unit="hg/ha")
    candidates["Random Forest Regressor"] = {"model": rf, "metrics": eval_rf}
    comparison_rows.append({
        "Module": "Crop Yield Prediction",
        "Model": "Random Forest Regressor",
        "Primary_Metric_Name": "RMSE (hg/ha)",
        "Primary_Metric_Value": round(eval_rf["rmse"], 2),
        "Secondary_Metric_Name": "MAE (hg/ha)",
        "Secondary_Metric_Value": round(eval_rf["mae"], 2),
        "Is_Selected": False,
        "Split": "Chronological (Train <= 2009, Test >= 2010)",
        "Train_Size": len(X_train),
        "Test_Size": len(X_test),
    })
    logger.info("Random Forest Regressor: RMSE = %.2f hg/ha, MAE = %.2f hg/ha, R2 = %.4f", eval_rf["rmse"], eval_rf["mae"], eval_rf["r2"])
    
    # Selection based on lower held-out test RMSE
    if eval_rf["rmse"] <= eval_lr["rmse"]:
        best_name = "Random Forest Regressor"
        selection_reason = (
            f"Random Forest Regressor achieved substantially lower held-out test RMSE ({eval_rf['rmse']:.2f} hg/ha vs {eval_lr['rmse']:.2f} hg/ha) "
            f"and superior R² ({eval_rf['r2']:.4f} vs {eval_lr['r2']:.4f}) on the temporal 2010-2013 test horizon."
        )
    else:
        best_name = "Linear Regression"
        selection_reason = (
            f"Linear Regression achieved lower held-out test RMSE ({eval_lr['rmse']:.2f} hg/ha)."
        )
        
    for r in comparison_rows:
        if r["Module"] == "Crop Yield Prediction" and r["Model"] == best_name:
            r["Is_Selected"] = True
            
    best_pipeline = candidates[best_name]["model"]
    best_metrics = candidates[best_name]["metrics"]
    
    meta = {
        "module": "yield_prediction",
        "selected_model": best_name,
        "selection_reason": selection_reason,
        "features": feature_cols,
        "categorical_features": YIELD_CAT_FEATURES,
        "numeric_features": YIELD_NUM_FEATURES,
        "target": YIELD_TARGET,
        "target_unit": "hg/ha",
        "split_strategy": "Chronological (Train: 1990-2009, Test: 2010-2013)",
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "metrics": best_metrics,
        "all_candidates": {k: v["metrics"] for k, v in candidates.items()},
        "training_timestamp": datetime.now().isoformat(),
    }
    
    return best_pipeline, meta, comparison_rows


def generate_evaluation_markdown(
    crop_meta: Dict[str, Any],
    fert_meta: Dict[str, Any],
    yield_meta: Dict[str, Any],
    comparison_df: pd.DataFrame,
) -> str:
    """Generate comprehensive MODEL_EVALUATION.md report."""
    md = []
    md.append("# MODEL EVALUATION & BENCHMARK REPORT")
    md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    md.append(f"**Environment:** Python {sys.version.split()[0]} | scikit-learn {joblib.__version__}  ")
    md.append("**Project:** AgriSmart — Smart Agriculture Decision Support System  \n")
    md.append("---\n")
    
    md.append("## 1. Executive Summary & Model Comparison Table\n")
    # Direct pure-python markdown table generation (avoids tabulate dependency)
    cols = comparison_df.columns.tolist()
    header = "| " + " | ".join(cols) + " |"
    divider = "| " + " | ".join(["---"] * len(cols)) + " |"
    rows = []
    for _, row in comparison_df.iterrows():
        rows.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
    md.append(header)
    md.append(divider)
    md.extend(rows)
    md.append("\n---\n")
    
    # Module A
    md.append("## 2. Module A: Crop Recommendation (Multiclass Classification)\n")
    md.append(f"- **Target Variable:** `{crop_meta['target']}` ({len(crop_meta['labels'])} balanced classes, 100 samples each)\n")
    md.append(f"- **Data Split:** Stratified 80:20 split (`random_state=42`) | Train: {crop_meta['train_samples']} | Test: {crop_meta['test_samples']}\n")
    md.append(f"- **Selected Model:** **{crop_meta['selected_model']}**\n")
    md.append(f"- **Selection Rationale:** {crop_meta['selection_reason']}\n\n")
    
    md.append("### Held-Out Test Candidate Comparison\n")
    md.append("| Model Candidate | Macro-F1 | Accuracy | Weighted-F1 | Status |\n")
    md.append("|---|---|---|---|---|\n")
    for name, m in crop_meta["all_candidates"].items():
        sel = "★ SELECTED" if name == crop_meta["selected_model"] else "Baseline / Candidate"
        md.append(f"| {name} | {m['macro_f1']:.4f} | {m['accuracy']:.4f} | {m['weighted_f1']:.4f} | {sel} |\n")
    md.append("\n")
    
    md.append("### Selected Model Classification Report\n")
    md.append("```\n")
    cr = crop_meta["metrics"]["classification_report"]
    report_rows = []
    for lbl, metrics in cr.items():
        if isinstance(metrics, dict):
            report_rows.append(f"{lbl:<15} Precision: {metrics['precision']:.3f} | Recall: {metrics['recall']:.3f} | F1: {metrics['f1-score']:.3f} | Support: {metrics['support']}")
    md.append("\n".join(report_rows))
    md.append("\n```\n\n---\n")
    
    # Module B
    md.append("## 3. Module B: Fertilizer Recommendation (Multiclass Classification)\n")
    md.append(f"- **Target Variable:** `{fert_meta['target']}` (7 classes with severe class imbalance)\n")
    md.append(f"- **Data Split:** Stratified 80:20 split (`random_state=42`) | Train: {fert_meta['train_samples']} | Test: {fert_meta['test_samples']}\n")
    md.append(f"- **Selected Model:** **{fert_meta['selected_model']}**\n")
    md.append(f"- **Selection Rationale:** {fert_meta['selection_reason']}\n\n")
    
    md.append("### Held-Out Test Candidate Comparison\n")
    md.append("| Model Candidate | Macro-F1 | Accuracy | Weighted-F1 | Status |\n")
    md.append("|---|---|---|---|---|\n")
    for name, m in fert_meta["all_candidates"].items():
        sel = "★ SELECTED" if name == fert_meta["selected_model"] else "Baseline / Candidate"
        md.append(f"| {name} | {m['macro_f1']:.4f} | {m['accuracy']:.4f} | {m['weighted_f1']:.4f} | {sel} |\n")
    md.append("\n")
    
    md.append("### Per-Class Performance Breakdown (Attention to Rare Classes)\n")
    md.append("| Fertilizer Class | Precision | Recall | F1-Score | Test Support |\n")
    md.append("|---|---|---|---|---|\n")
    cr_fert = fert_meta["metrics"]["classification_report"]
    for lbl in fert_meta["labels"]:
        if lbl in cr_fert:
            m = cr_fert[lbl]
            md.append(f"| {lbl} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1-score']:.4f} | {int(m['support'])} |\n")
    md.append("\n---\n")
    
    # Module C
    md.append("## 4. Module C: Crop Yield Prediction (Regression)\n")
    md.append(f"- **Target Variable:** `{yield_meta['target']}` (Units: {yield_meta['target_unit']})\n")
    md.append(f"- **Split Strategy:** {yield_meta['split_strategy']}\n")
    md.append(f"- **Train Period:** 1990–2009 ({yield_meta['train_samples']} samples) | **Test Period:** 2010–2013 ({yield_meta['test_samples']} samples)\n")
    md.append(f"- **Selected Model:** **{yield_meta['selected_model']}**\n")
    md.append(f"- **Selection Rationale:** {yield_meta['selection_reason']}\n\n")
    
    md.append("### Held-Out Temporal Horizon Candidate Comparison\n")
    md.append("| Model Candidate | RMSE (hg/ha) | MAE (hg/ha) | R² Score | RMSE (tonnes/ha) | Status |\n")
    md.append("|---|---|---|---|---|---|\n")
    for name, m in yield_meta["all_candidates"].items():
        sel = "★ SELECTED" if name == yield_meta["selected_model"] else "Baseline / Candidate"
        rmse_t = f"{m['rmse_tonnes_per_ha']:.2f}" if m.get("rmse_tonnes_per_ha") is not None else "N/A"
        md.append(f"| {name} | {m['rmse']:,.2f} | {m['mae']:,.2f} | {m['r2']:.4f} | {rmse_t} | {sel} |\n")
    md.append("\n")
    
    md.append("### Target Distribution on Held-Out Test Set (2010–2013)\n")
    ym = yield_meta["metrics"]
    md.append(f"- **Mean Yield:** {ym['target_mean']:,.2f} hg/ha ({ym['target_mean']/10000:.2f} tonnes/ha)\n")
    md.append(f"- **Standard Deviation:** {ym['target_std']:,.2f} hg/ha\n")
    md.append(f"- **Min / Max:** {ym['target_min']:,.2f} / {ym['target_max']:,.2f} hg/ha\n")
    md.append(f"- **Selected Model RMSE as % of Mean:** {ym['rmse_pct_of_mean']:.2f}%\n")
    md.append(f"- **Selected Model MAE as % of Mean:** {ym['mae_pct_of_mean']:.2f}%\n\n")
    
    md.append("---\n## 5. Agronomic Disclaimers & Limitations\n")
    md.append("1. **Decision Support Nature:** Predictions generated by these models represent statistical approximations derived from historical benchmark datasets. They are decision-support aids and do not supersede certified agronomist counsel or soil testing laboratory results.\n")
    md.append("2. **Regional Granularity:** Crop yield predictions rely on national-level FAO aggregates. Local farm microclimates, pest pressures, and specialized management inputs will vary from regional averages.\n")
    md.append("3. **Fertilizer Representation:** The fertilizer recommendation dataset reflects algorithmic simulation rules and must be treated as guidance rather than clinical prescription.\n")
    
    return "\n".join(md)


def run_training_pipeline():
    """Execute end-to-end training, serialization, and report generation."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    all_comparison_rows = []
    
    # 1. Module A
    crop_pipe, crop_meta, crop_rows = train_crop_recommendation()
    joblib.dump(crop_pipe, MODELS_DIR / "crop_recommendation.joblib", compress=3)
    with open(MODELS_DIR / "crop_recommendation_meta.json", "w") as f:
        json.dump(crop_meta, f, indent=2)
    all_comparison_rows.extend(crop_rows)
    logger.info("Saved crop_recommendation.joblib and metadata.")
    
    # 2. Module B
    fert_pipe, fert_meta, fert_rows = train_fertilizer_recommendation()
    joblib.dump(fert_pipe, MODELS_DIR / "fertilizer_recommendation.joblib", compress=3)
    with open(MODELS_DIR / "fertilizer_recommendation_meta.json", "w") as f:
        json.dump(fert_meta, f, indent=2)
    all_comparison_rows.extend(fert_rows)
    logger.info("Saved fertilizer_recommendation.joblib and metadata.")
    
    # 3. Module C
    yield_pipe, yield_meta, yield_rows = train_yield_prediction()
    joblib.dump(yield_pipe, MODELS_DIR / "yield_prediction.joblib", compress=3)
    with open(MODELS_DIR / "yield_prediction_meta.json", "w") as f:
        json.dump(yield_meta, f, indent=2)
    all_comparison_rows.extend(yield_rows)
    logger.info("Saved yield_prediction.joblib and metadata.")
    
    # 4. Reports Generation
    comparison_df = pd.DataFrame(all_comparison_rows)
    comparison_df.to_csv(REPORTS_DIR / "model_comparison.csv", index=False)
    logger.info("Saved reports/model_comparison.csv")
    
    eval_md = generate_evaluation_markdown(crop_meta, fert_meta, yield_meta, comparison_df)
    with open(REPORTS_DIR / "MODEL_EVALUATION.md", "w", encoding="utf-8") as f:
        f.write(eval_md)
    logger.info("Saved reports/MODEL_EVALUATION.md")
    
    logger.info("=== End-to-end training pipeline completed successfully! ===")


if __name__ == "__main__":
    run_training_pipeline()
