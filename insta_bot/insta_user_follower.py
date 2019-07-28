from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time, argparse, ast
if __name__ == '__main__':
    import element_classes as el
    import insta_logger as logger
else:
    from . import element_classes as el
    from . import insta_logger as logger


class InstaUserFollower:
    def __init__(self, user_list, driver):
        self.user_list = user_list
        self.driver = driver

    def follow(self):
        driver = self.driver  # get driver
        for user in self.user_list:
            driver.get(f"https://www.instagram.com/{user}/")  # open user
            time.sleep(3)
            try:
                driver.find_element_by_class_name(el.USER_FOLLOW_BUTTON_CLASS).click()
            except NoSuchElementException as _:
                print(f"User {user} does not exist or there are issues with your connection.")
            time.sleep(10)


def read_args():
    parser = argparse.ArgumentParser(
        description="""Follow given users"""
    )
    parser.add_argument(
        "-ul", "--user_list", required=True, help="list of users to follow", default=[]
    )
    parser.add_argument(
        "-u", "--username", required=True, help="your instagram username", default=None
    )
    parser.add_argument(
        "-p", "--password", required=True, help="your instagram password", default=None
    )
    args = vars(parser.parse_args())
    return args["user_list"], args["username"], args["password"]


if __name__ == "__main__":
    driver = webdriver.Firefox()
    user_list_str, username, password = read_args()
    login = logger.InstaLogger(username, password, driver)
    login.login()
    follower = InstaUserFollower(ast.literal_eval(user_list_str), driver)
    follower.follow()