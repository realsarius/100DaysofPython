from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://secure-retreat-92358.herokuapp.com/")

try:
    first_name = driver.find_element(By.NAME, value="fName").send_keys("John")
    last_name = driver.find_element(By.NAME, value="lName").send_keys("Doe")
    last_name = driver.find_element(By.NAME, value="email").send_keys("john.doe@doesntexist.com")
    submit_button = driver.find_element(By.XPATH, value='/html/body/form/button').click()

finally:
    pass