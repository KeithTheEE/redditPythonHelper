
import time
import datetime
import praw
from praw.exceptions import APIException
from prawcore import RequestException, ResponseException, ServerError
from asecretplace import getPythonHelperBotKeys
import sqlite3
import json
import os
import logging
import subprocess
import traceback
import socket
from shutil import copyfile

import kmlistfi

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
    def __init__(self, praw_sub, loaded_dict=None):
        if loaded_dict == None:
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
                    self.num_comments = praw_sub.num_comments
                    self.link_flair_text = praw_sub.link_flair_text
                    self.score_History = [[self.score, self.upvote_ratio, self.num_comments, now]]
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
        else:
            self.directed_to_learning_sub = False
            self.mod_removed_for_learning = False
            self.said_thanks_or_it_worked = False
            self.deleted_or_removed = False
            self.load_from_dict(loaded_dict)

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
                self.num_comments = praw_sub.num_comments
                if self.selftext != praw_sub.selftext:
                    self.edit_History.append(self.selftext)
                    self.selftext = praw_sub.selftext
                self.score_History.append([self.score, self.upvote_ratio, self.num_comments, now])
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


    def make_shortlink(self):
        return 'https://redd.it/'+self.id

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
                praw_sub.comments.replace_more(limit=None) # Loads all comments
                reclassedComments = []
                for comment in praw_sub.comments.list():
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

    def export_to_dict(self):
        submission_d = {}
        submission_d['author'] = self.author
        submission_d['created_utc'] = self.created_utc
        submission_d['id'] = self.id
        submission_d['url'] = self.url
        submission_d['score'] = self.score
        submission_d['upvote_ratio'] = self.upvote_ratio 
        submission_d['title'] = self.title 
        submission_d['selftext'] = self.selftext 
        submission_d['subreddit'] = self.subreddit 
        submission_d['num_comments'] = self.num_comments 
        submission_d['link_flair_text'] = self.link_flair_text 
        submission_d['score_History'] = self.score_History 
        submission_d['edit_History'] = self.edit_History 
        return submission_d
    def load_from_dict(self, submission_d):
        '''
        This currently does not have protections under the assumption that if 
        there is a keyerror, it needs to be raised
        '''
        self.author = submission_d['author'] 
        self.created_utc = submission_d['created_utc'] 
        self.id = submission_d['id'] 
        self.url = submission_d['url'] 
        self.score = submission_d['score'] 
        self.upvote_ratio = submission_d['upvote_ratio'] 
        self.title = submission_d['title'] 
        self.selftext = submission_d['selftext'] 
        self.subreddit = submission_d['subreddit'] 
        self.num_comments = submission_d['num_comments'] 
        self.link_flair_text = submission_d['link_flair_text'] 
        self.score_History = submission_d['score_History'] 
        self.edit_History = submission_d['edit_History'] 
        return
        


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


    def export_to_dict(self):
        comment_d = {}
        comment_d['author'] = self.author
        comment_d['created_utc'] = self.created_utc
        comment_d['body'] = self.body 
        comment_d['id'] = self.id
        comment_d['is_submitter'] = self.is_submitter
        comment_d['link_id'] = self.link_id
        comment_d['parent_id'] = self.parent_id
        comment_d['url'] = self.url
        comment_d['score'] = self.score
        comment_d['subreddit'] = self.subreddit
        comment_d['score_History'] = self.score_History 
        comment_d['edit_History'] = self.edit_History 
        return comment_d
    def load_from_dict(self, comment_d):
        '''
        This currently does not have protections under the assumption that if 
        there is a keyerror, it needs to be raised
        '''
        self.author = comment_d['author'] 
        self.created_utc = comment_d['created_utc'] 
        self.body = comment_d['body']
        self.id = comment_d['id'] 
        self.is_submitter = comment_d['is_submitter']
        self.link_id = comment_d['link_id']
        self.parent_id = comment_d['parent_id']
        self.url = comment_d['url'] 
        self.score = comment_d['score'] 
        self.subreddit = comment_d['subreddit'] 
        self.score_History = comment_d['score_History'] 
        self.edit_History = comment_d['edit_History'] 
        return
        

class phb_Reddit_User(object):
    '''
    Build local structure to save reddit data, only 
    be concerned with useful information, drop all else

    phb stands for Python Helper Bot

    God I hope this takes care of most reddit based errors
    I hope this acts like a padded room for the insanity that is reddit errors
    '''


    '''
Error Caused by User Account that was deleted while the bot was looking at/for it. 
Rare, but should be handled 

2019-02-28 08:08:49,848 - DEBUG - main.py:getReadyToComment():186 - Processing a valid post
2019-02-28 08:08:49,848 - DEBUG - botHelperFunctions.py:logPostFeatures():54 - **************************************************
2019-02-28 08:08:49,849 - DEBUG - botHelperFunctions.py:logPostFeatures():55 - [POST]   | what is python?
2019-02-28 08:08:49,849 - DEBUG - botHelperFunctions.py:logPostFeatures():56 - [AUTHOR] | shiriyadav
2019-02-28 08:08:49,849 - DEBUG - botHelperFunctions.py:logPostFeatures():57 - [ID]     | avnkh8
2019-02-28 08:08:49,849 - DEBUG - botHelperFunctions.py:logPostFeatures():59 -  Post Age: 2:14:43.849659
2019-02-28 08:08:49,849 - DEBUG - botHelperFunctions.py:logPostFeatures():60 -  Votes: 0
2019-02-28 08:08:49,850 - DEBUG - botHelperFunctions.py:logPostFeatures():61 -  Upvote Ratio: 0.1
2019-02-28 08:08:49,850 - DEBUG - sessions.py:_log_request():49 - Fetching: GET https://oauth.reddit.com/comments/avnkh8/
2019-02-28 08:08:49,851 - DEBUG - sessions.py:_log_request():50 - Data: None
2019-02-28 08:08:49,851 - DEBUG - sessions.py:_log_request():51 - Params: {'sort': 'best', 'raw_json': 1, 'limit': 2048}
2019-02-28 08:08:50,014 - DEBUG - connectionpool.py:_make_request():393 - https://oauth.reddit.com:443 "GET /comments/avnkh8/?sort=best&raw_json=1&limit=2048 HTTP/1.1" 200 1526
2019-02-28 08:08:50,018 - DEBUG - sessions.py:_make_request():100 - Response: 200 (1526 bytes)
2019-02-28 08:08:50,024 - DEBUG - sessions.py:_log_request():49 - Fetching: GET https://oauth.reddit.com/user/shiriyadav/submitted
2019-02-28 08:08:50,024 - DEBUG - sessions.py:_log_request():50 - Data: None
2019-02-28 08:08:50,024 - DEBUG - sessions.py:_log_request():51 - Params: {'sort': 'new', 'raw_json': 1, 'limit': 25}
2019-02-28 08:08:50,261 - DEBUG - connectionpool.py:_make_request():393 - https://oauth.reddit.com:443 "GET /user/shiriyadav/submitted?sort=new&raw_json=1&limit=25 HTTP/1.1" 404 38
2019-02-28 08:08:50,265 - DEBUG - sessions.py:_make_request():100 - Response: 404 (38 bytes)
2019-02-28 08:08:50,265 - ERROR - archiveAndUpdateReddit.py:getUserPosts():618 - Caught Server 500 Error | Specific Error:
2019-02-28 08:08:50,277 - ERROR - archiveAndUpdateReddit.py:getUserPosts():619 -
Traceback (most recent call last):
  File "/home/pi/Documents/filesForProgramming/Reddit/pythonHelpBot2/utils/archiveAndUpdateReddit.py", line 593, in getUserPosts
    for submission in praw_user.submissions.new(limit=limitCount):
  File "/usr/local/lib/python2.7/dist-packages/praw/models/listing/generator.py", line 80, in next
    return self.__next__()
  File "/usr/local/lib/python2.7/dist-packages/praw/models/listing/generator.py", line 52, in __next__
    self._next_batch()
  File "/usr/local/lib/python2.7/dist-packages/praw/models/listing/generator.py", line 62, in _next_batch
    self._listing = self._reddit.get(self.url, params=self.params)
  File "/usr/local/lib/python2.7/dist-packages/praw/reddit.py", line 371, in get
    data = self.request('GET', path, params=params)
  File "/usr/local/lib/python2.7/dist-packages/praw/reddit.py", line 486, in request
    params=params)
  File "/usr/local/lib/python2.7/dist-packages/prawcore/sessions.py", line 182, in request
    params=params, url=url)
  File "/usr/local/lib/python2.7/dist-packages/prawcore/sessions.py", line 127, in _request_with_retries
    raise self.STATUS_EXCEPTIONS[response.status_code](response)
NotFound: received 404 HTTP response



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
                    self.name = '[deleted]'
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

        Check for ban error
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
                    if (ageLimitHours != None) or (ageLimitTime != None):
                        if ageLimitHours != None:
                            if datetime.datetime.utcnow() - sub.created_utc > datetime.timedelta(hours=ageLimitHours):
                                break
                        if ageLimitTime != None:
                            if sub.created_utc < ageLimitTime:
                                # This does assume age limit time is give in utc
                                break
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
        return submissionList


    def getUsersComments(self, reddit, limitCount=25, ageLimitHours=None, ageLimitTime=None):
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
                    if (ageLimitHours != None) or (ageLimitTime != None):
                        if ageLimitHours != None:
                            if datetime.datetime.utcnow() - comment.created_utc > datetime.timedelta(hours=ageLimitHours):
                                break
                        if ageLimitTime != None:
                            if comment.created_utc < ageLimitTime:
                                # This does assume age limit time is give in utc
                                break
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

    if '_' in comment_id:
        comment_id = comment_id.split('_')[-1]

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


def comment_duplication_by_ratelimit_check(reddit, submission):
    '''
    Repurpose this to check the submission, not bots history

    This is a bodge check to see if the bots comment went through
    and was posted despite catching a ratelimit error which directed
    the bot to try again

    See issue 
    https://github.com/CrakeNotSnowman/redditPythonHelper/issues/1#issue-473053676
    '''
    timeDelay = 60 # seconds
    logging.debug("Got Rate Limit Error, Waiting and checking if comment went through")
    time.sleep(timeDelay)
    #phbot = get_redditor_by_name(reddit, 'pythonHelperBot')
    # comments = phbot.getUsersComments(reddit, limitCount=2)
    # Turns out this problem doesn't update the bots submissions, and just
    # lives on the submission page
    user_name = 'pythonHelperBot'
    comments = submission.get_top_level_comments(reddit)
    already_commented = False
    comments_by_bot = []
    for comment in comments:
        # comments link id begins with 't3_'
        # formatted_Cid = comment.link_id.split('_')[-1]
        # if  formatted_Cid == submission.id:
        #     already_commented = True
        # Under phb_Reddit_Comment, comment.author = praw_comment.author.name
        # This prevents accedientally passing around the author class 
        if comment.author == user_name:
            comments_by_bot.append(comment)
            already_commented = True
        logging.info("Commenters User Names: "+str(comment.author))


    if already_commented:
        logging.info("Comment went through despite error message")
        if len(comments_by_bot)>1:
            logging.error("recorded " + str(len(comments_by_bot) ) + " comments")
    else:
        logging.info("After " +str(timeDelay)+ " seconds the comment was not registered")

    return already_commented


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
                    logging.error("Submission ID: " + str(submission.id))
                    # Bodge
                    already_commented = comment_duplication_by_ratelimit_check(reddit, submission)
                    if already_commented:
                        vals_Assigned = True
                        break
                    requestBackoffTime = _backoff_Sleeper(requestBackoffTime)
                    if time.time()-startTime > maxTotalWaitTime:
                        logging.error("I've tried this too much, escalating error")
                        raise e
                    # Temp Patch: Bodge is failing 
                    if vals_Assigned == False:
                        logging.warning("Bypassing this block, auto assuming bot has commented, and server is having issues")
                        vals_Assigned = True
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
                try:
                    post = phb_Reddit_Submission(submission)
                    user = phb_Reddit_User(reddit.redditor(submission.author.name))
                    submissionList[submission.id] = [post, user]
                except AttributeError as e:
                    "User Probably deleted the post before the bot got to it | Specific Error:"
                    logging.error("\n"+traceback.format_exc())
                # submissionList[submission.id] = [phb_Reddit_Submission(submission)]
                # user = phb_Reddit_User(reddit.redditor(submission.author.name))
                # submissionList[submission.id].append(user)
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

def grabAndUpdateNewPosts(reddit,  phbArcPaths={}, sub="python", submissionList={}, ageLimitHours=12):
    submissionList = removeOldPosts(reddit, submissionList, ageLimitHours,  phbArcPaths=phbArcPaths,)
    submissionList = updatePostFeatures(reddit, submissionList)

    submissionList = getNewPosts(reddit, sub="python", submissionList={}, ageLimitHours=12)
    return submissionList

def updatePosts(reddit,  phbArcPaths={},  sub="python", submissionList={}, ageLimitHours=12):
    submissionList = removeOldPosts(reddit, submissionList, ageLimitHours,  phbArcPaths=phbArcPaths)
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

def getMods(reddit, sub="python"):
    
    maxTotalWaitTime = 5*60*60
    requestBackoffTime = 60 # starting amount of time required to wait after an error. it will then double
    serverBackoffTime = 5 
    startTime = time.time()

    vals_Assigned = False

    while True:
        if vals_Assigned:
            break
        try:
            mods = []
            for mod in reddit.subreddit(sub).moderator():
                mods.append(phb_Reddit_User(mod))
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
    return mods
    
# ~~~~~~~~~ Monitoring and Metrics ~~~~~~~~~~ # 



def makeCommentKarmaReport(user, reddit):
    # Deprecate soon
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

def joinAndMakeDir(parent, child):
    newDir = os.path.join(parent, child)
    if not os.path.exists(newDir):
        os.makedirs(newDir)
        logging.info("Making new directory: " + newDir)
    return newDir

def createFile(flpath, flname):
    fullflname = os.path.join(flpath, flname)
    fl = open(fullflname, 'a')
    fl.close()
    return fullflname

def getFLSize(flpath):
    return os.path.getsize(flpath)




def startupDatabase(archive_Locations):
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


    archive = archive_Locations[0]
    backup = archive_Locations[1]
    '''
    Archive Structure:
    phbArchive
    |-submissions
    |  |-JSONLike
    |    |-submissions01.qjson
    |    |-submissions02.qjson
    |    ..
    |    |-submissionsn.qjson
    |  |-SQL
    |-submissionsAndComments
    |  |-JSONLike
    |    |-sac01.qjson
    |    |-sac02.qjson
    |    ..
    |    |-sacn.qjson
    |-modActions
    |  |-JSONLike
    |    |-modComments01.qjson
    |    ..
    |-phbActions
    |  |-postHistory.txt
    |  |-summoningHistory.txt
    |  |-UsernameList.txt
    |  |-FullActionSet.txt
    '''
    # phb Archive On Primary Drive:
    #   Builds out archive structure if it doesn't already exist
    phbArchivePath = joinAndMakeDir(archive, 'phbArchive')

    phbSubmissionPath = joinAndMakeDir(phbArchivePath, 'submissions')
    phbSubJsonPath = joinAndMakeDir(phbSubmissionPath, 'JSONLike')
    phbSubSQLPath = joinAndMakeDir(phbSubmissionPath, 'SQL')

    phbSubAndCommentsPath = joinAndMakeDir(phbArchivePath, 'submissionsAndComments')
    phbSubAndComJsonPath = joinAndMakeDir(phbSubAndCommentsPath, 'JSONLike')

    phbModActionsPath = joinAndMakeDir(phbArchivePath, 'modActions')
    phbModActionsJsonPath = joinAndMakeDir(phbModActionsPath, 'JSONLike')

    phbActionsPath = joinAndMakeDir(phbArchivePath, 'phbActions')
    phbScoreDisplay = joinAndMakeDir(phbActionsPath, 'scoreDisplay')

    phbUserRecords = joinAndMakeDir(phbArchivePath, 'users')
    phbUserHistory = joinAndMakeDir(phbUserRecords, 'userInfo')
    phbUserReactions = joinAndMakeDir(phbUserRecords, 'userReactions')

    phbArcPaths ={}
    phbArcPaths['subJson'] = phbSubJsonPath
    phbArcPaths['subSQL'] = phbSubSQLPath
    phbArcPaths['subComJson'] = phbSubAndComJsonPath
    phbArcPaths['modActions'] = phbModActionsPath
    phbArcPaths['modActionsJson'] = phbModActionsJsonPath
    phbArcPaths['phbActionsDir'] = phbActionsPath
    phbArcPaths['phbScoreDisplay']= phbScoreDisplay
    phbArcPaths['userInfo']= phbUserHistory
    phbArcPaths['userReactions']= phbUserReactions



    # Special condition where reddit data was built without arcive present
    # Must make sure the two are equal copies
    if not os.path.isfile(os.path.join(phbArcPaths['phbActionsDir'], postCommentedOn)):
        logging.debug("Copying reddit data to archive location")
        srcPost = os.path.join(dirName, postCommentedOn)
        srcUser = os.path.join(dirName, usersInteractedWith)
        srcSummons = os.path.join(dirName, 'summoningHistory.txt')
        dstPost = os.path.join(phbArcPaths['phbActionsDir'], postCommentedOn)
        dstUser = os.path.join(phbArcPaths['phbActionsDir'], usersInteractedWith)
        dstSummons = os.path.join(phbArcPaths['phbActionsDir'], 'summoningHistory.txt')
        copyfile(srcPost, dstPost)
        copyfile(srcUser, dstUser)
        copyfile(srcSummons, dstSummons)


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

    return userNames, postHistory, phbArcPaths



def updateDatabase(username, post_id, phbArcPaths):
    if phbArcPaths == False:
        # Testing
        return
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

    
    # Archive Location
    fl = open(os.path.join(phbArcPaths['phbActionsDir'], usersInteractedWith), 'a')
    fl.write(str(username)+'\n')
    fl.close()
    fl = open(os.path.join(phbArcPaths['phbActionsDir'], postCommentedOn), 'a')
    fl.write(str(post_id)+'\n')
    fl.close()
    
    return
    
def getModifiedDate(fl):
    return os.stat(fl).st_mtime
def sortFilesByModification(fls):
    return sorted(fls, key=getModifiedDate, reverse=True)

def saveClassJson(class_Struct, database_path, max_MB=10):
    # Check if database has been created, and if there is,
    # check it's size. If too large or if none exist, create DB 
    fls = kmlistfi.les(database_path)
    newFile = False
    if len(fls) == 0:
        youngestFile = createFile(database_path, datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'.json')
        newFile = True
    else:
        youngestFile = sortFilesByModification(fls)[0]
        maxBytes = max_MB* 1024**2 # 10 Mb
        if os.stat(youngestFile).st_size > maxBytes:
            # End old json file with closing bracket
            with open(youngestFile, 'a') as ofl:
                ofl.write('\n]') # Makes file complete json
            youngestFile = createFile(database_path, datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'.json')
            newFile = True

    # Into database save submission keyfeatures:
    jsonText = export_dict_to_json(class_Struct.export_to_dict())

    with open(youngestFile, 'a') as ofl:
        if not newFile:
            ofl.write(',\n')
        else: 
            ofl.write('[\n')
        ofl.write(jsonText)
    

    # I am going to hate myself for this block of code, but the perfect
    #  implementation is never worth it if you never get it written
    return



def removeOldPosts(reddit, submissionList, ageLimitHours, phbArcPaths,  archive=True):

    # Get Archive Location:
    # -Handled at startup
    
    popList = []
    for key in submissionList:
        submission, user = submissionList[key]
        if datetime.datetime.utcnow() - submission.created_utc > datetime.timedelta(hours=ageLimitHours):
            popList.append(key)

    for popit in popList:
        submission, user = submissionList.pop(popit)
        if archive:
            # Submission
            logging.debug("Saving Submission.. " + str(submission.id))
            saveClassJson(submission, phbArcPaths['subJson'])
            # Submission And Comments
            logging.debug("Saving Submission and Comments..")
            saveClassJson(submission, phbArcPaths['subComJson'])
            comments = submission.get_all_comments(reddit)
            for comment in comments:
                saveClassJson(comment, phbArcPaths['subComJson'])
    
    logging.debug("Saving Complete.")


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


## ~ Archive Format Transforms ~ ##

def export_dict_to_json(class_as_dict):
    return json.dumps(class_as_dict, indent=4, sort_keys=True, default=str)



def reDateTimeify_submission(submission_d):
    if 'created_utc' in submission_d:
        print(submission_d['created_utc']) 
        submission_d['created_utc'] = datetime.datetime.strptime(submission_d['created_utc'], "%Y-%m-%d %H:%M:%S")
    if 'score_History' in submission_d:
        for x in submission_d['score_History']:
            x[-1] = datetime.datetime.strptime(x[-1], "%Y-%m-%d %H:%M:%S.%f")
    return submission_d

def load_submission_from_json(jsonDump):
    jsLoad  = json.loads(jsonDump)
    loadedSubD = reDateTimeify_submission(submission_d=jsLoad)
    loadedSubmission = phb_Reddit_Submission(None, loaded_dict=loadedSubD)
    return loadedSubmission
