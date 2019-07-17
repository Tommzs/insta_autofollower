# insta_autofollower
Python script to automatically follow profiles who created posts with selected hashtags.

Posts which are used to follow are stored in followed.txt and can be used to automatically unfollow.

## Prerequisites
Gecko driver is must since its used to navigate the web browser: https://github.com/mozilla/geckodriver/releases

## Usage
Given username, password, list of hashtags of arbitrary length in format "['tag1','tag2','tag3']" and approximate number of people to follow per hashtag this script is able to navigate trough the Instagram website, find post with given hashtags and follow people who posted it.

For detailed usage write insta_autofollower.py --help
                    
## Caveats
Might try to follow 1 account twice. Will not unfollow since there is 2nd click needed for that. However if this happens, there are 2 posts from 1 user in followed.txt thus unfollowing will be attempted twice and the 2nd try will result in following again.
