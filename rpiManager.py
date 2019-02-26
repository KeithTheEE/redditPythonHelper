


'''
Keith Murray


Logging 'not working' error notes can be found here
https://stackoverflow.com/questions/42431418/python-logging-multiple-modules-logger-not-working-outside-main-program

it appears that when main.py is run on the pi (currently running py2.7), an import sets 
logging ahead of the main settings, causing logging to just be printed

'''

import subprocess
import traceback
import socket
import sys
import os
import time
import logging
import threading
import datetime

from utils import rpiGPIOFunctions
from utils import textSupervision

import nltk
nltk.data.path.append('/home/pi/nltk_data')

import matplotlib
matplotlib.use('Agg')






'''
Pin Numbers	RPi.GPIO	Raspberry Pi Name	BCM2835		USED AS
P1_01		1		3V3	 
P1_02		2		5V0	 
P1_03		3		SDA0			GPIO0
P1_04		4		DNC	 
P1_05		5		SCL0			GPIO1
P1_06		6		GND	 				GND
P1_07		7		GPIO7			GPIO4
P1_08		8		TXD			GPIO14		TXD
P1_09		9		DNC	 
P1_10		10		RXD			GPIO15		RXD
P1_11		11		GPIO0			GPIO17	
P1_12		12		GPIO1			GPIO18
P1_13		13		GPIO2		 	GPIO21
P1_14		14		DNC	 
P1_15		15		GPIO3			GPIO22
P1_16		16		GPIO4			GPIO23
P1_17		17		DNC	 
P1_18		18		GPIO5			GPIO24
P1_19		19		SPI_MOSI		GPIO10
P1_20		20		DNC	 
P1_21		21		SPI_MISO		GPIO9
P1_22		22		GPIO6			GPIO25
P1_23		23		SPI_SCLK		GPIO11
P1_24		24		SPI_CE0_N		GPIO8
P1_25		25		DNC	 
P1_26		26		SPI_CE1_N		GPIO7
pin setup on PI 
        1   2 
        3   4
        5   6  --GND
BUTTON-	7   8  
  VCC--	9  10  
        11 12  --RED 
YELLOW-	13 14
 BLUE--	15 16  --HEARTBEAT
        17 18  --GREEN
        19 20
        21 22 
        23 24
        25 26
'''



class heartBeatThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name="HeartBeatThread"
        self.daemon = True
        self._stop = threading.Event()
    def run(self):
        logging.debug("STARTING THAT SICK BEAT YO (from the thread)")
        rpiGPIOFunctions.heartBeat()
    def stop(self):
        logging.debug("The Beat has Dropped")
        self._stop.set()
    def stopped(self):
        return self._stop.isSet()

class redditThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name="RedditBotThread"
        self.daemon = True
        self._stop = threading.Event()
    def run(self):
	    logging.debug("Starting reddit bot from thread")
	    botStuff()
	    logging.debug("I seem to have escaped from the threads")
    def stop(self):
	    self._stop.set()
    def stopped(self):
        return self._stop.isSet()

class restartButtonThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name="restartButtonThread"
        self.daemon = True
        self._stop = threading.Event()
    def run(self):
        logging.debug("Button thread is active")
        rpiGPIOFunctions.buttonListener()
    def stop(self):
        logging.debug("Button Button I'm done with the button")
        self._stop.set()
    def stopped(self):
        return self._stop.isSet()



def startupSwitchFlag():
    action = 'F0'
    



    return action

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


def pull_from_github():
    online = is_connected()
    while not online:
        online = is_connected()
        time.sleep(30)

    process = subprocess.Popen(["git", "pull", "origin", "master"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    logging.info(output)

    return
                

def botStuff():
    time.sleep(30)

    reddit, classifier, codeVTextClassifier, tdm, userNames, postHistory = main.startupBot()
    try:
        main.runBot(reddit, classifier, codeVTextClassifier, tdm, userNames, postHistory)
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
        textSupervision.send_update(msg)
    return


def allBotActions():
    
    heartB = heartBeatThread()
    powerButton = restartButtonThread()
    redditBot = redditThread()

    #botStuff()
    
    try:
        heartB.start()
        powerButton.start()
        #while True:
        #    redditBot.start()
        #    break # This break will be removed later
    except(KeyboardInterrupt, SystemExit):
        print("LKEYOI")
        logging.info("Keyboard interrupt or System Exit has occurred")
        heartB.stop()
        redditBot.stop()
        raise KeyboardInterrupt
        #powerButton.stop()
    try:
        botStuff()
        print("Oppsie")
    except(KeyboardInterrupt, SystemExit):
        print("ssssss")
        logging.info("Keyboard interrupt or System Exit has occurred after botstuff")
        heartB.stop()
        redditBot.stop()
        raise KeyboardInterrupt
        #powerButton.stop()
    except:
        # Something is going sour here: see breakingErrorReport.log
        #   which is the last 1k lines of a log where the program shutdown
        #   but kept the button active after this point
        logging.info("An Unkonwn error has occurred")
        heartB.stop()
        powerButton.stop()
    finally:
        logging.debug("I guess I'm done")
        heartB.stop()
        powerButton.stop()

    
        print("LKEYOI asd sd")

    print("L:KJL:K1")
    
    return


if __name__ == "__main__":
    # Logging Stuff 
    dirName = "logs"
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    logFileName =   'LOG_'+ datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.log'
    filePath = os.path.join(dirName, logFileName)
    logging.basicConfig(filename=filePath, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s():%(lineno)s - %(message)s')

    # check GPIO Flags
    # F0: Continue as is
    # F1: Pull code from repo origin master
    # F2: Do not begin program
    action = startupSwitchFlag()
    logging.debug('Startup Action: '+ action)
    if action == 'F1':
        # Pull source
        logging.debug("Pulling Source from Origin Master")
        pull_from_github()
    elif action == 'F2':
        logging.debug("As per startup Switch Flag, exiting program and not running")
        sys.exit(0) # Successful exit
    # 




    # Importing here to prevent the "import logging"
    import main
    resetTries = 0
    resetLimit = 3
    sleepDurationS = 30
    kbi = False
    while resetTries < resetLimit:
        try:
            allBotActions()
        except KeyboardInterrupt:
            print("KBI")
            logging.debug("Keyboard Interrupt: Ending Program from rpiManager")
            kbi = True
            break
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
            #textSupervision.send_update(msg)
        resetTries += 1
        time.sleep(sleepDurationS*resetTries)
    logging.debug("Exited the program, ending rpiManager if __name__=='__main__.")

    logging.debug("Leaving power button alive")
    if not kbi:
        textSupervision.send_update("Exited the program, ending rpiManager\nLeaving power button alive")
    powerButton = restartButtonThread()
    powerButton.start()
