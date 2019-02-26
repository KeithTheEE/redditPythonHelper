

import kmmessage
import time
import logging


'''  
Keith Murray 
email: kmurrayis@gmail.com
'''
from asecretplace import getPythonHelperBotKeys
smstoaddr = getPythonHelperBotKeys.GETSMSADDR()
mmstoaddr = getPythonHelperBotKeys.GETMMSADDR()
emailtoaddr = getPythonHelperBotKeys.GETEMAILADDR()

def getUserFeedbackViaText(outgoingMsg, recipAddr=smstoaddr, tryAgainDelayMin=5):
    """
    Sends a text message to the recipient and waits for a reply
    Parameters
    ----------
    outgoingMsg : str
        The message going to the user
    recipAddr : str
        Email Address string the recipient is at
    tryAgainDelayMin : int
        Number of minutes between each repeated sent message. Networks don't often 
        prioritize these messages, and 'loose' them fairly frequently, or don't 
        pass them through until multiple hours have passed. If there's no reply
        in `tryAgainDelayMin` time, another message is sent, until `resendTotalCount`
        attempts have been made
    Returns
    -------
    msg : str
        The body of the email recieved IF it came in after the outgoing message was 
        sent and before the `hardStopLimitMin` timelimit has been reached and was 
        sent by the same address as `recipAddr`.  If `hardStopLimitMin` is reached,
        returns an empty string.
    Notes
    -----
    It's not the cleanest function, but it works
    Eventually I will build in a varible that mutes the messages between a defined 
    timespan (night or during work hours)
    """
    # Bodge it
    quietAtNight = False
    tryResending = True
    resendTotalCount = 3
    if tryAgainDelayMin == -1:
        tryResending = False
    hardStopLimitMin = 60
    
    # Flush pop queue
    msg_From, msg_Body = kmmessage.checkForMessage()
    
    # Message User
    kmmessage.sms_message_Send(msg=outgoingMsg, recip=recipAddr)
    
    # wait for reply
    startTime = time.time()
    shortWaitStart = startTime
    sentCount = 1
    while True:
        timeSince = time.time() - startTime
        # Hard break if there's been no reply for a long period
        if timeSince > hardStopLimitMin*60:
            # It's over, we've waited too long. Time to move on
            msg = ""
            break
        # Resend message in case it got lost (happens mildly often)
        # Happened, 3 messages, zero recieved 
        if tryResending:
            if sentCount < resendTotalCount:
                if (time.time() - shortWaitStart) > (tryAgainDelayMin * 60):
                    kmmessage.sms_message_Send(msg=outgoingMsg, recip=recipAddr)
                    sentCount += 1
                    shortWaitStart = time.time()
        # Wait and check for new email
        time.sleep(30)
        msg_From, msg_Body = kmmessage.checkForMessage()
        msg = ""
        # Parse new emails to see if they're from recipAddr
        for i in range(len(msg_From)):
            trimmed = msg_From[i].strip('<').strip('>')
            print(recipAddr, trimmed)
            logging.debug(recipAddr, trimmed)
            
            if recipAddr == trimmed:
                msg = msg_Body[i]
                break
        if msg != "":
            break
            
    return msg

def send_update(outgoingMsg, recipAddr=smstoaddr):
    # Message User
    
    maxTotalWaitTime = 5*60*60
    backoffTime = 30 # starting amount of time required to wait after an error. it will then double
    maxBackoffTime = 60*60
    i = 0
    startTime = time.time()
    while True:
        try:
            kmmessage.sms_message_Send(msg=outgoingMsg, recip=recipAddr)
            break
        except Exception as err:
            logging.info("Caught exception\n" + err)

        # Grow the amount of time it tries
        if time.time()-startTime > maxTotalWaitTime:
            break
        wait = min(backoffTime* (2**i), maxBackoffTime)
        time.sleep(wait)
        i += 1
    return 

def send_karma_plot(outgoingMsg, outMedia, sbjLine, recipAddrMMS=mmstoaddr, recipAddrEmail=emailtoaddr):
    # Message User
    
    maxTotalWaitTime = 5*60*60
    backoffTime = 30 # starting amount of time required to wait after an error. it will then double
    maxBackoffTime = 60*60
    i = 0
    startTime = time.time()
    while True:
        try:
            logging.debug("Sending Karma Plot: Email")
            kmmessage.message_Send_Full_Email([recipAddrEmail], sbjLine, outgoingMsg, files=[outMedia])
            time.sleep(1)
            logging.debug("Sending Karma Plot: MMS")
            kmmessage.mms_message_Send(recipAddrMMS,outgoingMsg,outMedia)
            break
        except Exception as err:
            logging.info("Caught exception\n" + err)

        # Grow the amount of time it tries
        if time.time()-startTime > maxTotalWaitTime:
            break
        wait = min(backoffTime* (2**i), maxBackoffTime)
        time.sleep(wait)
        i += 1
    return
