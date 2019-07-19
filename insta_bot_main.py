"""import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import path
import time
import ast
import csv


class InstaFollower:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        self.FOLLOWED_LOG_PATH = "followed.txt"

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

    def get_post_links(self, tag, num_to_like):
        driver = self.driver  # get driver
        driver.get(
            f"https://www.instagram.com/explore/tags/{tag}/"
        )  # open page with tag
        time.sleep(3)  # wait for page to load
        followed = []
        # load all follow tags
        if path.exists(self.FOLLOWED_LOG_PATH):
            with open(self.FOLLOWED_LOG_PATH, "r") as followed_file:
                csv_reader = csv.reader(followed_file, delimiter=",")
                followed = [row[0] for row in csv_reader]
        all_post_links = []
        # load x posts
        for _ in range(1000):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            all_a_elements = driver.find_elements_by_tag_name("a")
            all_links = [a.get_attribute("href") for a in all_a_elements]
            post_links = list(filter(lambda link: "/p/" in link, all_links))
            post_links = post_links[9:]
            for post in post_links:
                if post not in all_post_links and post not in followed:
                    all_post_links.append(post)
            if len(all_post_links) > num_to_like:
                break
        return all_post_links, followed

    def like_tag(self, tag, num_to_like):
        post_links, followed = self.get_post_links(tag, num_to_like)
        driver = self.driver  # get driver
        for post in post_links:
            driver.get(post)  # open post
            time.sleep(3)
            driver.find_element_by_class_name("yWX7d").click()
            # save post to followed and to file
            followed.append(post)
            with open(self.FOLLOWED_LOG_PATH, "a") as followed_file:
                csv_writer = csv.writer(followed_file, delimiter=",")
                csv_writer.writerow([post])
            time.sleep(10)

    def like_tags(self, tags, num_to_like):
        for tag in tags:
            self.like_tag(tag, num_to_like)

    def unfollow_all(self):
        driver = self.driver  # get driver
        followed = []
        if path.exists(self.FOLLOWED_LOG_PATH):
            with open(self.FOLLOWED_LOG_PATH, "r") as followed_file:
                csv_reader = csv.reader(followed_file, delimiter=",")
                followed = [row[0] for row in csv_reader]
        
        for post in followed:
            driver.get(post)  # open post
            time.sleep(3)
            driver.find_element_by_class_name("yWX7d").click()
            time.sleep(3)
            driver.find_element_by_class_name("aOOlW").click()


def read_args():
    parser = argparse.ArgumentParser(
        description="""Follow people posting given tags. 
        Posts of people that were followed are added to file followed.txt 
        and can be unfollowed using this list. 
        Caviats: If post was deleted it will not unfollow."""
    )
    parser.add_argument(
        "-u", "--username", required=True, help="your instagram username", default=None
    )
    parser.add_argument(
        "-p", "--password", required=True, help="your instagram password", default=None
    )
    parser.add_argument(
        "-t", "--tag_list", required=False, help="list of tags to search", default=[]
    )
    parser.add_argument(
        "-n",
        "--num_of_follow",
        required=False,
        help="approximate number of people to follow per tag",
        default=50,
    )
    parser.add_argument(
        "-uf",
        "--unfollow",
        action="store_true",
        help="""use if instead of following you want to start 
        process of unfollowing people stored in followed.txt""",
    )
    args = vars(parser.parse_args())
    return args["username"], args["password"], args["tag_list"], args["num_of_follow"], args["unfollow"]


if __name__ == "__main__":
    username, password, tag_list, num_of_follow, unfollow = read_args()
    browser = InstaFollower(username, password)
    browser.login()
    if unfollow:
        browser.unfollow_all()
    else:
        browser.like_tags(ast.literal_eval(tag_list), int(num_of_follow))"""
