from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, argparse


class InstaLogger:
    def __init__(self, username, password, driver):
        self.username = username
        self.password = password
        self.driver = driver

    def login(self):
        driver = self.driver  # get driver
        driver.get("https://www.instagram.com/accounts/login/")  # open instagram login
        time.sleep(3)  # wait for page to load
        email = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")  # get password field
        email.clear()  # clear the fields
        password.clear()
        email.send_keys(self.username)  # insert username
        password.send_keys(self.password)  # insert password
        password.send_keys(Keys.RETURN)  #  login
        time.sleep(3)  # wait until logged in


def read_args():
    parser = argparse.ArgumentParser(
        description="""Log in into your instagram in Firefox browser."""
    )
    parser.add_argument(
        "-u", "--username", required=True, help="your instagram username", default=None
    )
    parser.add_argument(
        "-p", "--password", required=True, help="your instagram password", default=None
    )
    args = vars(parser.parse_args())
    return args["username"], args["password"]


if __name__ == "__main__":
    driver = webdriver.Firefox()
    username, password = read_args()
    browser = InstaLogger(username, password, driver)
    browser.login()