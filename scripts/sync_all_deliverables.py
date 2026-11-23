"""Synchronize all deliverables with graceful error handling for locked files.
"""

import shutil
from pathlib import Path

WORKSPACE = Path(r"D:\NIIT_University\Projects\Smart Agricultutre")
SRC_DELIVERABLES = WORKSPACE / "SE Delieverables"
CORRECTED_DIR = WORKSPACE / "SE_Deliverables_Corrected"

# Mirror corrected docx and pdf files back to SE Delieverables if unlocked
docx_pdf_files = [
    "01_Project_Proposal.docx", "01_Project_Proposal.pdf",
    "02_SRS.docx", "02_SRS.pdf",
    "03_SDD.docx", "03_SDD.pdf",
    "04_Wireframes.docx", "04_Wireframes.pdf",
    "06_Testing_Report.docx", "06_Testing_Report.pdf",
    "08_Final_Report.docx", "08_Final_Report.pdf"
]

for fname in docx_pdf_files:
    src_f = CORRECTED_DIR / fname
    dest_f = SRC_DELIVERABLES / fname
    if src_f.exists():
        try:
            shutil.copy2(src_f, dest_f)
            print(f"Mirrored {fname} -> SE Delieverables")
        except Exception as e:
            print(f"Notice: Could not mirror {fname} (file may be open by user): {e}")

print("Sync attempt completed.")
