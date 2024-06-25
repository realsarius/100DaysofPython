from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ACCOUNT_EMAIL = "your_email@example.com"
ACCOUNT_PASSWORD = "your_password"
PHONE = "your_phone_number"

def abort_application():
    try:
        close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        close_button.click()
        time.sleep(2)
        
        discard_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")
        discard_button.click()
    except NoSuchElementException:
        pass 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3586148395&f_LF=f_AL&geoId=101356765&"
               "keywords=python&location=London%2C%20England%2C%20United%20Kingdom&refresh=true")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-tracking-control-name="reject_consent"]'))).click()

    sign_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
    sign_in_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(ACCOUNT_EMAIL)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(ACCOUNT_PASSWORD)
    password_field.send_keys(Keys.ENTER)

    input("Press Enter when you have solved the Captcha")

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable")))
    all_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

    for listing in all_listings:
        print("Opening Listing")
        listing.click()
        time.sleep(2)
        
        try:
            apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-apply-button")
            apply_button.click()

            try:
                phone = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='phone']")))
                if phone.get_attribute("value") == "":
                    phone.send_keys(PHONE)
            except TimeoutException:
                pass

            try:
                complex_message = driver.find_element(By.CSS_SELECTOR, ".jobs-apply-form__msg.jobs-apply-form__msg--complex")
                abort_application()
                print("Complex application, skipped.")
                continue
            except NoSuchElementException:
                print("Submitting job application")
                submit_button = driver.find_element(By.CSS_SELECTOR, "footer button[type='submit']")
                submit_button.click()

                time.sleep(2)
                close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".artdeco-modal__dismiss")))
                close_button.click()

        except NoSuchElementException:
            abort_application()
            print("No application button, skipped.")
            continue

finally:
    time.sleep(5)
    driver.quit()
