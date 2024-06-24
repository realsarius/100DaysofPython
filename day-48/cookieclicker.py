from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

timeout = time.time() + 5
five_minutes = time.time() + 60 * 5 

try:
    cookie = driver.find_element(By.ID, value="cookie")
    while True:
        for i in range(100):
            cookie.click()

        money = driver.find_element(By.ID, value="money")
        if 105 < int(money.text) < 500:
            grandma = driver.find_element(By.ID, value="buyGrandma").click()
        elif 500 < int(money.text) < 2000:
            factory = driver.find_element(By.ID, value="buyFactory").click()
        elif 2000 < int(money.text) < 7701:
            mine = driver.find_element(By.ID, value="buyMine").click()
        elif 7701 < int(money.text) < 50000:
            shipment = driver.find_element(By.ID, value="buyShipment").click()
        elif 50000 < int(money.text) < 1000000:
            shipment = driver.find_element(By.ID, value="buyAlchemy lab").click()

        if time.time() > five_minutes:
            cookie_per_second = driver.find_element(by=By.ID, value="cps").text
            print(cookie_per_second)
            break
        
finally:
    pass
