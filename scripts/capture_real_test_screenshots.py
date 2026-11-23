"""Capture authentic, live rendered test screenshots using Selenium WebDriver.

This script launches the Streamlit app, drives Chrome via Selenium,
waits for DOM elements, triggers actual test predictions, and captures
high-resolution PNG screenshots with full visual evidence.
"""

import os
import sys
import time
import subprocess
import urllib.request
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = WORKSPACE_ROOT / "SE Delieverables" / "07_Test_Evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

print("Starting Streamlit server on http://localhost:8501...")
streamlit_proc = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true", "--server.port=8501"],
    cwd=str(WORKSPACE_ROOT),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

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
    print("Streamlit server failed to start.")
    streamlit_proc.terminate()
    sys.exit(1)

print("Streamlit server is live!")

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1400,1200")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 15)

try:
    # 1. TC-01: Home Dashboard
    print("\n--- Capturing TC-01: Home Dashboard ---")
    driver.get("http://localhost:8501/?page=Home")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "hero-title")))
    time.sleep(3)  # Allow Streamlit components to finish mounting
    out_tc01 = EVIDENCE_DIR / "TC-01_home_dashboard.png"
    driver.save_screenshot(str(out_tc01))
    print(f"Saved: {out_tc01.name} ({os.path.getsize(out_tc01):,} bytes)")

    # 2. TC-02: Crop Recommendation (Perform actual prediction test!)
    print("\n--- Capturing TC-02: Crop Recommendation ---")
    driver.get("http://localhost:8501/?page=Crop")
    # Wait for the predict button
    btn_crop = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Predict Recommended Crop')]")))
    time.sleep(2)
    # Click the predict button
    driver.execute_script("arguments[0].click();", btn_crop)
    # Wait for prediction-box to appear
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "prediction-box")))
    time.sleep(3)  # Allow Plotly chart to render
    out_tc02 = EVIDENCE_DIR / "TC-02_crop_recommendation.png"
    driver.save_screenshot(str(out_tc02))
    print(f"Saved: {out_tc02.name} ({os.path.getsize(out_tc02):,} bytes)")

    # 3. TC-05: Fertilizer Recommendation (Perform actual prediction test!)
    print("\n--- Capturing TC-05: Fertilizer Recommendation ---")
    driver.get("http://localhost:8501/?page=Fertilizer")
    btn_fert = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Predict Fertilizer Formulation')]")))
    time.sleep(2)
    driver.execute_script("arguments[0].click();", btn_fert)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "prediction-box")))
    time.sleep(3)
    out_tc05 = EVIDENCE_DIR / "TC-05_fertilizer_recommendation.png"
    driver.save_screenshot(str(out_tc05))
    print(f"Saved: {out_tc05.name} ({os.path.getsize(out_tc05):,} bytes)")

    # 4. TC-08: Crop Yield Prediction (Perform actual prediction test!)
    print("\n--- Capturing TC-08: Crop Yield Prediction ---")
    driver.get("http://localhost:8501/?page=Yield")
    btn_yield = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Predict Crop Yield')]")))
    time.sleep(2)
    driver.execute_script("arguments[0].click();", btn_yield)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "prediction-box")))
    time.sleep(3)
    out_tc08 = EVIDENCE_DIR / "TC-08_crop_yield_prediction.png"
    driver.save_screenshot(str(out_tc08))
    print(f"Saved: {out_tc08.name} ({os.path.getsize(out_tc08):,} bytes)")

    # 5. TC-10: Model Performance Page
    print("\n--- Capturing TC-10: Model Performance ---")
    driver.get("http://localhost:8501/?page=Performance")
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Master Model Comparison Matrix')]")))
    time.sleep(4)  # Allow Plotly charts and dataframe to render
    out_tc10 = EVIDENCE_DIR / "TC-10_model_performance.png"
    driver.save_screenshot(str(out_tc10))
    print(f"Saved: {out_tc10.name} ({os.path.getsize(out_tc10):,} bytes)")

    # 6. TC-11: Dataset Insights Page
    print("\n--- Capturing TC-11: Dataset Insights ---")
    driver.get("http://localhost:8501/?page=Insights")
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Crop Recommendation Dataset Profile')]")))
    time.sleep(4)  # Allow EDA charts to render
    out_tc11 = EVIDENCE_DIR / "TC-11_dataset_insights.png"
    driver.save_screenshot(str(out_tc11))
    print(f"Saved: {out_tc11.name} ({os.path.getsize(out_tc11):,} bytes)")

    # 7. TC-13: About & Limitations Page
    print("\n--- Capturing TC-13: About & Limitations ---")
    driver.get("http://localhost:8501/?page=About")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "disclaimer-banner")))
    time.sleep(3)
    out_tc13 = EVIDENCE_DIR / "TC-13_about_and_limitations.png"
    driver.save_screenshot(str(out_tc13))
    print(f"Saved: {out_tc13.name} ({os.path.getsize(out_tc13):,} bytes)")

finally:
    driver.quit()
    streamlit_proc.terminate()
    print("\nBrowser closed and Streamlit server stopped.")

print("All screenshots successfully captured with full live rendered UI!")
