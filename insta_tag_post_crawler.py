from selenium import webdriver
import time, argparse, ast


SCROLL_DOWN = "window.scrollTo(0, document.body.scrollHeight)"


class InstaTagPostCrawler:
    def __init__(self, tags, num_of_posts):
        self.tags = tags
        self.num_of_posts = num_of_posts
        self.driver = webdriver.Firefox()

    def crawl(self):
        posts = set()
        for tag in self.tags: # get posts for each tag
            posts.update(self.get_posts(tag))
        return list(posts)

    def get_posts(self, tag):
        driver = self.driver  # get driver
        driver.get(
            f"https://www.instagram.com/explore/tags/{tag}/"
        )  # open page with tag
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
        return post_links[9:] # ignore first 9 (skip recommended posts)


def read_args():
    parser = argparse.ArgumentParser(
        description="""Get list of recent instagram post with specified tags."""
    )
    parser.add_argument(
        "-t", "--tag_list", required=True, help="list of tags to search", default=[]
    )
    parser.add_argument(
        "-n",
        "--num_of_posts",
        required=False,
        help="approximate number of posts to get",
        default=50,
    )
    args = vars(parser.parse_args())
    return args["tag_list"], args["num_of_posts"]

if __name__ == "__main__":
    tag_list_str, num_of_posts_str = read_args()
    crawler = InstaTagPostCrawler(ast.literal_eval(tag_list_str), int(num_of_posts_str))
    print(crawler.crawl())
    