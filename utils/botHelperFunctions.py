




'''  
Keith Murray 
email: kmurrayis@gmail.com
'''

import logging
import datetime



def get_learning_sub_Names():
    fl = open('misc/learningSubs.txt', 'r')
    subList = []
    for line in fl:
        line = line.strip()
        if 'r/' in line:
            line = line.split('r/')[-1]
        subList.append(line.lower())
    fl.close()
    return subList

def load_autoreply_key_phrases(fl_path):
    fl = open('misc/autoreplyKeyPhrases.txt', 'r')
    phrase_set = []
    for line in fl:
        line = line.strip()
        if line != "":
            phrase_set.append(line.lower())
    fl.close()
    return phrase_set

def shortenRedditURL(url):
    url = url[8:]
    return '/'.join(url.split('/')[:-2])+'/'


def coolPlacesToDonate():
    donationList = []
    # Load websites, randomly suggest one as a good place to donate too
    return

def ramCheck():
    # Return used and available ram for logging 
    return


def logPostFeatures(submission):
    
    logging.debug( '*'*50)
    logging.debug('[POST]   | ' + str(submission.title.encode('ascii', 'ignore')))
    logging.debug('[AUTHOR] | ' + str(submission.author))
    logging.debug('[ID]     | ' + str(submission.id))
    postAge = datetime.datetime.utcnow() - submission.created_utc
    logging.debug(  '\t'+"Post Age: "+ str(postAge) )
    logging.debug(  '\t'+ "Votes: "+ str(submission.score))
    logging.debug(  '\t'+ "Upvote Ratio: "+str( submission.upvote_ratio ))
    return




def user_Already_Took_Advice(submission, postsInLearningSubs, suggestedTime):
    '''
    See whether or not user has posted in learning subs, and distinguish between
    following advice vs just posting in multiple places vs posting in learning 
    subs some time after vs unrelated

    
    Notes
    -----
    This is a bit messy
    The bot balances two users: the average r/python redditor (AR), and the user posting
    the question, OP (original poster).
    To the AR, it doesn't matter that the OP has already posted in the correct sub, it 
    matters that the r/python sub has OP's post. 
    To the OP, it doesn't matter where they post, they want an answer. 
    The Guiding principle is be helpful and don't spam. 
    Considering OP, if they were informed to try somewhere else, and they did, they 
    don't need to be told to do what has already been done. 
    If OP has cross posted as a 'see what sticks' method, they do need to be told to 
    not post here but post similar queries to learning subs. 

    If the bot takes on mod like roles (flagging posts for mod review) then the AR 
    should be the bots first focus. 
    Otherwise
    The bot should care about OP, and try to help. If the bots actions don't add value, 
    the bot should remain inactive. 

    It would be nice to acknowledge if the user has cross posted, but I'm not sure if that 
    would make 
    
    
    '''
    tookAdvice = False
    crossPosted = False
    askedLearningLater = False
    if len(postsInLearningSubs) > 0:
        pythonPostTime = submission.created_utc
        for post in postsInLearningSubs:
            learningPostTime = post.created_utc
            if suggestedTime  != -1:
                if learningPostTime - suggestedTime >  datetime.timedelta(seconds=0):
                    tookAdvice = True
                    logging.info("User took Advice")
            else:
                if abs(learningPostTime - pythonPostTime) < datetime.timedelta(seconds=30*60):
                    crossPosted = True
                    logging.info("User Cross Posted")
                elif learningPostTime- pythonPostTime  > datetime.timedelta(seconds=30*60):
                    askedLearningLater = True
                    
                    logging.info("User posted in learning Sub after a while ")


    return tookAdvice, crossPosted, askedLearningLater


def getSubsUsersInteractsIn(reddit, user, limitCount=25):
    '''
    Effectively a very basic funtion. However, because of the use-case
    it has an added flag to show whether or not the user has previously
    suggested the learnpython sub. 

    This whole function will probably be deleted at a later date for
    more optimized functions including:

    check whether or not user has suggested learnpython before
    check whether or not it has been suggested to them before
    check whether they use any learn programming related subs
    check whether the user makes duplicate posts
    check whether the user posts blog spam

    This incarnation is useful, but it burns api calls for very little 
    gains. 

    
 /r/cpp_questions
 /r/javahelp
 /r/LearnJavaScript
 /r/learnpython
 /r/learnmachinelearning
 /r/MLQuestions
 /r/learnprogramming
    '''
    learning_Subs = botHelperFunctions.get_learning_sub_Names()
    postsInLearningSubs = []
    redditSubs = {}
    submissionList = user.getUserPosts(reddit, limitCount)
    commentList = user.getUsersComments(reddit, limitCount)
    hasSuggestedLearnPython = False


    for submission in submissionList:
        if str(submission.subreddit ) in redditSubs:
            redditSubs[str(submission.subreddit )] += 1
        else:
            redditSubs[str(submission.subreddit )] = 1
        if str(submission.subreddit ).lower() in learning_Subs:
            postsInLearningSubs.append(submission)
        
    for comment in commentList:
        if 'learnpython' in comment.body.lower():
            hasSuggestedLearnPython = True
        if str(comment.subreddit ) in redditSubs:
            redditSubs[str(comment.subreddit )] += 1
        else:
            redditSubs[str(comment.subreddit )] = 1
        
    return redditSubs, hasSuggestedLearnPython, postsInLearningSubs
    