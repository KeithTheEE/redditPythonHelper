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
from utils import botHelperFunctions 
from utils import botMetrics
from utils import botSummons
from utils import buildComment
from utils import formatCode
from utils import learningSubmissionClassifiers
from utils import locateDB
from utils import questionIdentifier
from utils import searchStackOverflowWeb
from utils import summarizeText
from utils import textSupervision
from asecretplace import getPythonHelperBotKeys
  

'''  
Keith Murray 
email: kmurrayis@gmail.com


This bot is powered by coffee and the WestWorld Soundtrack. 

act = "JUST CODE IT"
print(act[:5]+ act[6:8][::-1]+act[9:])
'''

def buildHelpfulComment(submission, user, reddit, suggested, crossPosted, answered, 
                        codePresent, correctlyFormatted, quietMode, phbArcPaths):
    supervised = False
    underDev = True
    
    bagOfSents = []
    # Intro
    bagOfSents.append(buildComment.botIntro())

    # User Sittuation Context Awareness
    if crossPosted:
        bagOfSents.append(buildComment.userCrossPosted())
    elif answered:
        bagOfSents.append(buildComment.alreadyAnsweredComment())
    elif suggested:
        bagOfSents.append(buildComment.alreadySuggestedComment())
    else:
        bagOfSents.append(buildComment.standardIntro())

    # Follow rules and help make code clear
    bagOfSents.append(buildComment.followSubRules())
    logging.info("Code Present: " + str(codePresent) + " | Correctly Formatted: " + str(correctlyFormatted))
    if not (codePresent and correctlyFormatted):
        # They've either not shown code or not shown
        #  well formatted code, we should suggest formatting
        bagOfSents.append(buildComment.formatCodeAndOS())

    # Another good location is the discord
    bagOfSents.append(buildComment.discord())

    if supervised:
        logging.debug("Asking about post")
        bagOfSents.append(buildComment.supervisedComment())
        cleanURL = botHelperFunctions.shortenRedditURL(submission.url)
        sms_msg = "Is this post worth commenting on?\n" + cleanURL 
        reply = textSupervision.getUserFeedbackViaText(outgoingMsg=sms_msg).strip()
        if reply.lower() not in ['y', 'yes']:  
            logging.debug("Told not to comment")          
            return
        logging.debug("Told to comment")
    
    # Sign the message
    bagOfSents.append(buildComment.signatureComment() )
    # Say it's changing
    if underDev:
        bagOfSents.append(buildComment.inDevelopmentComment())


    msg = '\n'.join(bagOfSents)    
    logging.debug(msg)
    # Quiet Mode is used to debug, and avoid
    if not quietMode:
        archiveAndUpdateReddit.commentOnSubmmission(submission, msg, reddit, quietMode)
        archiveAndUpdateReddit.updateDatabase(user.name, submission.id, phbArcPaths=phbArcPaths)
        logging.debug( '\t\tCommented.')
    else:
        logging.debug("Quiet Mode is on, no actual post was made")
    

    return


def checkForLearnPythonSuggestion(reddit, submission):
    # This is to check and see if learn python has been suggested 
    topComments = submission.get_top_level_comments(reddit)
    suggestedTime = -1
    for comment in topComments:
        text = comment.body
        #words = text.split()
        if 'learnpython' in text:
            logging.debug("Someone has already Suggested r/learnpython")
            suggestedTime = comment.created_utc
            return True, suggestedTime

    return False, suggestedTime


def checkForAlreadyAnswered(reddit, user, submission):
    '''
    Soft Skill extension
    'Wow thank you so much!'
    'I think I get it'
    'Thanks a lot for pointing that out! I actually oversaw that on the site but now i'm working on getting it running'
    '''

    return False


            

def checkForSummons(msg):
    summonID = None
    if msg.subject.strip() == "username mention":
        if (msg.body.strip() == 'u/pythonHelperBot !reformat') or (msg.body.strip() == '/u/pythonHelperBot !reformat'):
            print("SUMMONS")
            print(msg.id)
            summonID = msg.id
        print(msg.body)
    
    return summonID

def check_for_help_tag(submission):
    '''
    Checks for new help tag 
    '''
    if submission.link_flair_text == 'Help':
        logging.debug("New Post Tagged as Help")
        return True
    return False

def check_for_key_phrase(submission, phrase_set):
    botHelperFunctions.logPostFeatures(submission)
    request_Made = learningSubmissionClassifiers.request_Key_Word_Classifier(submission, phrase_set)
    return request_Made

def lookForKeyPhrasePosts(reddit, setOfPosts, phrase_set):

    oldPosts = setOfPosts.copy() # https://stackoverflow.com/questions/5861498/
    setOfPosts = archiveAndUpdateReddit.getNewPosts(reddit, submissionList=setOfPosts)
    submissionsToCommentOn_KP = []
    for key in setOfPosts:
        if key not in oldPosts:
            submission, user = setOfPosts[key]
            request_Made = check_for_key_phrase(submission, phrase_set)
            help_tag = check_for_help_tag(submission)
            if request_Made or help_tag:
                submissionsToCommentOn_KP.append(key)

    return setOfPosts, submissionsToCommentOn_KP



def basicQuestion_classifyPost(submission, classifier):
    botHelperFunctions.logPostFeatures(submission)
    question_Sents = learningSubmissionClassifiers.basicQuestionClassify(submission, classifier)
    return question_Sents

def handleSetOfSubmissions(reddit, setOfPosts, postHistory, classifier):

    submissionsToCommentOn_BC = []
    for key in setOfPosts:
        if key not in postHistory:
            submission, user = setOfPosts[key]
            question_Sents = basicQuestion_classifyPost(submission, classifier)
            if question_Sents:
                submissionsToCommentOn_BC.append(key)
    return submissionsToCommentOn_BC


def getReadyToComment(reddit, setOfPosts, userNames, postHistory, commentOnThese, antiSpamList, codeVTextClassifier, quietMode, phbArcPaths):

    # Remove Duplicates as a precaution
    #commentOnThese = list(set(commentOnThese))

    for key in setOfPosts:
        if key in commentOnThese:
            if key not in postHistory:
                submission, user = setOfPosts[key]
                logging.debug("Processing a valid post")
                botHelperFunctions.logPostFeatures(submission)
                suggested, suggestedTime = checkForLearnPythonSuggestion(reddit, submission)
                user_status, postsInLearningSubs, antiSpamList = learningSubmissionClassifiers.basicUserClassify(reddit, user, userNames, submission, suggestedTime, antiSpamList) 
                if user_status:
                    logging.debug(  '\t'+ "User is valid")
                    tookAdvice = False
                    crossPosted = False
                    askedLearningLater = False
                    if len(postsInLearningSubs) > 0:
                        tookAdvice, crossPosted, askedLearningLater = botHelperFunctions.user_Already_Took_Advice(submission, postsInLearningSubs, suggestedTime)
                        
                    if not tookAdvice and not askedLearningLater:
                        # Shutup if already directed, and user listened
                        answered=False
                        codePresent=False
                        correctlyFormatted=False
                        msg, changesMade, codePresent, correctlyFormatted = formatCode.reformat(submission.selftext, codeVTextClassifier)

                        # Gauge user reactions (right now only archiving)
                        botMetrics.predictUserReaction(reddit, user, phbArcPaths)

                        buildHelpfulComment(submission, user, reddit, suggested, crossPosted, answered, codePresent, correctlyFormatted, quietMode, phbArcPaths=phbArcPaths) 
                        userNames.append(str(user.name))
                        postHistory.append(str(submission.id))


    return userNames, postHistory, antiSpamList



def startupBot():
    print("Loading bot")
    logging.debug("Loading Bot")


    paths = locateDB.get_db_file_locations()
    #print "File Path Keys: ", paths.keys()
    #print paths
    #archive = paths['archive']
    #backup = paths['backup']
    archive_Locations = [paths['archive'], paths['backup']]
    # Py SQL Database 
    userNames, postHistory, phbArcPaths = archiveAndUpdateReddit.startupDatabase(archive_Locations)

    # Make some form of error check for the path variable 
    #assert paths[enlishDB] is not False

    # Load Term-Doc Matrix Datastructure
    tdm = summarizeText.buildModelFromDocsInFolder(sourceDataPath=paths["englishDB"])
    # NLTK classifier (Statement, YNQuestion, WHQuestion, etc)
    classifier = questionIdentifier.buildClassifier02NLTKChat()
    # Code vs Text classifier 
    codeVTextClassifier = formatCode.buildTextCodeClassifier(sourceDataPath=paths["codeText"])

    # Reddit API 
    keySet = getPythonHelperBotKeys.GETREDDIT()
    #assert 1 == 2
    reddit = praw.Reddit(client_id=keySet[0], client_secret=keySet[1], 
                     password=keySet[2], user_agent=keySet[3],
                    username=keySet[4])

    # Ignore all mod posts: they know what they're doing
    mods = archiveAndUpdateReddit.getMods(reddit, sub="python")
    for mod in mods:
        userNames.append(str(mod.name)) 
    #recentComments = botHelperFunctions.updateBotsRecentComments(reddit)
    

    logging.debug( "Loaded. Running...")
    return reddit, classifier, codeVTextClassifier, tdm, userNames, postHistory, phbArcPaths



def runBot(reddit, classifier, codeVTextClassifier, tdm, userNames, postHistory,  phbArcPaths={}, quietMode=False):
    
    phrase_set = botHelperFunctions.load_autoreply_key_phrases(fl_path='misc/autoreplyKeyPhrases.txt')
    
    setOfPosts = archiveAndUpdateReddit.grabAndUpdateNewPosts(reddit)
    unreadCount = botSummons.handleInbox(reddit, codeVTextClassifier, phbArcPaths=phbArcPaths,  setOfPosts=setOfPosts, quietMode=quietMode)
    antiSpamList = {} # Used in basicUserClassify to only text me once per submission by a repeat user

  
    threeMin = 3
    lastThreeMin = datetime.datetime.now() - datetime.timedelta(seconds=threeMin*60)
    fifteenMin = 15
    lastFifteenMin = datetime.datetime.now() - datetime.timedelta(seconds=fifteenMin*60)
    twelveHours = 12
    last12Hours = datetime.datetime.now() - datetime.timedelta(seconds=twelveHours*60*60)

    while True:
        commentOnThese = [] 
        if datetime.datetime.now() - lastThreeMin > datetime.timedelta(seconds=threeMin*60):
            #print("3 mins")
            # Handle Inbox
            unreadCount = botSummons.handleInbox(reddit, codeVTextClassifier, phbArcPaths=phbArcPaths,  setOfPosts=setOfPosts, unreadCount=unreadCount, sendText= True, quietMode=quietMode)

            # Update karma score for posts under 2 hours old
            setOfPosts = archiveAndUpdateReddit.updateYoungerThanXPosts(reddit, submissionList=setOfPosts) 

            # Get new posts, respond to keywords
            setOfPosts, submissionsToCommentOn = lookForKeyPhrasePosts(reddit, setOfPosts, phrase_set)
            commentOnThese += submissionsToCommentOn

            lastThreeMin = datetime.datetime.now()
            logging.debug( "3 minute region is Sleeping..." + str(datetime.datetime.now()))

        if datetime.datetime.now() - lastFifteenMin > datetime.timedelta(seconds=fifteenMin*60):
            #print("15 mins")
            # Update posts
            setOfPosts = archiveAndUpdateReddit.updatePosts(reddit, submissionList=setOfPosts,   phbArcPaths=phbArcPaths) 

            # reclassify posts
            commentOnThese += handleSetOfSubmissions(reddit, setOfPosts, postHistory, classifier)

            # Performance Visualizations 
            botMetrics.performanceVisualization(reddit)
            lastFifteenMin = datetime.datetime.now()
            logging.debug( "15 minute region is Sleeping..." + str(datetime.datetime.now()))

            # TESTING
            #archiveAndUpdateReddit.removeOldPosts(reddit, submissionList=setOfPosts, ageLimitHours=1, phbArcPaths=phbArcPaths,  archive=True) 

        if datetime.datetime.now() - last12Hours > datetime.timedelta(seconds=twelveHours*60*60):
            # Rare actions
            botMetrics.archiveModActions(reddit, phbArcPaths=phbArcPaths, sub='Python')
            last12Hours = datetime.datetime.now()
            logging.debug("12 Hour Region is Sleeping...")

        # Comment on all classified submissions
        userNames, postHistory, antiSpamList =  getReadyToComment(reddit, setOfPosts, userNames, postHistory, commentOnThese, antiSpamList, codeVTextClassifier, quietMode, phbArcPaths=phbArcPaths)

        time.sleep(30)




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
    if quietMode:
        # Fair assumption that the user is watching the terminal during quiet mode
        print("Bot is Running in Quite Mode")
    # Logging Stuff
    dirName = "logs"
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    logFileName =   'LOG_'+ datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.log'
    filePath = os.path.join(dirName, logFileName) 
    logging.basicConfig(filename=filePath, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s():%(lineno)s - %(message)s')
    if quietMode:
        logging.debug("Running in Quiet Mode")

    reddit, classifier, codeVTextClassifier, tdm, userNames, postHistory, phbArcPaths = startupBot()
    try:
        runBot(reddit, classifier, codeVTextClassifier, tdm, userNames, postHistory,  phbArcPaths=phbArcPaths, quietMode=quietMode)
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

    


