import praw
from praw.models import Submission
import credentials
import pprint
import urllib.request
import time
import wget
import os
import sys
import datetime
import pygsheets

gc = pygsheets.authorize()
sh = gc.open('Reddit')

wks_saved = sh.worksheet_by_title("Saved")
wks_unsaveable = sh.worksheet_by_title("Un-Saveable")
wks_nonsubmission = sh.worksheet_by_title("Non-Submission")
wks_comments = sh.worksheet_by_title("Comments")

def post_unsave(submission):
    print("Unsaving...")
    submission.unsave()

def filetypes(filetype,item,submission):
    try:
        directory = credentials.home_path+str(item.subreddit)+"_"+item.id+filetype
        filename = wget.download(submission.url, directory)
        print("\n") #wget messes with print statements
        wks_saved.insert_rows(0, number=1, values=[timestamp(),link], inherit=False)
        post_unsave(submission)

    except Exception:
        wks_unsaveable.insert_rows(0, number=1, values=[timestamp(),link], inherit=False)
        post_unsave(submission)

reddit = praw.Reddit(client_id=credentials.client_id,
                     client_secret=credentials.client_secret,
                     user_agent="My user agent",
                     username=credentials.username,
                     password=credentials.password)

def timestamp():
    d = datetime.datetime.now()
    timestamp = str(d.year)+str(d.month)+str(d.day)+str(d.hour)+str(d.minute)+str(d.second)
    return str(timestamp)

saved = reddit.user.me().saved(limit=None)

for item in saved:
    if isinstance(item, Submission): #if it is a submission
        if item.over_18 == True or item.over_18 == False:
            submission = reddit.submission(item.id)
            link = str(submission.url)
            print("SUBMISSION: "+str(link))
            if "comments" in link: #if the link has comments in it
                print("COMMENTS")
                wks_comments.insert_rows(0, number=1, values=[timestamp(),link], inherit=False)
                post_unsave(submission)
                print()
            else: #if it is not a comment
                try:
                    directory = credentials.home_path+str(item.subreddit)+"_"+item.id
                    result_1 = os.popen("java -jar "+credentials.ripme_path+"ripme.jar -l "+directory+" -u "+str(link)).read()
                    if "No compatible ripper found" in result_1 or "Error" in result_1:
                        print("NO COMPATIBLE RIPPER, TRYING WGET...")
                        if ".jpg" in link:
                            filetypes(".jpg",item,submission)
                        elif ".jpeg" in link:
                            filetypes(".jpeg",item,submission)
                        elif ".png" in link:
                            filetypes(".png",item,submission)
                        #elif ".gif" in link:
                            #filetypes(".gif",item,submission)
                        else:
                            print("PASSING")
                            wks_unsaveable.insert_rows(0, number=1, values=[timestamp(),link], inherit=False)
                            post_unsave(submission)
                    else: #if ripme didn't error
                        print("RIPME WORKED")
                        wks_saved.insert_rows(0, number=1, values=[timestamp(),link], inherit=False)
                        post_unsave(submission)
                except Exception:
                    print("EXCEPTION")
    else: #if it is not a submission eg a comment
        comment = reddit.comment(item.id)
        link = str(comment.permalink)
        print("NON-SUBMISSION: "+str(link))
        wks_nonsubmission.insert_rows(0, number=1, values=[timestamp(),link], inherit=False)
        post_unsave(comment)
    print("*********") #only ripme comes down here
