from selenium import webdriver
from selenium.webdriver.common.by import By
import time

PROMISED_DOWN = 32
PROMISED_UP = 8
TWITTER_EMAIL = 'YOUR_EMAIL'
TWITTER_PASSWORD = 'YOUR_PASSWORD'

class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.up = 30
        self.down = 6

    def get_internet_speed(self):
        self.driver.get('https://www.speedtest.net/')
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, value='js-start-test').click()

        time.sleep(60)

        self.down = self.driver.find_element(By.XPATH, value='/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span')
        self.up = self.driver.find_element(By.XPATH, value='/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')

        print(f'Down: {self.down.text}')
        print(f'Up: {self.up.text}')

        self.driver.close()
        self.driver.quit()


    def tweet_at_provider(self):
        self.driver.get('https://www.twitter.com')
        self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[4]/a').click()
        time.sleep(2)

        self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input').send_keys(TWITTER_EMAIL)
        self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]').click()
        time.sleep(2)

        self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys(TWITTER_PASSWORD)
        self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button').click()
        time.sleep(5)

        self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a').click()
        time.sleep(2)

        self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div').send_keys(f'Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?')
        time.sleep(1)
        
        self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/button[2]').click()



