import praw
from praw.models import Submission
import credentials
import pprint
import urllib.request
import time
import wget


reddit = praw.Reddit(client_id=credentials.client_id,
                     client_secret=credentials.client_secret,
                     user_agent="My user agent",
                     username=credentials.username,
                     password=credentials.password)

#saved = reddit.redditor(credentials.username).saved
saved = reddit.user.me().saved(limit=None)

#print(saved)
for item in saved:

    if isinstance(item, Submission):
        # submission: https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
        if item.over_18 == False:
            submission = reddit.submission(item.id)
            #pprint.pprint(vars(submission))
            #print()
            link = str(submission.url)
            print(link)
            if ".jpg" in link or ".png" in link or ".gif" in link:
                directory = "/Users/jhavens/Pictures/Test/"
                filename = wget.download(submission.url, directory)
                print(filename)
            if ".gifv" in link:
                directory = "/Users/jhavens/Pictures/Test/"#+item.id+".gifv"
                filename = wget.download(submission.url, directory)
                print(filename)
            if "gfycat.com" in link:
                directory = "/Users/jhavens/Pictures/Test/"+item.id+".mp4"
                filename = wget.download(submission.url, directory)
                print(filename)

            #print(item.permalink)

            print()
            time.sleep(.5)
    else: #if it is not a submission eg a comment
        pass


# submission = reddit.submission(id='5or86n')
# submission.unsave()
