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
    def __init__(self, posts, driver, follower_limit=0):
        self.posts = posts
        self.driver = driver
        self.follower_limit = follower_limit

    def convert(self):
        users = set()
        for post in self.posts:  # get posts for each tag
            user = self.get_user(post)
            if user is not None:
                if self.follower_limit > 0 and self.get_follower_count(user) <= self.follower_limit:
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

    def get_follower_count(self, user):
        driver = self.driver  # get driver
        driver.get(f"https://www.instagram.com/{user}/")  # open user
        time.sleep(c.LOAD_WAIT)

        follower_count = -1
        try:
            follower_count = int(driver.find_elements_by_class_name(el.USER_FOLLOWERS_COUNT)[1].get_attribute('title').replace(",",""))
        except [NoSuchElementException, ValueError] as _:
            print(
                f"Follower count for user {user} was not possible to retrieve. There might be issues with your internet connections."
            )

        return follower_count


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
    converter = InstaPostToUserConverter(ast.literal_eval(post_list_str), driver, 200)
    print(converter.convert())
