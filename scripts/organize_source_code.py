import os
import shutil
from pathlib import Path

WORKSPACE = Path(r"d:\NIIT_University\Projects\Smart Agricultutre")
DELIVERABLES = WORKSPACE / "SE Delieverables"
SOURCE_CODE_DIR = DELIVERABLES / "05_Source_Code"

# 1. Structure Java Prototype
java_proto_dir = SOURCE_CODE_DIR / "java_prototype"
java_src_target = java_proto_dir / "src"
java_src_target.mkdir(parents=True, exist_ok=True)

old_src = SOURCE_CODE_DIR / "src"
if old_src.exists():
    for item in old_src.iterdir():
        dest = java_src_target / item.name
        if item.is_file():
            shutil.copy2(item, dest)
            item.unlink()
        elif item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
            shutil.rmtree(item)
    try:
        old_src.rmdir()
    except Exception:
        pass

# 2. Structure Python App
python_app_dir = SOURCE_CODE_DIR / "python_app"
python_app_dir.mkdir(parents=True, exist_ok=True)

items_to_copy = [
    "app.py",
    "requirements.txt",
    "src",
    "models",
    "reports",
    "tests",
]

for name in items_to_copy:
    src_path = WORKSPACE / name
    dest_path = python_app_dir / name
    if src_path.is_file():
        shutil.copy2(src_path, dest_path)
    elif src_path.is_dir():
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)

# 3. Create updated 05_Source_Code/README.md
readme_05_content = """# AgriSmart — Source Code Deliverable (05_Source_Code)

This folder contains the complete, dual-implementation source code for the **Machine Learning Based Smart Agriculture Decision Support System (AgriSmart)**.

---

## Architecture Overview

```
05_Source_Code/
├── python_app/               # PRIMARY PRODUCTION SYSTEM (Python 3.12 / Streamlit / ML)
│   ├── app.py                # Main Streamlit web application & multi-page router
│   ├── src/                  # Core modules (data pipelines, model trainers, UI views)
│   │   ├── data/             # Audited data loaders & preprocessors
│   │   ├── models/           # Scikit-learn pipelines & training automation
│   │   └── ui/               # Multi-page dashboard modules (Home, Crop, Fert, Yield, etc.)
│   ├── models/               # Serialized trained models (.joblib pipelines)
│   ├── reports/              # Model comparison metrics & evaluation report
│   ├── tests/                # Automated pytest verification test suite (22 tests)
│   └── requirements.txt      # Python dependencies
│
├── java_prototype/           # ACADEMIC OOP PROTOTYPE (Java JDK 25)
│   └── src/
│       ├── AgriSmartApp.java         # Interactive CLI application & menu system
│       ├── InputValidator.java       # Rule-based input boundary verification
│       └── AgricultureService.java   # OOP service layer encapsulation
│
└── README.md                 # This documentation guide
```

---

## 1. Primary Implementation: Python ML System (`python_app/`)

The primary deliverable of this project is a production-ready, full-stack Machine Learning application built using **Python 3.12**, **scikit-learn**, and **Streamlit**.

### Modules:
1. **Crop Recommendation**: 22-class multiclass classification using Random Forest (Macro-F1: 0.9932, Accuracy: 99.32%).
2. **Fertilizer Recommendation**: 7-class multiclass classification using Random Forest with class weighting (Macro-F1: 0.8988, Accuracy: 95.00%).
3. **Crop Yield Prediction**: Regression model predicting historical crop yield in `hg/ha` and `t/ha` using Random Forest Regressor (R²: 0.9859, RMSE: 10,756.91 hg/ha on chronological split).

### How to Run:
```bash
# Navigate to the Python application directory
cd python_app

# Install dependencies
pip install -r requirements.txt

# Launch the Streamlit Web Application
streamlit run app.py

# Run Automated Test Suite (22 Unit & Smoke Tests)
pytest tests/ -v
```

---

## 2. Academic OOP Prototype: Java (`java_prototype/`)

### Why Java is Included:
Section 7 of the university's **Software Engineering Project Guideline** (*"Small Java Implementation Model"*) requires demonstrating fundamental Object-Oriented Software Engineering concepts, including:
- Layered separation of concerns (Presentation / Controller, Validation Service, Domain Logic).
- Strict data encapsulation and strong typing.
- Modular console interface design.

To fulfill this specific guideline requirement without compromising the real Machine Learning pipelines, a self-contained Java OOP demonstration is provided under `java_prototype/src/`.

### How to Compile and Run:
```bash
cd java_prototype/src

# Compile all Java sources
javac *.java

# Execute the application
java AgriSmartApp
```

*Note: The Java prototype demonstrates architectural design and rule-based validation for academic assessment; real machine learning inference is powered by the Python scikit-learn models.*
"""

with open(SOURCE_CODE_DIR / "README.md", "w", encoding="utf-8") as f:
    f.write(readme_05_content)

print("05_Source_Code updated successfully.")
