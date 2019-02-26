
import time
import datetime
import praw
from praw.exceptions import APIException
from prawcore import RequestException, ResponseException, ServerError
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
    def __init__(self, praw_sub):
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
                    self.author = praw_sub.author.name
                except AttributeError:
                    # Author has deleted the post or been removed and can't be identified
                    self.author = '[deleted]'
                self.created_utc = datetime.datetime.utcfromtimestamp(praw_sub.created_utc)
                self.id = praw_sub.id
                self.url = praw_sub.url
                self.score = praw_sub.score
                self.upvote_ratio =  praw_sub.upvote_ratio
                self.title = praw_sub.title
                self.selftext = praw_sub.selftext
                self.subreddit = praw_sub.subreddit.display_name
                self.link_flair_text = praw_sub.link_flair_text
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
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = self._backoff(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
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
                praw_sub = reddit.submission(id=self.id)
                now = datetime.datetime.utcnow()
                self.edited = praw_sub.edited
                self.score = praw_sub.score
                self.upvote_ratio =  praw_sub.upvote_ratio
                self.link_flair_text = praw_sub.link_flair_text
                if self.selftext != praw_sub.selftext:
                    self.edit_History.append(self.selftext)
                    self.selftext = praw_sub.selftext
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
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = self._backoff(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
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

    def get_top_level_comments(self, reddit):
        
        # Prep for errors
        maxTotalWaitTime = 5*60*60
        requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
        serverBackoffTime = 5 
        maxBackoffTime = 5*60
        startTime = time.time()
        
        vals_Assigned = False
        while True:
            if vals_Assigned:
                break
            try:
                praw_sub = reddit.submission(id=self.id)
                commentList = praw_sub.comments
                reclassedComments = []
                for comment in commentList:
                    reclassedComments.append(phb_Reddit_Comment(comment))
                vals_Assigned = True
                break

            except RequestException as e:
                logging.error("Caught Server Rate Limit Hit | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = self._backoff(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = self._backoff(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
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


        # Of a submission
        return reclassedComments

    def get_all_comments(self, reddit):
        
        # Prep for errors
        maxTotalWaitTime = 5*60*60
        requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
        serverBackoffTime = 5 
        maxBackoffTime = 5*60
        startTime = time.time()

        vals_Assigned = False
        while True:
            if vals_Assigned:
                break
            try:
                praw_sub = reddit.submission(id=self.id)
                commentList = praw_sub.comments.replace_more(limit=None)
                reclassedComments = []
                for comment in commentList.list():
                    reclassedComments.append(phb_Reddit_Comment(comment))
                vals_Assigned = True
                break

            except RequestException as e:
                logging.error("Caught Server Rate Limit Hit | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = self._backoff(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = self._backoff(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
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


        # Of a submission
        return reclassedComments

class phb_Reddit_Comment(object):
    '''
    Build local structure to save reddit data, only 
    be concerned with useful information, drop all else

    phb stands for Python Helper Bot

    God I hope this takes care of most reddit based errors
    I hope this acts like a padded room for the insanity that is reddit errors
    '''
    def __init__(self, praw_comment):
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
                    self.author = praw_comment.author.name
                except AttributeError:
                    # Author has deleted the post or been removed and can't be identified
                    self.author = '[deleted]'
                self.created_utc = datetime.datetime.utcfromtimestamp(praw_comment.created_utc)
                self.body = praw_comment.body
                self.id = praw_comment.id
                self.is_submitter = praw_comment.is_submitter
                self.link_id = praw_comment.link_id
                self.parent_id = praw_comment.parent_id
                self.url = praw_comment.permalink
                self.score = praw_comment.score
                self.subreddit = praw_comment.subreddit.display_name
                self.score_History = [[self.score, now]]
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
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = self._backoff(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
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
                praw_comment = reddit.comment(id=self.id)
                now = datetime.datetime.utcnow()
                self.edited = praw_comment.edited
                self.score = praw_comment.score
                if self.body != praw_comment.body:
                    self.edit_History.append(self.body)
                    self.body = praw_comment.body
                self.score_History.append([self.score, now])
                vals_Assigned = True
                break

            except RequestException as e:
                logging.error("Caught Server Rate Limit Hit | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = self._backoff(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = self._backoff(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
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
        msg = "Comment by "+ self.author
        msg += "\nScore:  " + str(self.score)
        msg += "\nID: " + str(self.id)
        msg += "\nURL: " + str(self.url)
        msg += "\nSelfText:\n" + str(self.body)
        return msg
    def __repr__(self):
        return self._print_Full()

    #def get_top_level_comments(self, sub):

    #def get_all_comments(self, sub):

class phb_Reddit_User(object):
    '''
    Build local structure to save reddit data, only 
    be concerned with useful information, drop all else

    phb stands for Python Helper Bot

    God I hope this takes care of most reddit based errors
    I hope this acts like a padded room for the insanity that is reddit errors
    '''
    def __init__(self, praw_user):

        vals_Assigned = False
        self.directed_to_learning_sub = False
        self.said_thanks_or_it_worked = False
        
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
                    self.name = praw_user.name
                except AttributeError:
                    # Author has deleted the post or been removed and can't be identified
                    self.author = '[deleted]'
                self.created_utc = datetime.datetime.utcfromtimestamp(praw_user.created_utc)
                self.id = praw_user.id
                self.link_karma = praw_user.link_karma
                self.comment_karma = praw_user.comment_karma
                vals_Assigned = True
                break
            except RequestException as e:
                logging.error("Caught Server Rate Limit Hit | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = self._backoff(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = self._backoff(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
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

    def getUserPosts(self, reddit, limitCount=25, ageLimitHours=None, ageLimitTime=None):
        # Post or Submission depending on documentation, same thing
        '''
        Grabs users most recent submissions, up to either a count limit, back a 
        specific number of hours in the past, or back to a specific time.
        '''

        vals_Assigned = False
        
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
                submissionList = []
                praw_user = reddit.redditor(self.name)
                for submission in praw_user.submissions.new(limit=limitCount):
                    sub = phb_Reddit_Submission(submission)
                    submissionList.append(sub)
                return submissionList
                
                vals_Assigned = True
                break
            except RequestException as e:
                logging.error("Caught Server Rate Limit Hit | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = self._backoff(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = self._backoff(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
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


    def getUsersComments(self, reddit, limitCount=25):
        # most recent `limitCount` comments by this user
        
        vals_Assigned = False
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
                commentList = []
                praw_user = reddit.redditor(self.name)
                for comment in praw_user.comments.new(limit=limitCount):
                    comment = phb_Reddit_Comment(comment)
                    commentList.append(comment)                
                vals_Assigned = True
                break
            except RequestException as e:
                logging.error("Caught Server Rate Limit Hit | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = self._backoff(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = self._backoff(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
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

        return commentList

class phb_Reddit_Msg(object):
    '''
    Build local structure to save reddit data, only 
    be concerned with useful information, drop all else

    phb stands for Python Helper Bot

    God I hope this takes care of most reddit based errors
    I hope this acts like a padded room for the insanity that is reddit errors
    '''
    def __init__(self, praw_msg):
        # Prep for errors
        maxTotalWaitTime = 5*60*60
        requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
        serverBackoffTime = 5 
        maxBackoffTime = 5*60
        startTime = time.time()

        vals_Assigned = False
        while True:
            if vals_Assigned:
                break
            try:
                # ********************************
                now = datetime.datetime.utcnow()
                try:
                    self.author = praw_msg.author.name
                except AttributeError:
                    # Author has deleted the post or been removed and can't be identified
                    self.author = '[deleted]'
                self.body = praw_msg.body
                self.created_utc = datetime.datetime.utcfromtimestamp(praw_msg.created_utc)
                self.id = praw_msg.id
                self.subject = praw_msg.subject
                self.was_comment = praw_msg.was_comment
                try:
                    self.subreddit = praw_msg.subreddit.display_name
                except AttributeError:
                    self.subreddit = None
                # ********************************
                vals_Assigned = True
                break
            except RequestException as e:
                logging.error("Caught Server Rate Limit Hit | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = self._backoff(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = self._backoff(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
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

def get_redditor_by_name(reddit, name):
    
    # Prep for errors
    maxTotalWaitTime = 5*60*60
    requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
    serverBackoffTime = 5 
    maxBackoffTime = 5*60
    startTime = time.time()

    vals_Assigned = False

    while True:
        if vals_Assigned:
            break
        try:
            # ********************************
            user = phb_Reddit_User(reddit.redditor(name))
            # ********************************
            vals_Assigned = True
            break
        except RequestException as e:
            logging.error("Caught Server Rate Limit Hit | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
            if time.time()-startTime > maxTotalWaitTime:
                logging.error("I've tried this too much, escalating error")
                raise e
        except APIException as e:
            if "RATELIMIT" in traceback.format_exc():
                logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            else:
                raise e
        except (ServerError, ResponseException) as e:
            logging.error("Caught Server 500 Error | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            serverBackoffTime = _backoff_Sleeper(serverBackoffTime)
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

    return user
def get_comment_by_ID(reddit, comment_id):
    
    # Prep for errors
    maxTotalWaitTime = 5*60*60
    requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
    serverBackoffTime = 5 
    maxBackoffTime = 5*60
    startTime = time.time()

    vals_Assigned = False

    while True:
        if vals_Assigned:
            break
        try:
            # ********************************
            comment = phb_Reddit_Comment(reddit.comment(id=comment_id))
            # ********************************
            vals_Assigned = True
            break
        except RequestException as e:
            logging.error("Caught Server Rate Limit Hit | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
            if time.time()-startTime > maxTotalWaitTime:
                logging.error("I've tried this too much, escalating error")
                raise e
        except APIException as e:
            if "RATELIMIT" in traceback.format_exc():
                logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            else:
                raise e
        except (ServerError, ResponseException) as e:
            logging.error("Caught Server 500 Error | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            serverBackoffTime = _backoff_Sleeper(serverBackoffTime)
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

    return comment
def get_submission_by_ID(reddit, submission_id):
    
    # Prep for errors
    maxTotalWaitTime = 5*60*60
    requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
    serverBackoffTime = 5 
    maxBackoffTime = 5*60
    startTime = time.time()

    vals_Assigned = False

    while True:
        if vals_Assigned:
            break
        try:
            # ********************************
            submission = phb_Reddit_Submission(reddit.submission(id=submission_id))
            # ********************************
            vals_Assigned = True
            break
        except RequestException as e:
            logging.error("Caught Server Rate Limit Hit | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
            if time.time()-startTime > maxTotalWaitTime:
                logging.error("I've tried this too much, escalating error")
                raise e
        except APIException as e:
            if "RATELIMIT" in traceback.format_exc():
                logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            else:
                raise e
        except (ServerError, ResponseException) as e:
            logging.error("Caught Server 500 Error | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            serverBackoffTime = _backoff_Sleeper(serverBackoffTime)
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

    return submission
        
def _backoff_Sleeper(backoffTime, maxBackoffTime = 5*60):
    backoffTime = min(backoffTime, maxBackoffTime)
    time.sleep(backoffTime)
    return backoffTime*2

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


def commentOnSubmmission(submission, msg, reddit, quietMode):
    # Post message to reddit submission
    #testingsubmissionID = '8nvbf3'
    # Prep for errors
    maxTotalWaitTime = 5*60*60
    requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
    serverBackoffTime = 5 
    maxBackoffTime = 5*60
    startTime = time.time()

    vals_Assigned = False

    if not quietMode:
        while True:
            if vals_Assigned:
                break
            try:
                # ********************************
                submission = reddit.submission(id=submission.id)
                submission.reply(msg)
                # ********************************
                vals_Assigned = True
                break
            except RequestException as e:
                logging.error("Caught Server Rate Limit Hit | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
                logging.error("Caught Server 500 Error | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                serverBackoffTime = _backoff_Sleeper(serverBackoffTime)
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
    else:
        logging.debug("Quiet Mode is active, Comment On Submission Ignored")

    return

def commentOnComment(comment, msg, reddit, quietMode):
    
    # Prep for errors
    maxTotalWaitTime = 5*60*60
    requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
    serverBackoffTime = 5 
    maxBackoffTime = 5*60
    startTime = time.time()

    vals_Assigned = False


    if not quietMode: 
        while True:
            if vals_Assigned:
                break
            try:
                # ********************************
                comment = reddit.comment(id=comment.id)
                comment.reply(msg)
                # ********************************
                vals_Assigned = True
                break
            except RequestException as e:
                logging.error("Caught Server Rate Limit Hit | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            except APIException as e:
                if "RATELIMIT" in traceback.format_exc():
                    logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                    logging.error("\n"+traceback.format_exc())
                    requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                else:
                    raise e
            except (ServerError, ResponseException) as e:
                logging.error("Caught Server 500 Error | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                serverBackoffTime = _backoff_Sleeper(serverBackoffTime)
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
    else:
        logging.debug("Quiet Mode is active, Comment On Comment Ignored")
        
    return


def getNewPosts(reddit, sub="python", submissionList={}, ageLimitHours=12):
    
    # Prep for errors
    maxTotalWaitTime = 5*60*60
    requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
    serverBackoffTime = 5 
    maxBackoffTime = 5*60
    startTime = time.time()

    vals_Assigned = False

    while True:
        if vals_Assigned:
            break
        try:


            # ********************************
            # Find new posts
            subreddit = reddit.subreddit(sub)
            for submission in subreddit.new(limit=40):
                if submission.id in submissionList:
                    #print('Already In List')
                    break
                # This submission isn't cast into a phb_sub class until after I know it's worth it. Might not be a good idea..
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
                time.sleep(1) # Try to reduce rate limit issues
                submissionList[submission.id] = [phb_Reddit_Submission(submission)]
                user = phb_Reddit_User(reddit.redditor(submission.author.name))
                submissionList[submission.id].append(user)
            # ********************************

            vals_Assigned = True
            break
        except RequestException as e:
            logging.error("Caught Server Rate Limit Hit | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
            if time.time()-startTime > maxTotalWaitTime:
                logging.error("I've tried this too much, escalating error")
                raise e
        except APIException as e:
            if "RATELIMIT" in traceback.format_exc():
                logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            else:
                raise e
        except (ServerError, ResponseException) as e:
            logging.error("Caught Server 500 Error | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            serverBackoffTime = _backoff_Sleeper(serverBackoffTime)
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

    # Archive and filter out posts that are too old 

    return submissionList

def grabAndUpdateNewPosts(reddit, sub="python", submissionList={}, ageLimitHours=12):
    submissionList = removeOldPosts(submissionList, ageLimitHours)
    submissionList = updatePostFeatures(reddit, submissionList)

    submissionList = getNewPosts(reddit, sub="python", submissionList={}, ageLimitHours=12)
    return submissionList

def updatePosts(reddit, sub="python", submissionList={}, ageLimitHours=12):
    submissionList = removeOldPosts(submissionList, ageLimitHours)
    submissionList = updatePostFeatures(reddit, submissionList)
    return submissionList

    
def updateYoungerThanXPosts(reddit, sub="python", submissionList={}, ageLimitHours=2):
    '''
    Function exists so only a set of posts are updated where the set is defined by
    their age. 
    '''

    # Splitting into younger/older than
    holdSubmissions = {}
    newSubmissions = {}
    for key in submissionList:
        submission, user = submissionList[key]
        if datetime.datetime.utcnow() - submission.created_utc > datetime.timedelta(hours=ageLimitHours):
            holdSubmissions[key] = submissionList[key]
        else:
            newSubmissions[key] = submissionList[key]
    # The actual Update
    newSubmissions = updatePostFeatures(reddit, newSubmissions)
    # Merging Back Together
    for key in newSubmissions:
        holdSubmissions[key] = newSubmissions[key]

    return holdSubmissions


# ~~~~~~~~~ Monitoring and Metrics ~~~~~~~~~~ # 



def makeCommentKarmaReport(user, reddit):
    karma = []
    date = []  
    #commentList = getUsersComments(user, limitCount=1000)
    commentList = user.getUsersComments(reddit, limitCount=1000)
    for comment in commentList:
        karma.append(comment.score)
        timestamp = comment.created_utc
        date.append(timestamp)
    return date, karma

def checkForMessages(reddit):
    # Change to isolated msg class

    # Prep for errors
    maxTotalWaitTime = 5*60*60
    requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
    serverBackoffTime = 5 
    maxBackoffTime = 5*60
    startTime = time.time()

    vals_Assigned = False

    while True:
        if vals_Assigned:
            break
        try:
            # ********************************
            inboxMessages = []
            for msg in reddit.inbox.unread():
                time.sleep(1) # Try to reduce rate limit issues
                rfmsg = phb_Reddit_Msg(msg)
                inboxMessages.append(rfmsg)
            # ********************************

            vals_Assigned = True
            break
        except RequestException as e:
            logging.error("Caught Server Rate Limit Hit | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
            if time.time()-startTime > maxTotalWaitTime:
                logging.error("I've tried this too much, escalating error")
                raise e
        except APIException as e:
            if "RATELIMIT" in traceback.format_exc():
                logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            else:
                raise e
        except (ServerError, ResponseException) as e:
            logging.error("Caught Server 500 Error | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            serverBackoffTime = _backoff_Sleeper(serverBackoffTime)
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

    return inboxMessages
    

def markSummonsAsReadMessages(reddit, msgIDs = []):
    # Change to isolated msg class

    # Prep for errors
    maxTotalWaitTime = 5*60*60
    requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
    serverBackoffTime = 5 
    maxBackoffTime = 5*60
    startTime = time.time()

    vals_Assigned = False

    while True:
        if vals_Assigned:
            break
        try:
            # ********************************
            for msg in reddit.inbox.unread():
                time.sleep(1) # Try to reduce rate limit issues
                if msg.id in msgIDs:
                    msg.mark_read()
            # ********************************

            vals_Assigned = True
            break
        except RequestException as e:
            logging.error("Caught Server Rate Limit Hit | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
            if time.time()-startTime > maxTotalWaitTime:
                logging.error("I've tried this too much, escalating error")
                raise e
        except APIException as e:
            if "RATELIMIT" in traceback.format_exc():
                logging.error("Caught Server Rate Limit Hit By API | Specific Error:")
                logging.error("\n"+traceback.format_exc())
                requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
                if time.time()-startTime > maxTotalWaitTime:
                    logging.error("I've tried this too much, escalating error")
                    raise e
            else:
                raise e
        except (ServerError, ResponseException) as e:
            logging.error("Caught Server 500 Error | Specific Error:")
            logging.error("\n"+traceback.format_exc())
            serverBackoffTime = _backoff_Sleeper(serverBackoffTime)
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

    return 
    


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
        if datetime.datetime.utcnow() - submission.created_utc > datetime.timedelta(hours=ageLimitHours):
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
        submission, user = submissionList[key]
        submission.update_info(reddit)
        submissionList[key] = [submission, user]
        # Check if post and user has been deleted or removed

        #submissionList[key][0] = reddit.submission(id=key)


    return submissionList

def archiveAndRemoveOldSubmissions(reddit, submissionList={}):

    return

