

# CHANGELOG: Python Helper Bot Version pre Alpha A0.2.00
All notable changes to this project will be documented in this file.

The format is loosely based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).
It wont adhere perfectly, but it's a start. 

Dates follow YYYY-MM-DD format

> Do you remember the Machine’s own statement when you presented
> the problem to him? It was: ‘The matter admits of no explanation.’ The Machine did not
> say there was no explanation, or that it could determine no explanation. It simply was not
> going to admit any explanation. In other words, it would be harmful to humanity to have
> the explanation known, and that’s why we can only guess -- and keep on guessing.”

-- Susan Calvin in "I, Robot" by Isaac Asimov



## [A0.2.00] 2019-XX-XX
In Progress
### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

This project is not currently looking for other contributors

#### Big Picture: What happened, what was worked on

Folder structure has been redone, most helper functions have been moved to the utils folder. The code for vA0.1.01 has been posted to github so it's easier to completely mess up the vA0.2.00 update and have the ability to undo it. 


#### Added
 - The bot is now licensed under the MIT license
 - Source code has been posted to github (it's a big deal: woo!)
 - .gitignore file has been made
 - associated personal libraries have also been posted github
 - botHelperFunctions.coolPlacesToDonate(): a function (currently empty) that returns a website asking for donations. Ideally it's be sites that are non profit, and are for causes that either center around the bots actions, or center around my own favorite charities. Should rarely trigger.
 - botHelperFunctions.ramCheck(): Currently empty function. will return how much ram is being used and how much is free. Hopefully this will help when the pi runs for months then suddenly stops working, giving me a chance to see if there was a slow and creeping memory error. 
 - botHelperFunctions.load_autoreply_key_phrases(): rather than hard coding, key phrases can be loaded into a text file.
 - formatCode.py: a module to take in a submission or comment, and reformat it adding 4 spaces to help display the code on reddit. 
 - botSummons.py: a module to process any and all keyword summoning. 
 - misc/pyProgramTrainingLines.txt: training file for the 'code' classification, the 'text' is taken from the nltk Brown sentence corpus on 'news'. 
 - buildComment.py has been added, now functions as the holding ground for variations on the primary bot comment. 
 - learningSubmissionClassifiers.py has been added, though it is not currently active. It's intended to be base home of the post classifiers, clearing up the main and making modifications easier. 
 - archiveAndUpdateReddit: Ho Boy we're in for a lot here. Almost everything in this file has been changed to wrap all possible praw api calls into a custom class which has ugly but hopefully functional try/excepts wrapped in a while True loop attached to a backoff timer such that any time any anticipated exception gets raised. This should prevent the reddit server timeouts from causing random bot deaths as well as help isolate api calls to functions which are prepared for the concequences. It's big, it's ugly, but it's in a nice rubber padded room that's shielded from reality. So it works I guess. We'll see. A lot of breaking changes have been made. To comment on a submission or comment the bot now requires "quiteMode" to be passed, helping reduce errors caused by impropperly silencing the bot 




#### Changed
 - logs now record source module, function name, and line number when a log entry is named. New format is now: 
 YYYY-MM-DD HR:MN:SC,MSC - Level - module:function():line - Message
 - Most helper functions have been moved to a seperate folder named utils. This should help reduce clutter 
 - learningSubs.txt has been moved to misc/learningSubs.txt
 - codeVTextClassifier is now added to the startup and runbot functions, changing the return and in args respectively
 - shortenRedditURL(url) has been moved from main to botHelperFunctions module



#### Deprecated
 - buildHelpfulComment has been changed and rename as buildHelpfulComment_DEPRECATED with a new buildHelpfulComment acting in the same namespace. The new one does not have the stack overflow answer section included as that's been non functional for too long, and not needed. The new one is also cleaner and easier to understand.  
 idealQuery() and stackOverflowInfo() have been commented out and will be removed soon. 
#### Removed

#### Fixed
 - Fixed some of the changelog formatting

#### Security


### Main

### rpiManager.py

### Util Libraries

#### archiveAndUpdateReddit.py
#### botHelperFunctions.py
#### botMetrics.py
#### formatBagOfSentences.py
A module to order a handed bag of sentences, and insert new lines to make paragraphs. Currently does not function. 
#### formatCode.py
Trains a classifier on code vs text, returns the classifier. Later, takes in a textBlock and classifies it on a 'newline' basis, rather than a tokenized sentence basis. The feature profile is build from a modified lz78 algorithm, where 
#### locateDB.py
#### lsalib2.py
#### questionIdentifier.py
#### rpiGPIOFunctions.py
#### scriptedReply.py
#### searchStackOverflowWeb.py
#### summarizeText.py
#### textSupervision.py
#### updateLocalSubHistory.py
#### user_agents.py

### Tests 



## [A0.1.01] 2018-12-14

### Contributors
Keith Murray

email: kmurrayis@gmail.com

twitter: [@keithTheEE](https://twitter.com/keithTheEE)

github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

This project is not currently looking for other contributors

#### Big Picture: What happened, what was worked on
Project should now run with python3.6 and python2.7


#### Added
 - scriptedReply.py 
A Module to help handle all scripted responses to frequently asked questions on the python sub. Among them will be "How to install python?" "Is Python worth learning?" "Are there tutorials on X"? 
 - main.py now has a command line arguements which enabled quiet mode, that lets the bot run without commenting or texting errors, making it easier to deal with updating the code on one machine without worrying about double commenting or other similar errors.
#### Changed
 - main.basicUserClassify():
 Added lines that text me if it runs into a user who it's already interacted with, rather than just logging it. 
 AAAANNNND A bunch of bodges around that to prevent it from spamming me over and over every x minutes it runs. 
 COME BACK TO THIS AND CLEAN IT UP LATER, THE MAIN IS GETTING MESSY
 - summarizeText.wordRankKeywords(text): 
 Adjusted the code. Previously it was returning significantly different results than the textRank paper, now it's strongly similar, with differences that can reasonably be explained by the networkx implementation of the pagerank algorithm, as well as the nltk part of speech tagger. 
 - rpiManager:
 in if __name__=="__main__": If an error occurs (specifically if a reddit server based error) the program will log it, then restart. the restart will occur `resetLimit` times, and before restarting will wait 30 seconds * the number of previous restart tries. 
 - rpiManager:
 NLTK and matplotlib are now also imported in rpiManager. NLKT is imported, then the data path for the libraries on the pi are appended. matplotlib is imported then sets background manager to 'Agg' for the pi as well
 - rpiManager.allBotActions():
 in the except case for keyboardInterrupt, after handling stopping threads, it also raises a keyboard interrupt for the main level to handle gracefully  
 - Print statements now use () 
 - Expanded keyword auto-response
 - Updated the bot comment to include reference to the python discord channel
 - Updated the signature to link to the readme and FAQ hosted on github

#### Deprecated
#### Removed
 - def showMeSomething has been removed, the bot has moved past this function's usefulness
#### Fixed

#### Security


### Main

### Libraries

### archiveAndUpdateReddit.py
### botHelperFunctions.py
### botMetrics.py
### getChatBotKeys.py
### getPythonHelperBotKeys.py
### locateDB.py
### questionIdentifier.py
### rpiGPIOFunctions.py
### rpiManager.py
### searchStackOverflowWeb.py
### summarizeText.py
### textSupervision.py
### updateLocalSubHistory.py
### user_agents.py

### Tests 


## [A0.1.00] 2018-07-30

### Contributors
Keith Murray
email: kmurrayis@gmail.com
twitter: [@keithTheEE](https://twitter.com/keithTheEE)
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

#### Big Picture: What happened, what was worked on
The bot runs on the pi! 

There's relatively few changes that took place between A0.0.06 and A0.1.00, however because the bot is running sucessfully on the pi and has fairly solid performance, this update is a milestone. The bot successfully meets the early goal of redirecting users to r/learnpython if it decides a user's post belongs there. This functionality runs and is maintainable on the raspberry pi, and can pull updates from github once the code is published there. 

While the bot still is in need of many features, the movement to the pi will allow me to focus on the second early goal of the bot, helping a user arrive at a solution to their problem.

#### Added
 - on boot the pi runs the bot without the need for user input
 - rpiManager.py
 Module to run main.py on the pi. main.py is called from here and runs all pi based housekeeping and management functions. Starts Logging and catches and exits program on unexpected errors after error has been logged and message has been sent for it
 - rpiGPIOFunctions.py
 Module for all GPIO interactions, LED outputs (5), and Button input (1). Handles status LEDs and restart/shutdown button
 - class rpiManager.heartBeatThread()
 thread class that calls rpiGPIOFunctions.heartBeat()
 - class rpiManager.restartButtonThread()
 thread class that calls rpiGPIOFunctions.buttonListener()
 - rpiManager.is_connected():
 not currently in use, but pings google to see if local wifi is down or reddit is down
 - rpiManager.pull_from_github():
 Not currently in use, but pulls updates from github at the git origin master. Grabbed from twitter bot and needs to be adjusted but should be fairly functional 
 - rpiManager.botStuff():
 runs main.py. Should be structured to be nearly identical to if __name__ == __main__() in main.py
 - rpiManager.allBotActions():
 After if __name__ == __main__, this function starts all threads and runs main.py
 - rpiGPIOFunctions.ledCycle():
 blinks each LED on startup to show they work
 - rpiGPIOFunctions.myLED():
 Not currently in use. Takes in string that defines which LED to turn on. Acts as an status to show what the main.py program is doing at any given moment.
 - rpiGPIOFunctions.heartBeat():
 blinks an LED (white connected to pin 16) off and on for a second each to show the large program is still alive. 
 - rpiGPIOFunctions.buttonListener():
 watches the button (pin 17) to see if the user has pressed it. If press is less than 7 seconds it calls a raspberry pi system restart, if it's longer it calls a system shutdown. If testing set to true, instead of calling a system reboot or shutdown, it prints what kind of press was made. 
 - rpiGPIOFunctions.testPinConnections: 
 runs through each LED and blinks them to verify each LED works. After that, runs buttonListener() in testing mode to verify the LED works and prints the button press on the terminal


#### Changed
#### Deprecated
#### Removed
#### Fixed

#### Security


### Main

### Libraries

### archiveAndUpdateReddit.py
### botHelperFunctions.py
### botMetrics.py
### getChatBotKeys.py
### getPythonHelperBotKeys.py
### locateDB.py
### questionIdentifier.py
### rpiGPIOFunctions.py
- rpiGPIOFunctions.myLED():
 Not currently in use. Takes in string that defines which LED to turn on. Acts as an status to show what the main.py program is doing at any given moment.
 - rpiGPIOFunctions.heartBeat():
 blinks an LED (white connected to pin 16) off and on for a second each to show the large program is still alive. 
 - rpiGPIOFunctions.buttonListener():
 watches the button (pin 17) to see if the user has pressed it. If press is less than 7 seconds it calls a raspberry pi system restart, if it's longer it calls a system shutdown. If testing set to true, instead of calling a system reboot or shutdown, it prints what kind of press was made. 
 - rpiGPIOFunctions.testPinConnections: 
 runs through each LED and blinks them to verify each LED works. After that, runs buttonListener() in testing mode to verify the LED works and prints the button press on the terminal

### rpiManager.py

 - class rpiManager.heartBeatThread()
 thread class that calls rpiGPIOFunctions.heartBeat()
 - class rpiManager.restartButtonThread()
 thread class that calls rpiGPIOFunctions.buttonListener()
 - rpiManager.is_connected():
 not currently in use, but pings google to see if local wifi is down or reddit is down
 - rpiManager.pull_from_github():
 Not currently in use, but pulls updates from github at the git origin master. Grabbed from twitter bot and needs to be adjusted but should be fairly functional 
 - rpiManager.botStuff():
 runs main.py. Should be structured to be nearly identical to if __name__ == __main__() in main.py
 - rpiManager.allBotActions():
 After if __name__ == __main__, this function starts all threads and runs main.py

### searchStackOverflowWeb.py
### summarizeText.py
### textSupervision.py
### updateLocalSubHistory.py
### user_agents.py

### Tests 

## [A0.0.06] 2018-07-22

### Contributors
Keith Murray
email: kmurrayis@gmail.com
twitter: [@keithTheEE](https://twitter.com/keithTheEE)
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

#### Big Picture: What happened, what was worked on

#### Added
#### Changed
#### Deprecated
#### Removed
#### Fixed

#### Security


### Main

### Libraries

### archiveAndUpdateReddit.py
### botHelperFunctions.py
### botMetrics.py
### getChatBotKeys.py
### getPythonHelperBotKeys.py
### locateDB.py
### questionIdentifier.py
### searchStackOverflowWeb.py
### summarizeText.py
### textSupervision.py
### updateLocalSubHistory.py
### user_agents.py

### Tests 


## [A0.0.05] 2018-07-16

### Contributors
Keith Murray
email: kmurrayis@gmail.com
twitter: [@keithTheEE](https://twitter.com/keithTheEE)
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

#### Big Picture: What happened, what was worked on
This update focused on documentation, and internal code updates. The bot might not have said or acted much differently from the outside, but a lot of the changes occurred to make seeing the usefulness of the bot simpler, and evaluating mistakes easier. Logging was improved, and botMetrics was added: a suit to see how the bot is performing, and characterize the performance. 

#### Added
 - main.checkInbox: during runBot this will check the inbox and send a text if there's a new unread message
 - archiveAndUpdateReddit.checkForMessages(reddit) returns unread messages from reddit account
 - textSuperVision.send_update(outgoingMsg, recipAddr='defaultAddr') to just send a text
 - botMetrics.karmaPlotstoGif(outfileName, filePath) takes all karma plots and turns them into a gif
 - botMetrics.totalKarmaLinePlot() line plot of karma over time
 - summarizeText.stripURL() remove the url present in any given string.
 - botMetrics.measureUserReaction(post, user, suggestionTime) takes the original post, user name in question, and the time the bot made the suggestion to see if the user took the redditbots advice. The function is not yet in use. 
 - botHelperFunctions.py a module for functions which clutter main.py but are specific to the bot's functionality. 
 - botHelperFunctions.get_learning_sub_Names() grabs a list of subs classified as 'learning subs' which the user should post their questions in. 
 - main.getSubsUsersInteractsIn(user, limitCount=25) looks at the 25 most recent comments and 25 most recent posts a user has made and returns a dictionary with a key value pair of subreddit as the key, and number of interactions in that subreddit as the value, a boolean whether or not they have said 'r/learnpython' in their comments, and a list of all posts (in that 25) in learning related subs
 - main.user_Already_Took_Advice() Checks OPs post history to see if they already posted the question to a learning sub

#### Changed
 - summarizeText.parseStringSimple01(text, removeStopwords=False, removeURL=False) now has an optional input varible (boolean) to remove stopwords, where the default is False. It also has the option to remove a url automatically, default is set to True
 -  main.basicUserClassify() returns boolean and list of learning subs op has posted in

#### Deprecated
 - main.searchStackOverflowWeb.py is not fuctional and not in use
 - main.idealQuery() currently being called but not applied

#### Removed
 - mosestokenizer No longer included with NLTK and has been removed from summarizeText.py

#### Fixed
 - summarizeText.parseStringSimple01(text, removeStopwords=False) should now let main.request_Key_Word_Filter() and logging.debug(str(classified) +': '+ str(sent)) function as anticipated. Previously logged sentences and requested key words were not directly present in the original post. Stopword removal was quietly occuring. Now if stopwords are removed, it should be explicit. 

#### Security


### Main

 - checkInbox: during runBot this will check the inbox and send a text if there's a new unread message. In the event that there is, it will text me so I can see what was said, and if I need to reply 
 - main.getSubsUsersInteractsIn(user, limitCount=25) looks at the 25 most recent comments and 25 most recent posts a user has made and returns a dictionary with a key value pair of subreddit as the key, and number of interactions in that subreddit as the value, a boolean whether or not they have said 'r/learnpython' in their comments, and a list of all posts (in that 25) in learning related subs
 - main.user_Already_Took_Advice() Checks OPs post history to see if they already posted the question to a learning sub


### Libraries


### archiveAndUpdateReddit.py
 - archiveAndUpdateReddit.checkForMessages(reddit) returns unread messages
 
### botHelperFunctions.py
 - botHelperFunctions.get_learning_sub_Names() loads a list of learning and question focused subs from a text file 

### botMetrics.py
 - botMetrics.karmaPlotstoGif(outfileName, filePath) takes all karma plots and organizes them into a gif to see how the bot is performing 
 - botMetrics.totalKarmaLinePlot() line plot of karma over time

### getChatBotKeys.py
### getPythonHelperBotKeys.py
### locateDB.py
### questionIdentifier.py
### searchStackOverflowWeb.py
Not currently in use until a new rebound update is pushed

### summarizeText.py
 - mosestokenizer No longer included with NLTK : summarizeText.detokenize(token_text) just returns a space sepperated, joined string.
 - summarizeText.stripURL():
remove the url present in any given string. Evaluate ways to replace the url 
with some other placeholder
 - summarizeText.parseStringSimple01(text, removeStopwords=False, removeURL=True) now has an optional input varible (boolean) to remove stopwords, where the default is False. It also has the option to remove a url automatically, default is set to True

### textSupervision.py
 - textSuperVision.send_update(outgoingMsg, recipAddr='defaultAddr') to just send a text

### updateLocalSubHistory.py
Empty

### user_agents.py

### Tests 
