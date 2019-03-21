

import praw
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import logging

# Not sure about these two. It is metrics though..
try:
    import moviepy.editor as mpy
except:
    logging.warning("Unable to import moviepy editor, karmaPlotstoGif() will not function")
    
from PIL import Image


from utils import archiveAndUpdateReddit
from utils import botHelperFunctions
from utils import textSupervision


'''  
Keith Murray 
email: kmurrayis@gmail.com
'''


def questionAndAnswer(query):
    '''
    Hopefully this will be the first implementation of "Soft Skills"
    Questions I want to answer
    How well does this bot work
    How does this bot work
    How useful has the bot been to users
    How much does this bot fail 
    '''

    return

def karmaPlot(date, karma, totalCommentKarma):
    dirName = "karma"
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    
    color = ['red' if k < 0  else 'black' if k < 2 else 'blue' for k in karma]
    # Adjust x axis date display angle
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M')) 
    plt.gcf().autofmt_xdate()
    # Deal with weird x min/max bug (without, scale will be improperly set to +- ~ 2 months)
    # See:
    # https://github.com/matplotlib/matplotlib/issues/5963
    plt.xlim(xmin=min(date)-datetime.timedelta(days=1), xmax=max(date)+datetime.timedelta(days=1))
    # Actual thing we care about
    plt.scatter(date, karma, color=color) 
    curTime = datetime.datetime.utcnow()
    fname = str(curTime.strftime("%Y%m%d_%H%M"))
    prettyTime = curTime.strftime('%Y-%m-%d %H:%M')

    plt.title(prettyTime + " Comment Karma: " + str(totalCommentKarma))
    axes = plt.gca()
    # Try and remove y axis wiggle
    ymin, ymax = axes.get_ylim()
    ymag = max(abs(ymin), ymax)
    plt.ylim(ymin=-ymag, ymax=ymag) 
    #plt.show()
    plt.savefig(os.path.join(dirName, fname + '.png'), bbox_inches='tight')
    plt.close()

    
    fl = open(os.path.join(dirName, "totalKarmaByTime.txt"), 'a')
    fl.write(prettyTime + "\t" + str(totalCommentKarma)+'\n')
    fl.close()


    return

def totalKarmaLinePlot():
    # Load file
    dirName = "karma"    
    fl = open(os.path.join(dirName, "totalKarmaByTime.txt"), 'r')
    timeRange = []
    karmaCount = []
    for line in fl:
        line = line.strip()
        prettyTime, totalCommentKarma = line.split('\t')
        karmaCount.append(int(totalCommentKarma))
        timestamp = datetime.datetime.strptime(prettyTime, '%Y-%m-%d %H:%M')
        timeRange.append(timestamp)
    fl.close()

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M')) 
    plt.gcf().autofmt_xdate()
    # Deal with weird x min/max bug (without, scale will be improperly set to +- ~ 2 months)
    # See:
    # https://github.com/matplotlib/matplotlib/issues/5963
    plt.xlim(xmin=min(timeRange)-datetime.timedelta(days=1), xmax=max(timeRange)+datetime.timedelta(days=1))
    # Actual thing we care about
    plt.plot(timeRange, karmaCount) 

    plt.show()
    plt.close()
    return






def performanceVisualization(reddit):
    # Only run once per unit time

    # Running
    user = archiveAndUpdateReddit.get_redditor_by_name(reddit, 'pythonHelperBot')
    totalCommentKarma = user.comment_karma
    date, karma = archiveAndUpdateReddit.makeCommentKarmaReport(user, reddit) 
    karmaPlot(date, karma, totalCommentKarma)
    return




def karmaPlotstoGif(outfileName="redditBotKarma.mp4", filePath = "karma"):


    # Temp dir to stage all adjusted sized images
    tempDirName = "temp"
    if not os.path.exists(tempDirName):
        os.makedirs(tempDirName)
    
    # Grab all files
    fileList = []
    if os.path.isfile(filePath):
        fileList.append(filePath)
    else:
        for dirname, dirnames, filenames in os.walk(filePath):
            for filename in filenames:
                fileList.append(os.path.join(dirname, filename))
    
    # sort only images by timestamp 
    fileList = sorted([x for x in fileList if x[-4:] == ".png"])

    # Get max width and heigth of images 
    for imgF in fileList:
        maxW = 0
        maxH = 0
        with Image.open(imgF) as img:
            width, height = img.size
            maxW = max(maxW, width)
            maxH = max(maxH, height)

    #
    tempL = []
    for  imgF in fileList:
        imgFName = os.path.basename(imgF)
        
        with Image.open(imgF) as img:
            im = img.resize((maxW, maxH), Image.ANTIALIAS)
            imPath = os.path.normpath(tempDirName+'/'+imgFName)
            im.save(imPath)
            tempL.append(imPath)


    if len(tempL) > 0:
        clip = mpy.ImageSequenceClip(tempL, fps=10)
        clip.write_videofile(outfileName, fps=10)
        print("Built Gif")

        
    print("Deleting temp files ")
    for fl in tempL:
        os.remove(os.path.normpath(fl))
        #print fl 

    return 
    
def predictUserReaction(reddit, user, phbArcPaths):

    return


def measureUserReaction(reddit, submission, user, suggestionTime):
    '''
    For every user u/pythonHelperBot has interacted with,
    Check to see if they posted in r/learnpython a certain time 
    after their post (some function of next batch of user activity)


    '''
    limitCount = 10
    learningSubs = botHelperFunctions.get_learning_sub_Names()
    submissionList = user.getUserPosts(reddit, limitCount=limitCount)
    #tookAdvice = False
    #for submission in submissionList:
    #    if str(submission.subreddit).lower() in learningSubs:
    #        post_Time = datetime.datetime.utcfromtimestamp(submission.created_utc)
    #        if post_Time - suggestionTime > 0:
                # Here you could check to see if the posts are similar, but we'll ignore that
                # On the assumption that the bot is useful if it encourages users to ask
                # future questions in the correct sub. And that question 1 might have already 
                # been answered, but there might be a followup question incoming.
    #            tookAdvice = True

    

    #return tookAdvice


def archiveModActions(reddit, phbArcPaths, sub="Python"):
    '''
    Function is used to record posts mods have commented on about 
    removal, as well as the message associated with the removal.
    This will be used to build a 'crowd sourced' labeled set of 
    'learning' posts.
    '''
    
    # Load last recorded comment for mod
    ifl = os.path.join(phbArcPaths['modActions'], 'lastRecModAction.txt')
    lastArchivedModAction = {}
    if os.path.isfile(ifl):
        with open(ifl,'r') as fl:
            for line in fl:
                line = line.strip().split('\t')
                modName = line[0]
                dtString =  datetime.datetime.strptime(line[1], "%Y-%m-%d %H:%M:%S")

    # Get all but automod
    mods = []
    excludeMods = ['AutoModerator']
    mods = [mod for mod in archiveAndUpdateReddit.getMods(reddit, sub=sub) if mod.name not in excludeMods]

    for mod in mods: 
        if mod.name in lastArchivedModAction:
            comments = mod.getUsersComments(reddit=reddit, limitCount=100, ageLimitHours=None, ageLimitTime=lastArchivedModAction[mod.name])
        else:
            # Grab mod actions over the past 48 hours, we've never seen this mod before
            comments = mod.getUsersComments(reddit=reddit, limitCount=100, ageLimitHours=48)

        for comment in comments:
            if comment.subreddit == sub:
                #modActionComments.append(comment)
                archiveAndUpdateReddit.saveClassJson(comment, database_path=phbArcPaths['modActionsJson'])
            if mod.name not in lastArchivedModAction:
                lastArchivedModAction[mod.name] = comment.created_utc
            elif comment.created_utc > lastArchivedModAction[mod.name]:
                lastArchivedModAction[mod.name] = comment.created_utc


    # Save most recent mod action
    with open(ifl, 'w') as ofl:
        for key in lastArchivedModAction:
            ofl.write(key + "\t" + str(lastArchivedModAction[key]) + '\n')

    return

def processKarmaRequest(msg, setOfPosts, quietMode, phbArcPaths, ageLimitHours=4):
    ''' 
    By this point we know message is by an approved user, and is asking
    for a karma plot. We have to verify is the id associated with the
    request is currently in our setOfPosts. If so, make a plot, save to 
    temp(?) and send to me
    '''
    idTarget = msg.body.split(':')[-1].strip()
    input_subject_Line = msg.subject.lower()
    match = False
    for key in setOfPosts:
        submission, user = setOfPosts[key]
        if submission.id == idTarget:
            match = True
            break

    if match:
        karmaScore = [x[0] for x in submission.score_History]
        upvoteRatio = [x[1] for x in submission.score_History]
        date = [x[3] for x in submission.score_History]
        title = "Karma for post " + str(submission.make_shortlink()) + " by " + str(user.name)


        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M')) 
        #plt.gcf().autofmt_xdate()
        # Deal with weird x min/max bug (without, scale will be improperly set to +- ~ 2 months)
        # See:
        # https://github.com/matplotlib/matplotlib/issues/5963
        plt.xlim(xmin=min(date)-datetime.timedelta(minutes=20), xmax=max(date)+datetime.timedelta(minutes=20))
        # Actual thing we care about
        
        # Two subplots, the axes array is 1-d
        f, axarr = plt.subplots(2, sharex=True)
        axarr[0].plot(date, karmaScore)
        axarr[0].set_title(title)
        axarr[0].set_ylabel("Karma")
        axarr[1].plot(date, upvoteRatio)
        axarr[1].set_ylabel("Upvote Ratio")
        axarr[1].set_xlabel("Timestamp")
        

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M')) 
        plt.gcf().autofmt_xdate()

        dirName = phbArcPaths['phbScoreDisplay']
        outMedia = os.path.join(dirName, str(submission.id) + '.png')
        plt.savefig(outMedia, bbox_inches='tight')
        plt.close()

        # Send the info!!!
        outgoingMsg = title
        sbjLine = "Here's a pretty plot for you!"
        textSupervision.send_karma_plot(outgoingMsg, outMedia, sbjLine, input_subject_Line=input_subject_Line)
