import argparse, ast, instaloader


class InstaAccount:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.insta_session = instaloader.Instaloader()
        self.insta_session.login(username, password)
        self.profile_data = instaloader.Profile.from_username(self.insta_session.context, username)

    def get_users_that_I_follow(self):
        return set(self.profile_data.get_followers())

    def get_users_that_follow_me(self):
        return set(self.profile_data.get_followees())

    def get_users_that_I_follow_but_dont_follow_me(self):
        return [user.username for user in (self.get_users_that_I_follow() - self.get_users_that_follow_me())]

def read_args():
    parser = argparse.ArgumentParser(
        description="""Get account information"""
    )
    parser.add_argument(
        "-u", "--username", required=True, help="your instagram username", default=None
    )
    parser.add_argument(
        "-p", "--password", required=True, help="your instagram password", default=None
    )
    args = vars(parser.parse_args())
    return args["username"], args["password"]


if __name__ == "__main__":
    username, password = read_args()
    
    account = InstaAccount(username, password)
    users = account.get_users_that_I_follow_but_dont_follow_me()
    print(f"Users that I follow but they do not follow me: {users}")