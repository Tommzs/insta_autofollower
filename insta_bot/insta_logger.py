from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time, argparse
if __name__ == "__main__" or __name__ == "insta_logger":
    import element_classes as el
else:
    from . import element_classes as el

class InstaLogger:
    def __init__(self, username, password, driver):
        self.username = username
        self.password = password
        self.driver = driver

    def login(self):
        driver = self.driver  # get driver
        driver.get("https://www.instagram.com/accounts/login/")  # open instagram login
        time.sleep(2)  # wait for page to load
        email = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")  # get password field
        email.clear()  # clear the fields
        password.clear()
        email.send_keys(self.username)  # insert username
        password.send_keys(self.password)  # insert password
        password.send_keys(Keys.RETURN)  #  login
        time.sleep(5)  # wait until logged in
        user = self.username
        try:
            driver.find_element_by_class_name(el.HOME_NOTIFICATIONS_NOT_NOW_BUTTON).click()
        except NoSuchElementException as _:
            print("Notification box not found. If your internet is too slow it might cause issues.")
        try:
            user = driver.find_element_by_class_name(el.HOME_USERNAME_LABEL).text
        except NoSuchElementException as _:
            print("Username could not be retrieved. If your used email for login, this might cause issue. If you use your instagram username instead everything should be ok.")
        
        return driver.current_url == "https://www.instagram.com/", user


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
