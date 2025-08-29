
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import logging
from dotenv import load_dotenv
from datetime import datetime

# Setup logging
logging.basicConfig(filename='download_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

EMPLOYEE_ID = os.getenv("GOG_EMPLOYEE_ID")
PASSWORD = os.getenv("GOG_PASSWORD")

# Create download folder
download_dir = os.path.join(os.getcwd(), "payslips")
os.makedirs(download_dir, exist_ok=True)

# Setup Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})

# Initialize WebDriver
service = Service()
driver = webdriver.Chrome(service=service, options=options)

try:
    # Go to login page
    driver.get("https://www.gogpayslip.com/")
    time.sleep(2)

    # Fill in login form
    driver.find_element(By.ID, "employeeNumber").send_keys(EMPLOYEE_ID)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "loginButton").click()
    time.sleep(3)

    # Navigate to payslip section
    driver.find_element(By.LINK_TEXT, "My Payslip").click()
    time.sleep(2)

    # Download payslips for the past 5 years
    current_year = datetime.now().year
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    for year in range(current_year - 5, current_year + 1):
        for month in months:
            try:
                Select(driver.find_element(By.ID, "yearSelect")).select_by_visible_text(str(year))
                Select(driver.find_element(By.ID, "monthSelect")).select_by_visible_text(month)
                driver.find_element(By.ID, "generateButton").click()
                time.sleep(3)
                driver.find_element(By.ID, "saveButton").click()
                time.sleep(2)
                logging.info(f"Successfully downloaded payslip for {month} {year}")
            except Exception as e:
                logging.error(f"Failed to download payslip for {month} {year}: {e}")

except Exception as e:
    logging.critical(f"Script failed due to error: {e}")
finally:
    driver.quit()
