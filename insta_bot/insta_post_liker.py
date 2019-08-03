from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time, argparse, ast

if __name__ == "__main__":
    import element_classes as el
    import insta_logger as logger
    import constants as c
else:
    from . import element_classes as el
    from . import insta_logger as logger
    from . import constants as c


class InstaPostLiker:
    def __init__(self, post_list, driver):
        self.post_list = post_list
        self.driver = driver

    def like(self):
        driver = self.driver  # get driver
        for post in self.post_list:
            driver.get(post)  # open post
            time.sleep(c.LOAD_WAIT)

            try:
                driver.find_element_by_class_name(el.POST_LIKE_BUTTON).click()
            except NoSuchElementException as _:
                print(
                    f"Post {post} does not exist or there are issues with your connection."
                )

            time.sleep(c.LIKE_WAIT)


def read_args():
    parser = argparse.ArgumentParser(
        description="""Follow users that posted given posts"""
    )
    parser.add_argument(
        "-pl", "--post_list", required=True, help="list of posts to follow", default=[]
    )
    parser.add_argument(
        "-u", "--username", required=True, help="your instagram username", default=None
    )
    parser.add_argument(
        "-p", "--password", required=True, help="your instagram password", default=None
    )
    args = vars(parser.parse_args())
    return args["post_list"], args["username"], args["password"]


if __name__ == "__main__":
    driver = webdriver.Firefox()
    post_list_str, username, password = read_args()
    login = logger.InstaLogger(username, password, driver)
    login.login()
    liker = InstaPostLiker(ast.literal_eval(post_list_str), driver)
    liker.like()
