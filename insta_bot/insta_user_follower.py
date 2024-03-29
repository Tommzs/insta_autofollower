from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time, argparse, ast, random

if __name__ == "__main__":
    import element_classes as el
    import insta_logger as logger
    import constants as c
else:
    from . import element_classes as el
    from . import insta_logger as logger
    from . import constants as c


class InstaUserFollower:
    def __init__(self, user_list, driver):
        self.user_list = user_list
        self.driver = driver

    def follow(self):
        maxTries = 5
        driver = self.driver  # get driver
        followed = []

        for user in self.user_list:
            success = True
            for tryNum in range(maxTries):
                try:
                    driver.get(f"https://www.instagram.com/{user}/")  # open user
                    break
                except WebDriverException as _:
                    print(f"Loading user page of {user} failed. Retrying {tryNum+1}/{maxTries} after 2 minutes of waiting.")
                    time.sleep(120)

            time.sleep(c.LOAD_WAIT)

            try:
                driver.find_element_by_class_name(el.USER_FOLLOW_BUTTON).click()
            except NoSuchElementException as _:
                print(
                    f"User {user} does not exist or there are issues with your connection."
                )
                success = False

            if success:
                followed.append(user)
                print(f"({len(followed)}) User {user} followed successfully.")
                time.sleep(c.FOLLOW_WAIT*random.random())  

        return followed


def read_args():
    parser = argparse.ArgumentParser(description="""Follow given users""")
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
