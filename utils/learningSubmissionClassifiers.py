



import nltk
import logging
import datetime


from utils import archiveAndUpdateReddit
from utils import botMetrics
from utils import botHelperFunctions 
from utils import buildComment
from utils import formatCode
from utils import locateDB
from utils import nb_text_classifier
from utils import questionIdentifier
from utils import searchStackOverflowWeb
from utils import summarizeText
from utils import textSupervision
from asecretplace import getPythonHelperBotKeys

'''
Keith Murray
email: kmurrayis@gmail.com

This is not currently intended to be functional. 
This is a place holder to be filled out to clean up the main,

and it's pros and cons are being evaluated.

'''


def request_Key_Word_Classifier(submission, phrase_set):
    '''
    This is a hand made feature set to id titles that make reddit-typical 
    requests for help, but might not phrase the request as a question

    '''    
    text = ' '.join(summarizeText.parseStringSimple01(submission.title))
    # Pass phrase_set through string parser and back, it'll help? 
    #phrase_set = botHelperFunctions.load_autoreply_key_phrases(fl_path='misc/autoreplyKeyPhrases.txt')
    '''
    phrase_set = ['need help', '[help]', '[ help ]', '[question]', 
                    '[ question ]', 'noob ', 'n00b ', ' newb','please help', 
                    'noobie question', 'help!', 'help me', "isn't working",
                    'not working', 'issues with', 'issue with',
                    'looking for tutorial', 'Quick question', 'help needed',
                    'plz help', "what's wrong", "need some help", '[q]',
                    '[Beginner Question]']
    '''
    request_Made = False
    #print text
    for phrase in phrase_set:
        if ' '.join(summarizeText.parseStringSimple01(phrase)).lower() in text:
            logging.info(phrase + " Was used in the post title")
            request_Made = True
            break
    
    #if submission.id not in submission.url:
        # Links off site 
        # This check was not in early versions of the bot (v pa0.1.01 and earlier)
    #    logging.debug(  '\t'+'Results: Error. Classification is dead,  (URL) Mismatch. ')
    #    request_Made = False

    return request_Made




def basicQuestionClassify(submission, classifier):
    """
    A really simple classifier. if a submission is old enough, has low enough votes
    and asks a question, it's treated as a basic question that r/learnpython is 
    better suited for.
    Parameters
    ----------
    submission : praw submission object
    user : praw user object
    classifier : nltk classifier object
    tdm : term document matrix object
    Returns
    -------
     
    Notes
    -----
    It's not what I want, but it'll force me to
    References
    ----------
    Examples
    --------
    """
    #title = summarizeText.parseStringSimple01(submission.title)
    #text = summarizeText.parseStringSimple01(submission.selftext)
    #postText = title + text

    postAge = datetime.datetime.utcnow() - submission.created_utc
    hours2 = datetime.timedelta(hours=2)
    #logging.debug(  '\t'+"Post Age: "+ str(postAge) )

    votes = submission.score 
    upvoteRatio = submission.upvote_ratio 


    #print title
    #logging.debug(  '\t'+ "Votes: "+ str(votes))
    #logging.debug(  '\t'+ "Upvote Ratio: "+str( upvoteRatio))

    if postAge < hours2:
        return False

    if votes > 0:
        return False

    if upvoteRatio > 0.41:
        return False

    if submission.id not in submission.url:
        # Links off site 
        logging.debug(  '\t'+'Results: Error. Classification is dead,  (URL) Mismatch. ')
        return False



    # ID if a question is here right now
    title = summarizeText.parseStringSimple01(submission.title, removeURL=True)
    text = summarizeText.parseStringSimple01(submission.selftext, removeURL=True)
    postText = title + text
    sents = nltk.sent_tokenize(' '.join(postText))# nltk.sent_tokenize(title) + nltk.sent_tokenize(text)
    #print " ".join(sents)
    question_Sents = []
    for sent in sents:
        #sentDisplay = ' '.join(sent.strip().split('\n'))
        #print '\t', sentDisplay.strip()
        classified = questionIdentifier.classifyString(sent, classifier)
        #print classified
        if "question" in classified.lower():
            question_Sents.append(sent)
            logging.debug(str(classified) +': '+ str(sent))
            print('\tSentence: ', sent)
            print('\tClassified As: ', classified)
        #print '\t', classified
    if len(question_Sents) > 0:
        logging.info('|'.join(question_Sents))
        return question_Sents
    logging.debug("\tNo Question Identified")



    
    # All else
    return False 




def basicUserClassify(reddit, user, userNames, submission, suggestedTime, antiSpamList):
    def popOldSpammers(antiSpamList, ageLimitHours):
        # This is a bodge because it's late
        ageLimit = datetime.timedelta(hours=ageLimitHours)
        oldKeys = []
        for key in antiSpamList:
            age = datetime.datetime.utcnow() - antiSpamList[key]
            if age > ageLimit:
                oldKeys.append(key)
        for key in oldKeys:
            if key in antiSpamList:
                del antiSpamList[key]

        return antiSpamList
    
    # Need to classify a user here
    # Only post if 
    DayLimit = 700
    timeDelt = datetime.timedelta(days=DayLimit)
    accountAge = datetime.datetime.utcnow() - user.created_utc

    antiSpamList = popOldSpammers(antiSpamList, ageLimitHours=12) # Should stop growing dict memory leak

        
    # Don't bother commenting if I've talked to the user before
    #  UNLESS they used the help flair
    if str(user.name) in userNames:
        logging.info( "\tI've already commented on a post by "+ str(user.name) )
        if submission.link_flair_text != 'Help':
            msg = "\tI've already commented on a post by " + str(user.name) 
            print(msg)
            if submission.id not in antiSpamList:
                antiSpamList[submission.id] = submission.created_utc
                msg = msg.strip() + "\n\nPost in Question: "+ botHelperFunctions.shortenRedditURL(submission.url)
                textSupervision.send_update(msg)
            return False, [], antiSpamList
        else:
            logging.info("But they used the help flair")


    if accountAge > timeDelt:
        logging.debug('\t'+ str(user.name))
        # User is old enough to know better
        # This is emperically false but I need some limits
        # Actually in practice the bot nearly never comments because of this
        logging.debug( str( accountAge) + " User Should Know Better, They're old enough")
        #print  '\t', "USER SHOULD KNOW BETTER"
        #return False, []


    subs, directedOthersToLearn, postsInLearningSubs = botHelperFunctions.getSubsUsersInteractsIn(reddit, user)
    if 'learnpython' in subs:
        # Probably should check if user has posted in the sub more recently than current post
        logging.info("User " + str(user.name) + " has posted in r/learnpython before")


    if directedOthersToLearn:
        logging.info("User " + str(user.name) + " has directed others to r/learnpython")
        #return False, [], antiSpamList

    return True, postsInLearningSubs, antiSpamList
