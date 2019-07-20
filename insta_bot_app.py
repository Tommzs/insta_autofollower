from os import path
import time
import csv
import consts as c


def bot_menu():
    print(c.INSTA_LOGO)
    print(f"------|||||| Insta bot v{c.VERSION} ||||||------")
    print(c.SELECT_MENU)
    return int(input("Select what you want to do: "))


def execute_selection(selection):
    status = None
    if 0 < selection < 8:
        if selection == 1:
            status = A_get_posts_by_tags()
        elif selection == 2:
            status = B_get_users_by_tags
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
        status = f"Wrong option: {selection}."
    return status


def A_get_posts_by_tags():
    # get tag list
    tags = ask_for_tags()
    if(len(tags) < 1):
        return "No tags were given."

    # get number of posts
    try:
        num = ask_for_number_of_posts()
    except ValueError as _:
        return "Wrong number of posts given."
    if num > c.MAX_POSTS:
        return f"The maximal amount of posts to request is {c.MAX_POSTS}"

    # ask if headless
    headless = ask_if_headless()
    
    return "OK"


def B_get_users_by_tags():
    return "OK"


def C_get_posts_by_users():
    return "OK"


def D_like_posts_by_tags():
    return "OK"


def E_follow_users_by_tags():
    return "OK"


def F_like_posts_by_users():
    return "OK"


def G_unfollow_users():
    return "OK"


def ask_for_tags():
    print("Write tags followed by enter. Do not write anything into line and press enter to finish.")
    tags = []
    tag = None
    while tag != "":
        tag = input("#")
        tags.append(tag)
    return tags[:-1]


def ask_for_number_of_posts():
    return int(input("How many posts for each tag/user do you want to get? "))


def ask_if_headless():
    print("Do you want to see the browser during the process or hide it? Write 'see' or 'hide' please.")
    answer = []
    while answer != "see" and answer != "hide":
        answer = input("see/hide: ")
    return True if answer == "hide" else False


if __name__ == "__main__":
    selection = bot_menu()
    status = execute_selection(selection)
    print(status)