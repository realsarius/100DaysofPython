from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://en.wikipedia.org/wiki/Main_Page")

try:
    # article_count = driver.find_element(By.ID, value="articlecount")
    # print(article_count.text.split(" ")[0])
    article_count = driver.find_element(By.CSS_SELECTOR, value="#articlecount a")
    print(article_count.text)
    # article_count.click()


    all_portals = driver.find_element(By.LINK_TEXT, value="Content portals")
    # all_portals.click()

    search = driver.find_element(By.NAME, value="search")
    driver.find_element(By.XPATH, value='//*[@id="p-search"]/a').click()
    search.send_keys("Python", Keys.ENTER)
finally:
    pass
