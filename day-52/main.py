from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

SIMILAR_ACCOUNT = "buzzfeedtasty"
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"


class InstaFollower:

    def __init__(self):
        self.driver = webdriver.Firefox()

    def login(self):
        try:
            url = "https://www.instagram.com/accounts/login/"
            self.driver.get(url)
            time.sleep(4)

            self.dismiss_cookie_warning()

            username_input = self.driver.find_element(By.NAME, "username")
            password_input = self.driver.find_element(By.NAME, "password")

            username_input.send_keys(USERNAME)
            password_input.send_keys(PASSWORD)
            password_input.send_keys(Keys.ENTER)

            time.sleep(5)

            self.dismiss_save_login_prompt()

            self.dismiss_notifications_prompt()

        except Exception as e:
            print(f"Exception during login: {str(e)}")

    def dismiss_cookie_warning(self):
        try:
            decline_button = self.driver.find_element(By.XPATH, "//button[text()='Decline']")
            decline_button.click()
        except NoSuchElementException:
            pass

    def dismiss_save_login_prompt(self):
        try:
            save_login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
            save_login_button.click()
        except NoSuchElementException:
            pass

    def dismiss_notifications_prompt(self):
        try:
            notifications_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
            notifications_button.click()
        except NoSuchElementException:
            pass

    def find_followers(self):
        try:
            time.sleep(3)
            self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/followers")
            time.sleep(5)

            modal = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            for _ in range(3):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                time.sleep(2)

        except NoSuchElementException as e:
            print(f"Exception while finding followers: {str(e)}")

    def follow(self):
        try:
            time.sleep(3)
            follow_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Follow']")
            
            for button in follow_buttons:
                try:
                    button.click()
                    time.sleep(1.5)
                except ElementClickInterceptedException:
                    cancel_button = self.driver.find_element(By.XPATH, "//button[text()='Cancel']")
                    cancel_button.click()
                    time.sleep(1)

        except NoSuchElementException as e:
            print(f"Exception while following: {str(e)}")

    def close_browser(self):
        self.driver.quit()

if __name__ == "__main__":
    bot = InstaFollower()
    try:
        bot.login()
        bot.find_followers()
        bot.follow()
    finally:
        bot.close_browser()