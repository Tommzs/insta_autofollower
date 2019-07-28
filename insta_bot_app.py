from insta_bot.insta_tag_post_crawler import InstaTagPostCrawler
from insta_bot.insta_post_to_user_converter import InstaPostToUserConverter
from insta_bot.insta_user_post_crawler import InstaUserPostCrawler
from insta_bot.insta_logger import InstaLogger
from insta_bot.insta_post_liker import InstaPostLiker
from insta_bot.insta_user_follower import InstaUserFollower
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from os import path
from getpass import getpass
import time, csv
import consts as c


def bot_menu():
    print(c.INSTA_LOGO)
    print(f"------|||||| Insta bot v{c.VERSION} ||||||------")
    print(f"Hi, I am here to help you gain fame on Instagram! :)")
    print(c.SELECT_MENU)
    return int(input("What you want me to do for you today?: "))


def execute_selection(selection):
    status = None
    if 0 < selection < 8:
        if selection == 1:
            status = A_get_posts_by_tags()
        elif selection == 2:
            status = B_get_users_by_tags()
        elif selection == 3:
            status = C_get_posts_by_users()
        elif selection == 4:
            status = D_like_posts_by_tags()
        elif selection == 5:
            status = E_follow_users_by_tags()
        elif selection == 6:
            status = F_like_posts_by_users()
        elif selection == 7:
            status = G_unfollow_users()
    else:
        status = f"Sorry I dont know what option ({selection}) is. :(."
    return status


def A_get_posts_by_tags():
    # get tag list
    tags = ask_for_tags()
    if(len(tags) < 1):
        return "Cant search tags without tags, please give me some tags (:"

    # get number of posts
    try:
        num = ask_for_number_of_posts()
    except ValueError as _:
        return "Thats not a number... dont try to fool me! :P"
    if num > c.MAX_POSTS:
        return f"Sorry cant handle more than {c.MAX_POSTS} posts. (Psst: you can change that in consts.py)"

    # ask if headless
    headless = ask_if_headless()

    # ask for filename
    filename = ask_for_filename()
    
    print("Thanks :) Lets see what I can find...")

    # get tags
    driver = get_driver(headless)
    tag_crawler = InstaTagPostCrawler(tags, num_of_posts=num, driver=driver)
    posts = tag_crawler.crawl()

    # save to file
    list_to_csv(filename, posts)

    return f"Posts saved to file {filename}. It was a pleasure helping you. :)"
    

def B_get_users_by_tags():
    # get tag list
    tags = ask_for_tags()
    if(len(tags) < 1):
        return "No tags were given. Please give me some tags :("

    # get number of posts
    try:
        num = ask_for_number_of_users()
    except ValueError as _:
        return "I can tell a number from... not a number. Give me a number next time if you want me to help you."
    if num > c.MAX_USERS:
        return f"Whaaat..so many? I cant. Sorry.. at most {c.MAX_USERS}. Or change it in consts.py"

    # ask if headless
    headless = ask_if_headless()

    # ask for filename
    filename = ask_for_filename()
    
    print("Lets see who posts with these tags...")

    # get users from tags
    driver = get_driver(headless)
    tag_crawler = InstaTagPostCrawler(tags, num_of_posts=num*2, driver=driver)
    posts = tag_crawler.crawl()

    post_to_user_converter = InstaPostToUserConverter(posts, driver)
    users = post_to_user_converter.convert()

    if len(users) > num:
        users = users[:num]
    else:
        print(f"I only found {len(users)} users for given tags. Seems like too many posts were posted by 1 user. Try different tags. Sorry :(")

    # save to file
    list_to_csv(filename, users)

    return f"I have saved the users to {filename} for you."


def C_get_posts_by_users():
    # get user list
    users = ask_for_users()
    if(len(users) < 1):
        return "No users were given. I guess you dont want me to do anything :("
    
    # get number of posts
    try:
        num = ask_for_number_of_posts()
    except ValueError as _:
        return "Thats not a number... dont try to fool me! :P"
    if num > c.MAX_POSTS:
        return f"Sorry cant handle more than {c.MAX_POSTS} posts. (Psst: you can change that in consts.py)"

    # ask if headless
    headless = ask_if_headless()

    # ask for filename
    filename = ask_for_filename()
    
    print("Thanks :) Lets see what I can find...")

    # get users
    driver = get_driver(headless)
    posts = []
    for user in users:
        tag_crawler = InstaUserPostCrawler(username=user, num_of_posts=num, driver=driver)
        posts += tag_crawler.crawl()

    # save to file
    list_to_csv(filename, posts)

    return f"Posts for all users saved to file {filename}. Let me know when you need something else :)"


def D_like_posts_by_tags():
    # get username and password
    username = ask_for_username()
    password = ask_for_password()

     # get tag list
    tags = ask_for_tags()
    if(len(tags) < 1):
        return "Cant search tags without tags, please give me some tags (:"

    # get number of posts
    try:
        num = ask_for_number_of_posts()
    except ValueError as _:
        return "Thats not a number... dont try to fool me! :P"
    if num > c.MAX_POSTS:
        return f"Sorry cant handle more than {c.MAX_POSTS} posts. (Psst: you can change that in consts.py)"

    # ask if headless
    headless = ask_if_headless()
    
    print("Thanks :) Lets go do some liking...")

    # set driver
    driver = get_driver(headless)
    
    # login
    logger = InstaLogger(username, password, driver=driver)
    is_logged = logger.login()
    if not is_logged:
        return f"Wrong username or password."

    # get list of posts
    tag_crawler = InstaTagPostCrawler(tags, num_of_posts=num, driver=driver)
    posts = tag_crawler.crawl()
    if len(posts) < 1:
        return f"No posts found, nothing to like."

    # like tags
    tag_liker = InstaPostLiker(post_list=posts, driver=driver)
    tag_liker.like()

    return f"All done. Lets do this again sometimes..."


def E_follow_users_by_tags():
    # get username and password
    username = ask_for_username()
    password = ask_for_password()

     # get tag list
    tags = ask_for_tags()
    if(len(tags) < 1):
        return "Cant search tags without tags, please give me some tags (:"

    # get number of posts
    try:
        num = ask_for_number_of_users()
    except ValueError as _:
        return "Thats not a number... dont try to fool me! :P"
    if num > c.MAX_POSTS:
        return f"Sorry cant handle more than {c.MAX_USERS} users. (Psst: you can change that in consts.py)"

    # ask for filename
    filename = ask_for_filename("Where should I save list of followed users? ")

    # ask if headless
    headless = ask_if_headless()
    
    print("Thanks :) Lets follow some ppl...")

    # set driver
    driver = get_driver(headless)
    
    # login
    logger = InstaLogger(username, password, driver=driver)
    is_logged = logger.login()
    if not is_logged:
        return f"Wrong username or password."

    # get list of posts
    tag_crawler = InstaTagPostCrawler(tags, num_of_posts=round(num*1.5), driver=driver)
    posts = tag_crawler.crawl()
    if len(posts) < 1:
        return f"No posts found, nothing to follow."

    user_converter = InstaPostToUserConverter(posts, driver)
    users = user_converter.convert()

    if(len(users) < num):
        return f"Sorry could only get {len(users)} users. I will still follow them, dont worry. :)"
    else:
        users = users[:num]
    
    # follow users
    user_follower = InstaUserFollower(user_list=users, driver=driver)
    user_follower.follow()

    # save followed users to file
    list_to_csv(filename, list_to_save=users)

    return f"All done. Thanks for using my services! :)"


def F_like_posts_by_users():
    # get username and password
    username = ask_for_username()
    password = ask_for_password()

     # get tag list
    users = ask_for_users()
    if(len(users) < 1):
        return "Cant like posts of users if there are no users :("

    # get number of posts
    try:
        num = ask_for_number_of_posts()
    except ValueError as _:
        return "Thats not a number... dont try to fool me! :P"
    if num > c.MAX_POSTS:
        return f"Sorry cant handle more than {c.MAX_POSTS} posts. (Psst: you can change that in consts.py)"

    # ask if headless
    headless = ask_if_headless()
    
    print("Thanks :) Lets go do some liking...")

    # set driver
    driver = get_driver(headless)
    
    # login
    logger = InstaLogger(username, password, driver=driver)
    is_logged = logger.login()
    if not is_logged:
        return f"Wrong username or password."

    # get list of posts
    posts = []
    for user in users:
        user_crawler = InstaUserPostCrawler(user, num_of_posts=num, driver=driver)
        posts += user_crawler.crawl()
    if len(posts) < 1:
        return f"No posts found, nothing to like."

    # like posts
    post_liker = InstaPostLiker(post_list=posts, driver=driver)
    post_liker.like()

    return f"All done. Lets do this again sometimes..."


def G_unfollow_users():
    return "OK"


def get_driver(headless):
    options = Options()
    options.headless = headless
    return webdriver.Firefox(options=options)


def list_to_csv(filename, list_to_save):
    with open(filename, 'w') as writeFile:
        writer = csv.writer(writeFile, delimiter='\n')
        writer.writerows([list_to_save])


def ask_for_list_str(message, input_str):
    print(f"{message} Write each followed by enter. If you want to finish, do not write anything into the line and press enter.")
    out_list = []
    element = None
    while element != "":
        element = input(input_str)
        out_list.append(element)
    return out_list[:-1]


def ask_for_str(message, show_in=True):
    str_in = ""
    while str_in == "":
        if show_in:
            str_in = input(message)
        else:
            str_in = getpass(message)
        if str_in == "":
            print(f"Write valid string please. I cant work with {str_in}.. :(")
    return str_in


def ask_if_a_or_b(message, opTrue, opFalse):
    print(message)
    answer = []
    while answer != opTrue and answer != opFalse:
        answer = input(f"{opFalse}/{opTrue}: ")
    return True if answer == opTrue else False


def ask_for_username():
    return ask_for_str("What is your instagram username?:")


def ask_for_password():
    return ask_for_str("What is your instagram password?:", show_in=False)


def ask_for_number_of_posts():
    return int(input("How many posts for each tag/user do you want me to get? "))


def ask_for_number_of_users():
    return int(input("How many user links do you want me to get? "))


def test_file(filename):
    try:
        open(filename, 'w')
        return True
    except OSError:
        return False


def ask_for_filename(message="Select name of a file to which I should save what I find for you: "):
    filename = ""
    while test_file(filename) == False:
        filename = ask_for_str(message)
    return filename


def ask_for_tags():
    message = "What tags are you interested in? Write each followed by enter. If you want to finish, do not write anything into the line and press enter."
    return ask_for_list_str(message, input_str="#")


def ask_for_users():
    message = "What user's post are you interested in?"
    return ask_for_list_str(message, input_str="@")


def ask_if_headless():
    message = "Do you want to spy on me while I am doing whatever you want me to do or can I do it privately? Write 'spy' or 'private' please."
    opTrue = "private"
    opFalse = "spy"
    return ask_if_a_or_b(message, opTrue=opTrue, opFalse=opFalse)


if __name__ == "__main__":
    selection = bot_menu()
    status = execute_selection(selection)
    print(status)