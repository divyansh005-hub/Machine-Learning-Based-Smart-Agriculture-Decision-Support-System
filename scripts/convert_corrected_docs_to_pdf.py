"""Convert all corrected docx files in SE_Deliverables_Corrected to high-resolution PDFs using Microsoft Word COM.
"""

import os
import sys
from pathlib import Path

try:
    import win32com.client
except ImportError:
    print("win32com.client not available.")
    sys.exit(1)

CORRECTED_DIR = Path(r"D:\NIIT_University\Projects\Smart Agricultutre\SE_Deliverables_Corrected")

docs_to_convert = [
    "01_Project_Proposal.docx",
    "02_SRS.docx",
    "03_SDD.docx",
    "04_Wireframes.docx",
    "06_Testing_Report.docx",
    "08_Final_Report.docx"
]

print("Initializing Microsoft Word COM...")
word = win32com.client.Dispatch("Word.Application")
word.Visible = False

try:
    for doc_name in docs_to_convert:
        docx_path = CORRECTED_DIR / doc_name
        pdf_name = doc_name.replace(".docx", ".pdf")
        pdf_path = CORRECTED_DIR / pdf_name
        
        if not docx_path.exists():
            print(f"Skipping {doc_name}: file does not exist.")
            continue
            
        print(f"Converting {doc_name} -> {pdf_name}...")
        doc = word.Documents.Open(str(docx_path.resolve()))
        # FileFormat=17 represents wdFormatPDF
        doc.SaveAs(str(pdf_path.resolve()), FileFormat=17)
        doc.Close()
        print(f"Success: {pdf_name} ({os.path.getsize(pdf_path):,} bytes)")
finally:
    word.Quit()
    print("Microsoft Word COM closed.")

print("All PDF conversions complete.")
