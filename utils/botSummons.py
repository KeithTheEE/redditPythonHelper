


import logging

from utils import archiveAndUpdateReddit
from utils import formatCode
from utils import textSupervision
from utils import botMetrics


def summonCommands():
    '''
    Returns a list of accepted commands for bot actions
    Currently just reformat, however should later include "Helpme"
    to trigger bot auto answer 
    '''
    return ['reformat']

def actOnSummons(reddit, msg, command, codeVTextClassifier, quietMode, setOfPosts):

    if 'reformat' == command.strip().lower():
        formatCode.handleSummons(reddit, msg, codeVTextClassifier, quietMode)
    elif 'format_howto' == command.strip().lower():
        formatCode.makeFormatHelpMessage(reddit, msg, quietMode)
    elif ('kplot' == command) and (msg.author.lower() == 'iamkindofcreative'):
        botMetrics.processKarmaRequest(msg, setOfPosts, quietMode, ageLimitHours=4)
    else:
        logging.info("No know command associated with summons command")

    return

def checkForSummons(msg):
    summonID = None
    command = None
    #commandList = summonCommands()
    if msg.subject.strip() == "username mention":
        if 'u/pythonHelperBot !'.lower() in msg.body.lower().strip() :
            command = msg.body.strip().lower().split('u/pythonHelperBot !'.lower())[-1]
            #if command in commandList:
            logging.info("Bot has been summoned: ID: " + str(msg.id) + " Author: " + str(msg.author) + "\nDate: " + str(msg.created_utc) +"\nSubject: " + str(msg.subject) + "\nBody\n" + str(msg.body))
            #print("SUMMONS")
            #print(msg.id)
            summonID = msg.id
        #print(msg.body)
    elif not msg.was_comment:
        # Was a direct message
        if msg.author.lower() in  ['iamkindofcreative', 'u/iamkindofcreative']:
            if 'kplot' in msg.body.lower():
                # Call the karma plot thingy
                command = 'kplot'
                summonID = msg.id
    
    return summonID, command


def handleInbox(reddit, codeVTextClassifier, setOfPosts={}, unreadCount=None, sendText = True, quietMode=False):
    # Mark all messages as read after notification has been sent
    rawInboxMessages = archiveAndUpdateReddit.checkForMessages(reddit)
    sendText = True
    
    # Handle Summoning:
    inboxMessages = []
    summonMsgs = []
    summonedIDs = []
    if len(rawInboxMessages) == 1:
        logging.debug("Checking Inbox.. 1 message")
    else:
        logging.debug("Checking Inbox.. "+str(len(rawInboxMessages)) + " message(s)")

    for msg in rawInboxMessages:
        summoned, command = checkForSummons(msg)
        if summoned != None:
            # Reply
            # Pass message off to summoning processor, 
            # Act on summons,
            # Reply to summoner 
            # mark summoning as read
            summonMsgs.append(msg)
            summonedIDs.append(summoned)
            actOnSummons(reddit, msg, command, codeVTextClassifier, quietMode, setOfPosts)
        else:
            inboxMessages.append(msg)

    # Commented out during testing:
    if len(summonedIDs) > 0:
        logging.debug(str(len(summonedIDs)) + " summoning messages, clearing them..")
        # Not sure if I should clear summons during testing..
        #if not quietMode:
        #    archiveAndUpdateReddit.markSummonsAsReadMessages(reddit, msgIDs =summonedIDs)
        archiveAndUpdateReddit.markSummonsAsReadMessages(reddit, msgIDs =summonedIDs)

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
                # Check to see if it was a karma summons
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

    
