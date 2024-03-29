from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time, argparse

if __name__ == "__main__":
    import constants as c
else:
    from . import constants as c


class InstaUserPostCrawler:
    def __init__(self, username, num_of_posts, driver):
        self.username = username
        self.num_of_posts = num_of_posts
        self.driver = driver

    def crawl(self):
        posts = self.get_posts(self.username)
        return list(posts)

    def get_posts(self, username):
        driver = self.driver  # get driver
        driver.get(f"https://www.instagram.com/{username}/")  # open page with user
        time.sleep(c.LOAD_WAIT)  # wait for page to load
        posts = set()
        prev_post_list_len = 0
        same_size_counter = 0
        for _ in range(1000):  # scroll to "infinity"
            driver.execute_script(c.SCROLL_DOWN)
            time.sleep(c.SCROLL_WAIT)
            post_list = self.get_post_list()
            for post in post_list:
                if post not in posts:
                    posts.update([post])
            if len(posts) > self.num_of_posts:
                break
            if len(posts) == prev_post_list_len:
                same_size_counter += 1
            else:
                prev_post_list_len = len(posts)
            if same_size_counter > 4:
                if prev_post_list_len == 0:
                    print(
                        f"Sorry, {username} have 0 posts, is private or does not exist."
                    )
                else:
                    print(
                        f"Sorry, {username} does not have more than {prev_post_list_len} posts."
                    )
                break
                # reduce size to required number
        while len(posts) > self.num_of_posts:
            posts.pop()
        return posts

    def get_post_list(self):
        all_a_elements = self.driver.find_elements_by_tag_name(
            "a"
        )  # get a tag elements
        all_links = [a.get_attribute("href") for a in all_a_elements]  # get all links
        post_links = list(filter(lambda link: "/p/" in link, all_links))  # filter posts
        return post_links


def read_args():
    parser = argparse.ArgumentParser(
        description="""Get list of instagram post from specified user."""
    )
    parser.add_argument(
        "-u", "--username", required=True, help="username to get posts from", default=[]
    )
    parser.add_argument(
        "-n",
        "--num_of_posts",
        required=False,
        help="approximate number of posts to get",
        default=50,
    )
    args = vars(parser.parse_args())
    return args["username"], args["num_of_posts"]


if __name__ == "__main__":
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    username, num_of_posts_str = read_args()
    crawler = InstaUserPostCrawler(username, int(num_of_posts_str), driver)
    print(crawler.crawl())
