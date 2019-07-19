from selenium import webdriver
import time, argparse

SCROLL_DOWN = "window.scrollTo(0, document.body.scrollHeight)"

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
        driver.get(
            f"https://www.instagram.com/{username}/"
        )  # open page with user
        time.sleep(3)  # wait for page to load
        posts = set()
        for _ in range(1000): # scroll to "infinity"
            driver.execute_script(SCROLL_DOWN)
            time.sleep(1)
            post_list = self.get_post_list()
            for post in post_list:
                if post not in posts:
                    posts.update([post])
            if len(posts) > self.num_of_posts:
                break
        return posts

    def get_post_list(self):
        all_a_elements = self.driver.find_elements_by_tag_name("a") # get a tag elements
        all_links = [a.get_attribute("href") for a in all_a_elements] # get all links
        post_links = list(filter(lambda link: "/p/" in link, all_links)) # filter posts
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
        default=50
    )
    args = vars(parser.parse_args())
    return args["username"], args["num_of_posts"]

if __name__ == "__main__":
    driver = webdriver.Firefox()
    username, num_of_posts_str = read_args()
    crawler = InstaUserPostCrawler(username, int(num_of_posts_str), driver)
    print(crawler.crawl())