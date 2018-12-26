
import time
import datetime
import praw
from prawcore import RequestException, ServerError
from asecretplace import getPythonHelperBotKeys
import sqlite3
import os
import logging



import subprocess
import traceback
import socket


# In all certainty this will be redone with sqlite3 or something similar
#  But until then, I just want to get past this
#  'just code it'



'''  
Keith Murray 
email: kmurrayis@gmail.com
'''


class phb_Reddit_Submission(object):
    '''
    Build local structure to save reddit data, only 
    be concerned with useful information, drop all else

    phb stands for Python Helper Bot

    God I hope this takes care of most reddit based errors
    I hope this acts like a padded room for the insanity that is reddit errors
    '''
    def __init__(self, sub):
        vals_Assigned = False
        self.directed_to_learning_sub = False
        self.mod_removed_for_learning = False
        self.said_thanks_or_it_worked = False
        self.deleted_or_removed = False
        
        # Prep for errors
        maxTotalWaitTime = 5*60*60
        requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
        serverBackoffTime = 5 
        maxBackoffTime = 5*60
        startTime = time.time()

        while True:
            if vals_Assigned:
                break
            try:
                now = datetime.datetime.utcnow()
                try:
                    self.author = sub.author.name
                except AttributeError:
                    # Author has deleted the post or been removed and can't be identified
                    self.author = '[deleted]'
                self.created_utc = datetime.datetime.utcfromtimestamp(sub.created_utc)
                self.id = sub.id
                self.url = sub.url
                self.score = sub.score
                self.upvote_ratio =  sub.upvote_ratio
                self.title = sub.title
                self.selftext = sub.selftext
                self.subreddit = sub.subreddit.display_name
                self.link_flair_text = sub.link_flair_text
                self.score_History = [[self.score, self.upvote_ratio, now]]
                self.edit_History = []
                vals_Assigned = True
                break
            except RequestException as e:
                logging.error("Caught Server Rate Limit Hit | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = self._backoff(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except ServerError as e:
                logging.error("Caught Server 500 Error | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                serverBackoffTime = self._backoff(serverBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except Exception as e:
                internet = is_connected()
                if internet:
                    # I'm connected and There's some problem. Figure it out and pass it along
                    logging.error("I'm connected to the internet and recieving this error")
                    logging.error("\n"+traceback.format_exc())
                    raise e 
                else:
                    # no internet, figure out what to do here
                    logging.error("I'm not connected to the internet escalating this error")
                    logging.error("\n"+traceback.format_exc())
                    raise e

    def _backoff(self, backoffTime, maxBackoffTime = 5*60):
        backoffTime = min(backoffTime, maxBackoffTime)
        time.sleep(backoffTime)
        return backoffTime*2

    def update_info(self, reddit):
        vals_Assigned = False

        
        maxTotalWaitTime = 5*60*60
        requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
        serverBackoffTime = 5 
        maxBackoffTime = 5*60
        startTime = time.time()

        while True:
            if vals_Assigned:
                break
            try:
                sub = reddit.submission(id=self.id)
                now = datetime.datetime.utcnow()
                self.edited = sub.edited
                self.score = sub.score
                self.upvote_ratio =  sub.upvote_ratio
                self.link_flair_text = sub.link_flair_text
                if self.selftext != sub.selftext:
                    self.edit_History.append(self.selftext)
                    self.selftext = sub.selftext
                self.score_History.append([self.score, self.upvote_ratio, now])
                vals_Assigned = True
                break

            except RequestException as e:
                logging.error("Caught Server Rate Limit Hit | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = self._backoff(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except ServerError as e:
                logging.error("Caught Server 500 Error | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                serverBackoffTime = self._backoff(serverBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except Exception as e:
                internet = is_connected()
                if internet:
                    # I'm connected and There's some problem. Figure it out and pass it along
                    logging.error("I'm connected to the internet and recieving this error")
                    logging.error("\n"+traceback.format_exc())
                    raise e 
                else:
                    # no internet, figure out what to do here
                    logging.error("I'm not connected to the internet escalating this error")
                    logging.error("\n"+traceback.format_exc())
                    raise e


    def _print_Full(self):
        msg = self.title
        msg += "\nPost by "+ self.author
        msg += "\nScore:  " + str(self.score)
        msg += "\nUpvote ratio: " + str(self.upvote_ratio)
        msg += "\nID: " + str(self.id)
        msg += "\nURL: " + str(self.url)
        msg += "\nSelfText:\n" + str(self.selftext)
        return msg
    def __repr__(self):
        return self._print_Full()

    #def get_top_level_comments(self, sub):

    #def get_all_comments(self, sub):


class phb_Reddit_Comment(object):
    '''
    Build local structure to save reddit data, only 
    be concerned with useful information, drop all else

    phb stands for Python Helper Bot

    God I hope this takes care of most reddit based errors
    I hope this acts like a padded room for the insanity that is reddit errors
    '''
    def __init__(self, comment):
        self.author
        self.id
        self.parentID
        self.parentSubreddit
        self.score



class phb_Reddit_User(object):
    '''
    Build local structure to save reddit data, only 
    be concerned with useful information, drop all else

    phb stands for Python Helper Bot

    God I hope this takes care of most reddit based errors
    I hope this acts like a padded room for the insanity that is reddit errors
    '''
    def __init__(self, sub):



        


# WARNING: This function is duplicated. Not yet sure how best to organize it
#   in archiveAndUpdateReddit vs rpiManager: both need the function for their own reasons, 
#   while neither module has a strong need to import the other. Perhaps is_connected and 
#   safetyZone deserve their own module
def is_connected():
    REMOTE_SERVER = "www.google.com"
    try:
        logging.info("Testing Internet Connection")
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(REMOTE_SERVER)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
	    pass
    return False


def redditSafetyZone(foo, args, kwargs, anticipated_exceptions):
    '''
    A try except block to try interacting with reddit with a growing
    backoff timer that slows down the frequency of its attempts in the 
    event of reddit server errors (500 block)


    If it involves connecting to reddit, it runs the risk of reddit's server
    errors. Rather than have this same code block littered everywhere, this

    '''


    # Bodge
    anticipated_exceptions = ValueError#(praw.errors.HTTPException)

    maxTotalWaitTime = 5*60*60
    backoffTime = 30 # starting amount of time required to wait after an error. it will then double
    maxBackoffTime = 60*60

    while True:
        try:
            x = foo(*args, **kwargs)
            break
        except anticipated_exceptions as err:
            logging.info("Caught exception\n" + err)
        # Allow other exceptions to be fully raised and handled in the logging catch. 


    return x



def grabAndUpdateNewPosts(reddit, sub="python", submissionList={}, ageLimitHours=12):
    submissionList = removeOldPosts(submissionList, ageLimitHours)
    submissionList = updatePostFeatures(reddit, submissionList)

    # Find new posts
    subreddit = reddit.subreddit(sub)
    for submission in subreddit.new(limit=40):
        if submission.id in submissionList:
            #print('Already In List')
            break
        if datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(submission.created_utc) > datetime.timedelta(hours=ageLimitHours):
            #print datetime.datetime.utcnow()
            #print datetime.datetime.utcfromtimestamp(submission.created_utc)
            #print("Past Age Limit")
            '''
            There's a risk that an old post was removed, then overturned by a mod.
            This shows up in the new feed, but all calls to the post show it as
            an old post. In an of itself, it's not bad, but it does violate the 
            assumption of orderedness (by age) that the 'new' feed has.

            As it stands, when this takes place, the bot is simply going to miss
            posts that were made between the time the bot last ran, and the time
            the old post was reinstated. 

            Consider adding a common sense flag: if the time between two submissions
            is irradically greater than the average, and some second flag to check 
            anticipated old aged posts, then check the next post in the sorted by
            newest list. Super low priority though, it's a rare issue
            '''
            break
        #try:
        #    print(submission.title)
        #except: 
        #    pass
        submissionList[submission.id] = [submission]
        user = reddit.redditor(submission.author.name)
        submissionList[submission.id].append(user)


    # Archive and filter out posts that are too old 

    return submissionList

def getUserPosts(user, limitCount=25, ageLimitHours=None, ageLimitTime=None):
    # Post or Submission depending on documentation, same thing
    '''
    Grabs users most recent submissions, up to either a count limit, back a 
    specific number of hours in the past, or back to a specific time.
    '''
    submissionList = []
    for submission in user.submissions.new(limit=limitCount):
        submissionList.append(submission)
    return submissionList

def getUsersComments(user, limitCount=25):
    # most recent `limitCount` comments by this user
    commentList = []
    for comment in user.comments.new(limit=limitCount):
        commentList.append(comment)
    return commentList




def getTopLevelComments(submission):
    # Of a submission
    return submission.comments

def getAllComments(submission):
    # Of a submission
    submission.comments.replace_more(limit=None)
    return submission.comments.list()



# ~~~~~~~ reddit bot database files: less general reddit stuff ~~~~~~~~~ #


def startupDatabase():
    dirName = "redditData"
    postCommentedOn = "postHistory.txt"
    usersInteractedWith = "UsernamessList.txt"
    submissionDBName = "PLACEHOLDER"

    # Ensure all databases are built
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    fl = open(os.path.join(dirName, usersInteractedWith), 'a')
    fl.close()
    fl = open(os.path.join(dirName, postCommentedOn), 'a')
    fl.close()


    # Load comment history and user interaction history
    userNames = []
    fl = open(os.path.join(dirName, usersInteractedWith), 'r')
    for line in fl:
        userNames.append(line.strip())
    fl.close()

    postHistory = []
    fl = open(os.path.join(dirName, postCommentedOn), 'r')
    for line in fl:
        postHistory.append(line.strip())
    fl.close()

    return userNames, postHistory


def updateUserNameDB(username):
    dirName = "redditData"
    usersInteractedWith = "UsernamessList.txt"
    fl = open(os.path.join(dirName, usersInteractedWith), 'a')
    fl.write(str(username)+'\n')
    fl.close()
    return


def updateDatabase(username, post_id):
    # Right now it's a flat database, soon it'll be not so flat 
    dirName = "redditData"
    postCommentedOn = "postHistory.txt"
    usersInteractedWith = "UsernamessList.txt"
    
    
    fl = open(os.path.join(dirName, usersInteractedWith), 'a')
    fl.write(str(username)+'\n')
    fl.close()
    fl = open(os.path.join(dirName, postCommentedOn), 'a')
    fl.write(str(post_id)+'\n')
    fl.close()
    
    return
    


def saveSubmissions(submission, database):
    # Check if database has been created, if no
    # Create DB

    
    # Into database save submission keyfeatures:
    

    return



def removeOldPosts(submissionList, ageLimitHours):
    
    popList = []
    for key in submissionList:
        submission, user = submissionList[key]
        if datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(submission.created_utc) > datetime.timedelta(hours=ageLimitHours):
            # Archive post
            # TODO
            # Pop it!
            popList.append(key)
    for popit in popList:
        temp = submissionList.pop(popit)
        pass

    return submissionList


def updatePostFeatures(reddit, submissionList={}):
    # Update the info for all submissions
    # TODO: If post is deleted or removed, only update 
    #   votes info, 
    for key in submissionList:
        #submission, user = submissionList[key]
        # Check if post and user has been deleted or removed

        submissionList[key][0] = reddit.submission(id=key)


    return submissionList

def archiveAndRemoveOldSubmissions(reddit, submissionList={}):

    return


# ~~~~~~~~~ Monitoring and Metrics ~~~~~~~~~~ # 

def makeCommentKarmaReport(user):
    karma = []
    date = []  
    commentList = getUsersComments(user, limitCount=1000)
    for comment in commentList:
        karma.append(comment.score)
        timestamp = datetime.datetime.utcfromtimestamp(comment.created_utc)
        date.append(timestamp)
    return date, karma

def checkForMessages(reddit):
    inboxMessages = []
    for msg in reddit.inbox.unread():
        inboxMessages.append(msg)
    return inboxMessages
    
