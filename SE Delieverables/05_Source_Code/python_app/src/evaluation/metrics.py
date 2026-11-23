"""Evaluation metrics for classification and regression models in AgriSmart."""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix,
    root_mean_squared_error,
    mean_absolute_error,
    r2_score,
)


def evaluate_classifier(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    labels: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Compute comprehensive classification performance metrics.
    
    Args:
        y_true: True class labels.
        y_pred: Predicted class labels.
        labels: Optional ordered list of target class names.
        
    Returns:
        Dict[str, Any]: Dictionary containing macro-F1, accuracy, per-class report, and confusion matrix.
    """
    if labels is None:
        labels = sorted(list(set(y_true) | set(y_pred)))
        
    macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    weighted_f1 = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
    accuracy = float(accuracy_score(y_true, y_pred))
    macro_precision = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
    macro_recall = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
    
    report_dict = classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    return {
        "macro_f1": macro_f1,
        "accuracy": accuracy,
        "weighted_f1": weighted_f1,
        "macro_precision": macro_precision,
        "macro_recall": macro_recall,
        "labels": labels,
        "classification_report": report_dict,
        "confusion_matrix": cm.tolist(),
        "total_test_samples": int(len(y_true)),
    }


def evaluate_regressor(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    target_unit: str = "hg/ha",
) -> Dict[str, Any]:
    """Compute comprehensive regression performance metrics.
    
    Args:
        y_true: True numeric target values.
        y_pred: Predicted numeric target values.
        target_unit: Unit string for the target.
        
    Returns:
        Dict[str, Any]: Dictionary containing RMSE, MAE, R², and descriptive statistics.
    """
    rmse = float(root_mean_squared_error(y_true, y_pred))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    
    # Calculate percentage errors relative to mean
    mean_true = float(np.mean(y_true))
    rmse_pct = float((rmse / mean_true) * 100) if mean_true != 0 else 0.0
    mae_pct = float((mae / mean_true) * 100) if mean_true != 0 else 0.0
    
    # Convert to tonnes/ha if unit is hg/ha
    rmse_tonnes = float(rmse / 10000.0) if target_unit == "hg/ha" else None
    mae_tonnes = float(mae / 10000.0) if target_unit == "hg/ha" else None
    
    return {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
        "target_unit": target_unit,
        "rmse_pct_of_mean": rmse_pct,
        "mae_pct_of_mean": mae_pct,
        "rmse_tonnes_per_ha": rmse_tonnes,
        "mae_tonnes_per_ha": mae_tonnes,
        "target_mean": mean_true,
        "target_std": float(np.std(y_true)),
        "target_min": float(np.min(y_true)),
        "target_max": float(np.max(y_true)),
        "total_test_samples": int(len(y_true)),
    }
