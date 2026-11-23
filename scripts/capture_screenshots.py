"""Capture authentic UI screenshots for AgriSmart test evidence across all pages."""

import os
import sys
import time
import subprocess
import urllib.request
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = WORKSPACE_ROOT / "SE Delieverables" / "07_Test_Evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

print(f"Using browser: {CHROME_PATH}")

# Start Streamlit
streamlit_proc = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true", "--server.port=8501"],
    cwd=str(WORKSPACE_ROOT),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

print("Waiting for Streamlit server to initialize...")
server_up = False
for _ in range(30):
    time.sleep(1)
    try:
        resp = urllib.request.urlopen("http://localhost:8501", timeout=2)
        if resp.status == 200:
            server_up = True
            break
    except Exception:
        pass

if not server_up:
    print("Streamlit failed to start in time.")
    streamlit_proc.terminate()
    sys.exit(1)

print("Streamlit is online on http://localhost:8501!")
time.sleep(2)

pages_to_capture = [
    ("TC-01_home_dashboard.png", "http://localhost:8501/?page=Home"),
    ("TC-02_crop_recommendation.png", "http://localhost:8501/?page=Crop"),
    ("TC-05_fertilizer_recommendation.png", "http://localhost:8501/?page=Fertilizer"),
    ("TC-08_crop_yield_prediction.png", "http://localhost:8501/?page=Yield"),
    ("TC-10_model_performance.png", "http://localhost:8501/?page=Performance"),
    ("TC-11_dataset_insights.png", "http://localhost:8501/?page=Insights"),
    ("TC-13_about_and_limitations.png", "http://localhost:8501/?page=About"),
]

for filename, url in pages_to_capture:
    out_path = EVIDENCE_DIR / filename
    print(f"Capturing {filename} from {url}...")
    subprocess.run([
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--screenshot={out_path}",
        "--window-size=1280,1024",
        url
    ], check=True)
    time.sleep(1)
    print(f"  -> Saved {out_path.name} ({os.path.getsize(out_path):,} bytes)")

streamlit_proc.terminate()
print("\nAll UI screenshots captured successfully!")
