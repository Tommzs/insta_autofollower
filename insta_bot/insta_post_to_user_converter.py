from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time, argparse, ast

if __name__ == "__main__":
    import element_classes as el
    import constants as c
else:
    from . import element_classes as el
    from . import constants as c


class InstaPostToUserConverter:
    def __init__(self, posts, driver):
        self.posts = posts
        self.driver = driver

    def convert(self):
        users = set()
        for post in self.posts:  # get posts for each tag
            user = self.get_user(post)
            if user is not None:
                users.add(user)
        return list(users)

    def get_user(self, post):
        driver = self.driver  # get driver
        driver.get(post)  # open page with post
        time.sleep(c.LOAD_WAIT)  # wait for post to load
        user = None

        try:
            user = driver.find_element_by_class_name(el.POST_USER_BUTTON_CLASS).text
        except NoSuchElementException as _:
            print(
                f"Post {post} does not exist or there are issues with your connection."
            )

        return user


def read_args():
    parser = argparse.ArgumentParser(
        description="""Get list of users that posted posts from a list."""
    )
    parser.add_argument(
        "-p", "--post_list", required=True, help="list of posts to convert", default=[]
    )
    args = vars(parser.parse_args())
    return args["post_list"]


if __name__ == "__main__":
    driver = webdriver.Firefox()
    post_list_str = read_args()
    converter = InstaPostToUserConverter(ast.literal_eval(post_list_str), driver)
    print(converter.convert())
