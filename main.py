from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run_selenium():
    data = request.json
    id_number = data.get("id_number", "000000000")

    try:
        chrome_options = Options()
        chrome_options.binary_location = os.path.join(os.getcwd(), "bin", "google-chrome")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver_path = os.path.join(os.getcwd(), "bin", "chromedriver")
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigation automatisée
        driver.get("https://www.btl.gov.il/Pages/default.aspx")
        wait = WebDriverWait(driver, 20)

        link = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Topmneu_HyperLink9")))
        link.click()

        input_field = wait.until(EC.presence_of_element_located((By.ID, "vm_OptZehut")))
        input_field.clear()
        input_field.send_keys(id_number)

        label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="vm_CellMsgType$2"]')))
        label.click()

        submit_btn = wait.until(EC.element_to_be_clickable((By.NAME, "btnOpt")))
        submit_btn.click()

        time.sleep(5)

        page_source = driver.page_source
        driver.quit()

        return {"status": "success", "message": "Requête réussie"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Exécution avec waitress pour Render
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
