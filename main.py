import praw
import nltk
import datetime
import time
import os
import argparse, textwrap
# Logging Info
import logging
import traceback

from utils import archiveAndUpdateReddit
from utils import questionIdentifier
from utils import summarizeText
from utils import searchStackOverflowWeb
from utils import textSupervision
from utils import locateDB
from utils import botMetrics
from utils import botHelperFunctions 
from asecretplace import getPythonHelperBotKeys
  

'''  
Keith Murray 
email: kmurrayis@gmail.com


This bot is powered by coffee and the WestWorld Soundtrack. 

act = "JUST CODE IT"
print(act[:5]+ act[6:8][::-1]+act[9:])
'''

# Post to reddit text block
def baseComment():
    msg = '''Hello! I'm a bot! 
It looks to me like your post might be better suited for r/learnpython, a sub geared towards questions and learning more about python. 
That said, I am a bot and it is hard to tell.
I highly recommend posting your question there. 
Please follow the subs rules and guidelines when you do post there, it'll help you get better answers faster. 

Show /r/learnpython the code you have tried and describe where you are stuck. 
**[Be sure to format your code for reddit](https://www.reddit.com/r/learnpython/wiki/faq#wiki_how_do_i_format_code.3F)** and include which version of python and what OS you are using.

You can also ask this question in the [Python discord](https://discord.gg/3Abzge7), a large, friendly community focused around the Python programming language, open to those who wish to learn the language or improve their skills, as well as those looking to help others. 
'''
    return msg
def alreadySuggestedComment():
    msg = '''Hello! I'm a bot!
I see someone has already suggested going to r/learnpython, a sub geared towards questions and learning more about python. I highly recommend posting your question there. 
Please follow the subs rules and guidelines when you do post there, it'll help you get better answers faster. 
    
Show /r/learnpython the code you have tried and describe where you are stuck. 
**[Be sure to format your code for reddit](https://www.reddit.com/r/learnpython/wiki/faq#wiki_how_do_i_format_code.3F)** and include which version of python and what OS you are using.

You can also ask this question in the [Python discord](https://discord.gg/3Abzge7), a large, friendly community focused around the Python programming language, open to those who wish to learn the language or improve their skills, as well as those looking to help others. 
'''
    return msg
def UserCrossPosted():
    # Figure out what to say to the spray and pray
    msg = '''Hello! I'm a bot!
It looks like you posted this in multiple subs in a short period of time. 

    '''
    return msg
def alreadyAnsweredComment():
    msg = '''Hello! I'm a bot!
It looks to me like someone might have already answered your question. 
That said, I am a bot and it is hard to tell. 
In the future, I suggest asking questions like this in r/learnpython, a sub geared towards questions and learning more about python. 
Please follow the subs rules and guidelines when you do post there, it'll help you get better answers faster. 
    
Show /r/learnpython the code you have tried and describe where you are stuck. 
**[Be sure to format your code for reddit](https://www.reddit.com/r/learnpython/wiki/faq#wiki_how_do_i_format_code.3F)** and include which version of python and what OS you are using.

You can also ask this question in the [Python discord](https://discord.gg/3Abzge7), a large, friendly community focused around the Python programming language, open to those who wish to learn the language or improve their skills, as well as those looking to help others. 
'''
    return msg
def supervisedComment():
    msg ="\n\n###I am currently running in a supervised mode for testing and only comment when it's been approved"
    return msg

def signatureComment():
    msg = """\n\n***\n\n[^(README)](https://github.com/CrakeNotSnowman/redditPythonHelper) 
^(|)
[^(FAQ)](https://github.com/CrakeNotSnowman/redditPythonHelper/blob/master/FAQ.md) 
^(|)
^(this bot is written and managed by /u/IAmKindOfCreative) 
"""
    return msg

def inDevelopmentComment():
    msg = "\n\n^(This bot is currently under development and experiencing changes to improve its usefulness)"
    return msg

def commentOnSubmmission(submission, msg, reddit):
    # Post message to reddit submission
    #testingsubmissionID = '8nvbf3'
    #submission = reddit.submission(id=testingsubmissionID)

    submission.reply(msg)
    return


def idealQuery(title, questions, keywords, tdm):
    # Using NLP Magic (yet to be determined): identify best keywords 
    #   to search stack overflow with
    text = title 
    text += ' '.join(questions) 
    text += '\n' + ' '.join(keywords)
    try:
        summary = summarizeText.summarizeDoc_SentToDoc(text, tdm, topSentCount=1)
    except Exception as e:
        print(e)
        logging.error(e)
        summary = ' '.join(keywords)
    logging.debug( '\t' + summary)
    query = 'python ' + summary
    return query

def stackOverflowInfo(title, text, questions, tdm):
    # Extract keywords for SO search
    postText = summarizeText.detokenize( title + text)

    key_phrase_set = summarizeText.wordRankKeywords(postText)
    if len(key_phrase_set) > 5:
        key_phrase_set = key_phrase_set[:5]

    x = ' '.join(key_phrase_set)
    
    # Best Query is max ()
    # PENDING IMPLEMENTATION, NOT YET READY

    query = idealQuery(title, questions, key_phrase_set, tdm)
    # Search SO
    try:
        searchResults = searchStackOverflowWeb.search_stackoverflow(query)
    except:
        # It's a bodge, but this block of code is slated to be changed soon anyway. 
        searchResults=[None]

    # Review results

    # If results are good, build SO Answer to msg
    result_msg = ""
    resultScore = []
    #resultTitle
    # BODGE
    '''
    Traceback (most recent call last):
  File "main.py", line 321, in <module>
    runBot(reddit, classifier, tdm, userNames, postHistory)
  File "main.py", line 294, in runBot
    buildHelpfulComment(submission, user, question_Set, classifier, tdm, reddit)
  File "main.py", line 106, in buildHelpfulComment
    key_phrases, so_msg, search_results = stackOverflowInfo(title, text, question_Set, tdm)
  File "main.py", line 72, in stackOverflowInfo
    if len(searchResults[0])> 0:
TypeError: object of type 'NoneType' has no len()
    '''
    if searchResults[0] is not None: 
        if len(searchResults[0])> 0:
            i = 1
            for key in searchResults[0]:
                result_msg += '\n' + str(i) + '. [' + key['Title'] + '](' + key['URL'] + ')'
                if i >= 3:
                    break
                i += 1


    msgIntro = "\n\nWhile I was at it, I checked [Stack Overflow](https://stackoverflow.com/) "

    msg = msgIntro

    if len(result_msg) > 0: 
        msg += "and found these results which might be useful:\n" + result_msg
    else:
        msg += "but I couldn't find a useful result"

    msgNotWorkingProperly = "\n\nThough fair warning, this section of the my code is under development, and I don't expect these links to be very useful."
    msg += msgNotWorkingProperly

    return key_phrase_set, msg, searchResults

def shortenRedditURL(url):
    url = url[8:]
    return '/'.join(url.split('/')[:-2])+'/'

def buildHelpfulComment(submission, user, question_Set, classifier, tdm, reddit, suggested, crossPosted, quietMode):
    supervised = False
    underDev = True

    title = summarizeText.parseStringSimple01(submission.title)
    text = summarizeText.parseStringSimple01(submission.selftext)
    if suggested:
        msg = alreadySuggestedComment()
    #elif crossPosted:
     #   msg = UserCrossPosted()
    else:
        msg = baseComment()

    # Stack Overflow has changed and I'm not working through the soup right now
    #key_phrases, so_msg, search_results = stackOverflowInfo(title, text, question_Set, tdm)
    #msg += so_msg

    if supervised:
        msg = msg+supervisedComment()
        print(title)
        print(text)
        print(submission.url)
        cleanURL = shortenRedditURL(submission.url)
        sms_msg = "Is this post worth commenting on?\n" + cleanURL 
        reply = textSupervision.getUserFeedbackViaText(outgoingMsg=sms_msg).strip()
        #input_str = raw_input("Is this post worth commenting on?")
        if reply.lower() in ['y', 'yes']:
            print("COOL BRO")
            #print("Keywords found: ", key_phrases, '\nSearch Result Size')
            #print(len(search_results[0]))
            print('\tCommenting...')
        else:
            print("Aw Damnit.")
            return
    # Sign the message
    msg += signatureComment() 
    # Say it's changing
    if underDev:
        msg += inDevelopmentComment()
    logging.debug(msg)
    # Quiet Mode is used to debug, and avoid
    if not quietMode:
        commentOnSubmmission(submission, msg, reddit)
        archiveAndUpdateReddit.updateDatabase(user.name, submission.id)
        logging.debug( '\t\tCommented.')
    else:
        logging.debug("Quiet Mode is on, no actual post was made")
    

    return

    
def request_Key_Word_Filter(submission):
    '''
    This is a hand made feature set to id titles that make reddit-typical 
    requests for help, but might not phrase the request as a question

    '''

    # Consider adding a time delay here?
    
    text = ' '.join(summarizeText.parseStringSimple01(submission.title))
    # Pass phrase_set through string parser and back, it'll help? 
    phrase_set = ['need help', '[help]', '[ help ]', '[question]', 
                    '[ question ]', 'noob ', 'n00b ', ' newb','please help', 
                    'noobie question', 'help!', 'help me', "isn't working",
                    'not working', 'issues with', 'issue with',
                    'looking for tutorial', 'Quick question', 'help needed',
                    'plz help', "what's wrong", "need some help", '[q]',
                    '[Beginner Question]']
    request_Made = False
    #print text
    for phrase in phrase_set:
        if ' '.join(summarizeText.parseStringSimple01(phrase)).lower() in text:
            logging.info(phrase + " Was used in the post title")
            request_Made = True
            break

    if request_Made:
        text = summarizeText.parseStringSimple01(submission.selftext)
        sents = nltk.sent_tokenize(' '.join(text))
        # Returning the last sentence is chosen purely based on a guess
        # It'll be more useful to select sents based on idf and entropy score
        try:
            return sents[-1]
        except:
            logging.info("Failed to grab last sentence: Probably links offsite")
            pass

    
    return False


def basicQuestionClassify(submission, user, classifier, tdm):
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

    postAge = datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(submission.created_utc)
    hours2 = datetime.timedelta(hours=2)
    logging.debug(  '\t'+"Post Age: "+ str(postAge) )

    votes = submission.score 
    upvoteRatio = submission.upvote_ratio 


    #print title
    logging.debug(  '\t'+ "Votes: "+ str(votes))
    logging.debug(  '\t'+ "Upvote Ratio: "+str( upvoteRatio))

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
        sentDisplay = ' '.join(sent.strip().split('\n'))
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

def checkForLearnPythonSuggestion(submission):
    # This is to check and see if learn python has been suggested 
    topComments = archiveAndUpdateReddit.getTopLevelComments(submission)
    suggestedTime = -1
    for comment in topComments:
        text = comment.body
        #words = text.split()
        if 'learnpython' in text:
            logging.debug("Someone has already Suggested r/learnpython")
            suggestedTime = datetime.datetime.fromtimestamp(comment.created_utc)
            return True, suggestedTime

    return False, suggestedTime


def checkForAlreadyAnswered(submission):
    '''
    Soft Skill extension
    'Wow thank you so much!'
    'I think I get it'
    'Thanks a lot for pointing that out! I actually oversaw that on the site but now i'm working on getting it running'
    '''

    return False

def getSubsUsersInteractsIn(user, limitCount=25):
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
    submissionList = archiveAndUpdateReddit.getUserPosts(user, limitCount)
    commentList = archiveAndUpdateReddit.getUsersComments(user, limitCount)
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
    
def basicUserClassify(user, userNames, submission, suggestedTime, antiSpamList):
    
    # Need to classify a user here
    # Only post if 
    DayLimit = 700
    timeDelt = datetime.timedelta(days=DayLimit)
    accountAge = datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(user.created_utc)

    antiSpamList = popOldSpammers(antiSpamList, ageLimitHours=12) # Should stop growing dict memory leak

        
    # Don't bother commenting if I've talked to the user before
    if str(user.name) in userNames:
        logging.info( "\tI've already commented on a post by "+ str(user.name) )
        msg = "\tI've already commented on a post by " + str(user.name) 
        print(msg)
        if submission.id not in antiSpamList:
            antiSpamList[submission.id] = datetime.datetime.utcfromtimestamp(submission.created_utc)
            msg = msg.strip() + "\n\nPost in Question: "+ shortenRedditURL(submission.url)
            textSupervision.send_update(msg)
        return False, [], antiSpamList


    if accountAge > timeDelt:
        logging.debug('\t'+ str(user.name))
        # User is old enough to know better
        # This is emperically false but I need some limits
        # Actually in practice the bot nearly never comments because of this
        logging.debug( str( accountAge) + " User Should Know Better, They're old enough")
        #print  '\t', "USER SHOULD KNOW BETTER"
        #return False, []


    subs, directedOthersToLearn, postsInLearningSubs = getSubsUsersInteractsIn(user)
    if 'learnpython' in subs:
        # Probably should check if user has posted in the sub more recently than current post
        logging.info("User " + str(user.name) + " has posted in r/learnpython before")


    if directedOthersToLearn:
        logging.info("User " + str(user.name) + " has directed others to r/learnpython")
        return False, [], antiSpamList

    return True, postsInLearningSubs, antiSpamList


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
        pythonPostTime = datetime.datetime.utcfromtimestamp(submission.created_utc)
        for post in postsInLearningSubs:
            learningPostTime = datetime.datetime.utcfromtimestamp(post.created_utc)
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


            




def checkInbox(reddit, unreadCount=None, sendText = True):
    # Mark all messages as read after notification has been sent
    inboxMessages = archiveAndUpdateReddit.checkForMessages(reddit)
    sendText = True

    # Handle startup unread count
    if unreadCount == None:
        return len(inboxMessages)


    if len(inboxMessages) > unreadCount:
        commentReplies = 0
        directMessages = 0
        userNameMentions = 0
        for msg in inboxMessages:
            if msg.was_comment:
                if msg.subject == "username mention":
                    userNameMentions += 1
                else: 
                    commentReplies += 1
            else:
                directMessages += 1
        newMsgCount = len(inboxMessages) - unreadCount

        if sendText:
            if newMsgCount > 1:
                txtmsg = "You have " + str(newMsgCount) + " new unread messages."
            else:
                txtmsg = "You have 1 new unread message."
            txtmsg += "\n\nUnread Replies to your Comments: " + str(commentReplies)
            txtmsg += "\nUnread Direct Messages: " + str(directMessages)
            txtmsg += "\nUnread Username Mentions: " + str(userNameMentions)
            textSupervision.send_update(txtmsg)
            logging.info("Text Message sent: \n"+txtmsg)

    unreadCount = len(inboxMessages)

    return unreadCount

    







def startupBot():
    print("Loading bot")
    logging.debug("Loading Bot")


    paths = locateDB.get_db_file_locations()
    #print "File Path Keys: ", paths.keys()
    #print paths
    # Make some form of error check for the path variable 
    #assert paths[enlishDB] is not False

    # Load Term-Doc Matrix Datastructure
    tdm = summarizeText.buildModelFromDocsInFolder(sourceDataPath=paths["englishDB"])
    # NLTK classifier (Statement, YNQuestion, WHQuestion, etc)
    classifier = questionIdentifier.buildClassifier02NLTKChat()
    # Reddit API
    keySet = getPythonHelperBotKeys.GETREDDIT()
    reddit = praw.Reddit(client_id=keySet[0], client_secret=keySet[1], 
                     password=keySet[2], user_agent=keySet[3],
                    username=keySet[4])

    # Py SQL Database 
    userNames, postHistory = archiveAndUpdateReddit.startupDatabase()
    # Ignore all mod posts: they know what they're doing
    for mod in reddit.subreddit('python').moderator():
        userNames.append(str(mod))
    

    logging.debug( "Loaded. Running...")
    return reddit, classifier, tdm, userNames, postHistory


def runBot(reddit, classifier, tdm, userNames, postHistory, quietMode=False):
    setOfPosts = archiveAndUpdateReddit.grabAndUpdateNewPosts(reddit)
    unreadCount = checkInbox(reddit)
    antiSpamList = {} # Used in basicUserClassify to only text me once per submission by a repeat user
    while True:
        for key in setOfPosts:
            submission, user = setOfPosts[key]
            if str(submission.id) not in postHistory:
                logging.debug( '*'*50)
                logging.debug('[POST]   | ' + str(submission.title.encode('ascii', 'ignore')))
                logging.debug('[AUTHOR] | ' + str(user.name))
                logging.debug('[ID]     | ' + str(submission.id))
                question_Set = basicQuestionClassify(submission, user, classifier, tdm)
                request_Made = request_Key_Word_Filter(submission)
                if question_Set or request_Made:
                    # BODGE
                    if request_Made and not question_Set:
                        question_Set = request_Made
                    
                    logging.debug(  '\t'+ "Found a valid post")
                    suggested, suggestedTime = checkForLearnPythonSuggestion(submission)
                    user_status, postsInLearningSubs, antiSpamList = basicUserClassify(user, userNames, submission, suggestedTime, antiSpamList) 
                    if user_status:
                        logging.debug(  '\t'+ "User is valid")

                        if len(postsInLearningSubs) > 0:
                            tookAdvice, crossPosted, askedLearningLater = user_Already_Took_Advice(submission, postsInLearningSubs, suggestedTime)
                        else: 
                            tookAdvice = False
                            crossPosted = False
                            askedLearningLater = False

                        # Check to see if user has already posted to LP

                        if not tookAdvice and not askedLearningLater:
                            # Shutup if already directed, and user listened
                            buildHelpfulComment(submission, user, question_Set, classifier, tdm, reddit, suggested, crossPosted, quietMode)
                            userNames.append(str(user.name))
                            postHistory.append(str(submission.id))
                            #pass

        botMetrics.performanceVisualization(reddit)
        unreadCount = checkInbox(reddit, unreadCount=unreadCount, sendText= True)
        logging.debug( "Sleeping..." + str(datetime.datetime.now()))
        time.sleep(15*60)
        setOfPosts = archiveAndUpdateReddit.grabAndUpdateNewPosts(reddit, submissionList=setOfPosts)


def interface():
    args = argparse.ArgumentParser(
        prog='main.py', 
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='A reddit bot to help direct new users to r/learnpython',
        epilog=textwrap.dedent('''\
            To run the bot without the risk of commenting, run quiet mode.
        '''))
    args.add_argument('-q', '--quiet-mode', type=bool, default=False,\
                      help='[True/False] Run the program without posting to reddit or texting')
    args = args.parse_args()
    return args


# https://i.imgur.com/vHRUkak.gif Mos Fire
# https://i.imgur.com/3i8EM9Q.jpg Kiss and wave
# https://i.imgur.com/9RnHTMs.mp4 Woody entrance 





if __name__ == "__main__":
    args = interface()
    quietMode = args.quiet_mode
    print(quietMode)
    # Logging Stuff
    dirName = "logs"
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    logFileName =   'LOG_'+ datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.log'
    filePath = os.path.join(dirName, logFileName)
    logging.basicConfig(filename=filePath, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    if quietMode:
        logging.debug("Running in Quiet Mode")

    reddit, classifier, tdm, userNames, postHistory = startupBot()
    try:
        runBot(reddit, classifier, tdm, userNames, postHistory, quietMode=quietMode)
    except KeyboardInterrupt:
        print("Concluding Program")
        logging.debug("Keyboard Interrupt: Ending Program")
    except:
        logging.error("\n"+traceback.format_exc())
        fl = open("ERRORLOG.log", 'a')
        fl.write("\n"+"*"*50+"\n"+traceback.format_exc())
        fl.close()
        print(traceback.format_exc())
        trc = traceback.format_exc().strip().split("\n")[-1]
        msg = "Program exited on Error:\n"+str(trc)
        if len(msg) > 133:
            msg = msg[:130] + '...'
            print(msg)
        print(msg)
        if not quietMode:
            textSupervision.send_update(msg)

    


