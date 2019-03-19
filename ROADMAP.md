

# ROADMAP: Python Helper Bot Version pre Alpha A0.2.01
Future expansions are considered in this file. 
Their presence is not a promise that they'll exist, but rather this file serves as an
early outline of features this project hopes to add, as well as changes in directions


The format is adapted from [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).
It wont adhere perfectly, but it's a start. 


Dates follow YYYY-MM-DD format

> Do you remember the Machine’s own statement when you presented
> the problem to him? It was: ‘The matter admits of no explanation.’ The Machine did not
> say there was no explanation, or that it could determine no explanation. It simply was not
> going to admit any explanation. In other words, it would be harmful to humanity to have
> the explanation known, and that’s why we can only guess -- and keep on guessing.”

-- Susan Calvin in "I, Robot" by Isaac Asimov



## [A0.3.00] 2019-XX-XX
In Progress
### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

### Short Term Roadmap

With the class wrappers in place, archiving should be significantly easier. 
This next update will probably decide a database structure, and either start archiving posts via the bot on the pi, or a clone bot on my primary computer. Before the SO search engine can be rigorously tested, I will need sample data, so archiving is finally a real priority, as oppose to an ideal priority. 

The bot summoning could use some work. While it's summons works well, it could classify when the bot has been summoned to reformat code that has indent errors, and say when it expects it can't help with reformatin, but refer to reformatting help



#### Add
 - [X] Hardware: USB or USB connected Sata drive.
 - Migrate most files to usb/usb-sata drive to host. Watch power requirements. 
 - Build a 'light archive' which will save posts as either xml or json (json has been selected). This should build in db focused structure and function calls, without requiring a db commitment. 
 - With light archive, build a 'save state' and 'load state' function so records on new posts aren't lost during reboots.
 - [X] (NO CHANGE MADE) Verify the key phrase response checks for self post v image post. Ok this code is written and in learningSubmissionClassifiers, but after looking through the older versions of this, it never was a requirement. And it's usually pretty spot on. The code is commented out, so think on it for a while. [Update] While it comments on non self posts, these are pretty accurate and I don't view this as an issue. I'll allow it to continue to post on non self posts if a key phrase is used
 - loggingSetup.py: a module to be imported first by rpiManager and main, which sets up the logging format so the program can be called by either module on any system and initialize in the same way
 - botHelperFunctions/botMetrics: Add ram usage check and log it in every 'awake' cycle of program, to try and tease out any possible MemeoryError's kicking up after long periods of time. Might as well save other diagnostics info, maybe call this from the hearbeat thread so it becomes a better representation of runtime
 - rpiManager.startupSwitchFlag(): 
 Moving this higher up.
 A function which polls one of the gpio pins to see if it's low (normally high) (or flipped levels). That pin will be tied to a jumper or switch. When set, the bot will not turn on at boot, allowing for simpler diagnostics, updates, etc. 
 Also a pull origin master from github state would be incredibly useful
 - Verify reddit post logs by grabbing most recent bot comments. This should reduce risk of two computers commenting on the same post which could happen if databases are de-synced and one computer is not in quiet mode because I typed in the wrong command. Opperator Error Risk Reduction. Only the most recent x+buffer hours of interaction are needed. This does not protect from multiple posts by the same user but should prevent multiple comments on the same post even if the bot runs on different computers. 
 - Full Test Suite: PRIORITY (Ok it'll have to wait until posts have been archived, but it'll still be nice)
 - Archive Posts: PRIORITY
    Solidify what values to save, and what to save them with. Probably build an SQL to XML or JSON exporter for third party testing.
 - botMetrics.measureUserReaction(): 
 A function focused on seeing if a user did in fact go to
 r/learnpython after the bot made its suggestion. Currently built (kind of, the praw wrappers messed it up a bit), now need to add 
 functionality in main.py to use it
 - Continue Documentation in functions, add documentation files too
 - A queue which has inputs added to it by functions, and removed by the raspberry pi gpio handler, allowing the bot to change LED status based on what it's doing. Similar to the twitter event bot design (sepperate project).
 - Deprecate karma scatter plot: or change it post all posts in the past week to minimize size. It's no longer useful or very interesting. Maybe activate it once a week or something too
 - Consider creating praw rewrapper (prawRegift) to hold all praw focused wrappers and sepperate it from the phb functions. This will make it easier to have the same protections on other bots as necessary. 
 


#### Change
 - Move NLP functions from NLTK (used in many files) to a buffer module, allowing for simpler, universal changes to be made. For example, if there is a better POS tagger than nltk.pos_tag(sent) then we can easily switch to that. Right now NLTK is used over a fairly large filespace making adjustments of that sort difficult. 
 - Review all my logging notes. See what should be dropped, changed, etc. 
 - Make sure the bot defaults to commenting about formatting even if there's no code present
 - When errors occur, or a shutdown button is pressed, attempt to save current reddit info into a temp file. on startup, load that info in then connect with praw to expand the knowledge base. 


#### Deprecate

#### Remove

#### Fix
 - Standardize function name style. Either underscore or camelcase, just not both
 Probably preferable to use underscore, the despite camelcase being faster..

#### Security
#### Consider



---

### General to Long Term Expansion

 - Develop terms for a walk away condition. Either End of active development and the bot remains online, end of active development and death of bot, or end of active development and project is passed on to others. Terms will almost certainly be changed constantly and the project grows and evolves, but it's nice to have an idea of what I consider to be a "complete" project. 

 - Numbering system for items in roadmap to clear up what's being worked on and what is completed from an outside perspective. A master numbering system probably is a good idea, vX.X.XX[a,c,d,r,f,s,co]XX, following version, section, and specific roadmap suggestion number. But That seems bloated and unnecessary. (Maybe this isn't worth while, maybe it is and will help catch things in the changelog. Probably wont be seriously considered until alpha)

 - summarizeText.loadEnglishModel(sourceDataPath=paths["prebuiltEnglishDB"]):
 Prebuild and pickle the output tdm of 
 summarizeText.buildModelFromDocsInFolder(sourceDataPath=paths["englishDB"])
 so the raspberry pi doesn't have to hit memory errors in in main.startupBot()
 load the prebuilt database and build it if the prebuild database does not exist.
 Or just build a custom compression scheme and load that instead of using pickle.

 - test.EvaluatePost():
 Given recent restructuring, this should be much easier. Take a post given a post id, then run it through the classifier where the exitpoints are turned off from the functions, forcing it to classify the post in full. Because the praw wrappers are in place, there shouldn't be a concern about forcing full evaluation any more. This can be considered to be half completed: the silent mode the bot has helps evaluate posts. 
 
 - Reply To Common posts:
 Build semi scripted replies to frequently asked questions (probably largely pulled from the sidebar, since that's how the side bar gets populated)
 This includes "How do I install python" and "Is learning python worth it?" (Aka "Why learn python?")--A quality version of this is a full research task. Build off of internal sentence ordering models + soft skills. Pull text from comments on these posts to build up scripted reply. Look into adapting this (or maybe starting with this) to classifying the posts so their types can be diplayed as tags. 
 
 - local Flask website/dashboard to monitor the status and logs of the bot in realtime. Low priority. 
 
 - Log processing: a set of functions and visualizations to process the log files for various useful tidbits. Something nicer than grep




### Main
 - alreadyAnswered():
 Parse through OPs comments on the thread, and search for text that implies the question
 has been answered. Adjust comment on submission accordingly, probably to say, "Next time
 you have a question like this, consider using r/learnpython" blah blah  blah 


### rpiManager.py
 - update the commented gpio naming and numbering list
 - update grab-from-github functions
 - add a queue to work with rpiGPIO for LED displays for various tasks
 


### Libraries:


### archiveAndUpdateReddit.py
Most of the 'light' archive functionallity is currently being built out, rendering a large chunk of this section of the roadmap either completed, in progress, or dismissed. It is also no longer in the realm of 'long term'. 

[x] The big set of functions necessary in this module are database creation, and update functions.
There might be two databases: one of just posts, and another comprising of posts, and comments.

ARCHIVE FUNCTIONS
TODO: Saves it into sqlite3 table after it's passed the time threshold to "not in 
use" 

"not in use" is probably going to be defined as 8 hours. Past that point the 
post will be either 'successful', 'mild', or 'unsuccessful', defined as 
x >= 8 points, 8 > x >= 1, 1 > x 

Adjust it so 'not in use' is not defined as 8 hours, but instead defined as 
a varible, which changes based on the time of day (either defined by utc or
cdt--cdt being my current local time) that the posts was made. 'Late at night' as
defined by the time where the fewest users/ r/python 'actions' (posts, upvotes, 
comments) are made, adjusted according to the day of the week and or holiday 
(unlikely that this bot will need to be that specific) the post is made on.

 r/learnpython is another source of data: 

it will act as a source of useful questions, and will allow the bot to direct
users to other reddit based questions rather than simply stack overflow (this
distinction should help allow the bot to be generalizable) 
posts between 3 and 8 upvotes will be determined as 'basic questions' and
will be used as suggested solutions if the similarity between the new r/python
post and the old r/learpython post is greater than some threshold


### botHelperFunctions.py

### botMetrics.py

 - measureUserReaction(): 
to see if redditor does post to r/learnpython. The post will have to be strongly similar
to their r/python post, and be posted not long after the python sub post

- questionAndAnswer(query): to attempt to reply to semi-scripted questions

- buildConfusionMatrix(): to measure performance

#### Confusion Matrix Traits
##### True Positive: 
[The bot has commented,] And
[[Either a mod has removed the post due to 'learning'], 
Or [the redditor posts their question on r/learnpython]]

##### False Negative: 
[The bot did not comment after 8 hours] And
[[Either a mod has removed the post due to learning,] 
Or, [[someone else has commented r/learnpython] and [has greater than 2 upvotes after 8 to 24 
hours after commenting,]]
Or, [the user posted their question on r/learnpython]]

##### False Positive: 
[The bot has commented],And [has less than -1 comment karma after 8 to 24 hours,]
And [[the post is not removed due to learning within 8-24 hours] or [by mods recent 
activity plus some threshold.]]
And [[the user does not make a similar post to r/learnpython within a timespan of 8
hours] or [4 hours after their next user activity monitored for no more than a week]]

##### True Negative:
[The bot did not comment after 8 hours] And
[[No mod has removed the post using a reference to 'learning' after 8 to 24 hours] or 
by mods recent activity plus some threshold.] And
[[No commenter has post made a post which contains 'r/learnpython'] And [has more than 2 upvotes]]

##### Fuzzy:
All Else. 
This class will be either require human moderation to place into the confusion matrix, Or
will be used for other classificaiton, such as "Blog Spam". It could be that topics placed 
in this area can be re-examined and labelled, helping the bot generalize preformance in 
other areas 

### botSummons.py
 - Finish makeFormatHelpMessage summons
### buildComment.py
### formatBagOfSentences.py
### formatCode.py
 - formatCode.py: Cleave sentence from comment and first line of code from one another 
 - formatCode.py: Using rewrapClassifications output, check to see if any indentation is present for lines that have been classified as code. If >5 lines of code are present and none of them have indents, classify block as "The reddit text editor royally screwed this one up", adjust comment to say it's unlikely that the code has been indented properly, and enter the special fixer.
 - formatCode.reformatFromHell(): Read in all previous code. Read in current line. If rfh classification Adds indent: current line is a child of the previous line. If it is the same indent level, current line is a sibling. If it is minus indent, line is a sibling of the previous lines parent. 
   - Previous code is stored in a tree like structure
   - Leverage sentence ordering ideology to say given the current line and the previous state of the code tree, which level of node in the tree should I be
 This should be an area of linguists where there's plenty of work already completed, look for it. I think Nevil-manning sequitor addresses it briefly, look at that+cited by for other work in the area.


### learningSubmissionClassifiers.py

### locateDB.py
 - load in path data from a prefernce file, and or take it as input that way the path isn't
 1. Hard coded and
 2. Hard coded in the module 
 Generic is better if it's generally useful. 

 That said, "check_though_these():" is a pretty good and simple function to move out of "locateDB.py" and into main.py

 - Call a function in this library to recast folder/file calls to the correct os format. Or just redo it everywhere in the code. 
 Whatever works best

### lsalib2.py

### questionIdentifier.py
It'd be nice to use stack overflow's user submissions and r/learnpython's 
submissions compared to 'successful' r/python submissions to build a 'programmers 
question' classifier (and expand the classifier to blogspammers). This would
make it generalizable so posts which are questions or requests ("HELP ME CODE") 
are directed to r/learnpython, posts which are clearly for click/ads are commented
on as such, and good posts are 'ignored': allowing redditors to act on it as they
choose. This is not an easy goal to acheive and is incredibly arbitary. but there
are still certain factors which can be measured and acted on. 

This will probably leverage a stack overflow search engine and compare n results 
with k or greater similarity. 

### rpiGPIOFunctions.py
### scriptedReply.py
### searchStackOverflowWeb.py
 - Scrap and rebuild with approved api and bound it to search for results between 
 local database build date and present day. Not important until after local copy of SO
 is up and running 
### summarizeText.py
 - Improve the english language model for topic modeling, and focus on programming topic modeling.
### textSupervision.py
### updateLocalSubHistory.py
### user_agents.py

### OTHER
(This is all functions that don't have a clear parent module)

 - moqaProgram

 - ELMO/BERT programs

 - reformat_User_Code():
 a function to identify python code blocks that aren't properly formated, and auto format the code
 for other reddit users. Might live it its own module.
 Currently being worked on.

 - Leverage reformat user code with automatic Q&A: Use classified code regions to match SO code regions, classified text regions to match SO text regions. Hopefully this improves the search engine and cuts the risk of added noise by a text to code block increasing precieved distance between the user query and the SO database post.
 Next If a majority of highly matching SO posts have sample code in the question, but the reddit query does not, strongly suggest adding the example code that caused the issue to the next itteration of the query.


 - question_topic_Modeling():
 This is going to take a few parts. 
   - Identify all related learning subreddits:

   - Model the topics of stack overflow questions. 

   - Model the topics in the learning subs
 Do network analysis to find the most active sub that addresses a topic: probably pagerank since it's simple and it works. It doesn't need to be state of the art, and if it can run on the pi, that's even better

   - Next take in the question, extract topics, feed the topics in the network, identify the sub that will get the best answer fastest. This means there also has to be some knowledge of the subs activity score

 - sub_Activity_Measure():
 Or score.. 
 This will probably return some arbatrary number that only makes sense in the context of other measures
 It might be a function of:
 The distance between the top 25 posts on Hot and the top 25 posts in New, where 'top' refers to 
 reddits ranking. 
 The number of comments and the absolute value of karma of those comments
 the number of unique users in those 25 posts
 The time between each activity

 Comparing the intersection of hot to new posts shows a glimps of how active the sub is without requiring the bot to look at the sub at multiple times. 

 This function would be useful with the question_topic_modeling() function and wouldn't need to run frequently. Though over multiple runs, it would have a solid understanding of how active a sub is at different times of day, which might encourage the bot to direct a user to a learning sub that is 
 active at that time. 


 - Auto Reply to common questions (Functional FAQ as it were)
  (This is probably going to be an early test of soft skills)
  * ["Possibly wanting to learn Python, is it worth it?"](https://www.reddit.com/r/Python/comments/917zxd/)

 - Use Automatic Sentence Ordering to construct the bots autoreply, reducing the mess of the code there. Should be mildly simple (ha, sure...), and allow for much more flexible commenting. Target is to have a defined intro, a 'bag of sentences' for the body, and a defined signature. The 'mildly simple' notion is built off the idea that there will be little the program can do incorrectly with that scaffolding. Look at two metrics: absolute sentence ordering, and new paragraph insertion. Maybe train on a ton of readme's, or wiki data for the new paragraph insertion. 


#### Question & Answer
Resources to draw from:
 - Stack Overflow (Primary)
 - Python Docs (Secondary)
 - Python Blog Posts (Out of Focus)
 - Scraped Github Code (Out of Focus)

Think about using a subset of highly matching SO posts code to OPs source code and using bayes in a MSAlignment fashion to guess on solution.
Most likely this is especially useful with syntax errors and stack traces. 


### Generalizing the bot: 
These are features which an ideal bot-mod would have, but which are not directly linked to a question-answer-and-redirector bot like u/pythonHelperBot (as of mid July 2018)
 - sub_Toxicisty_Score():
 Alternatively a friendly score. Bit ambigous, and doesn't immeadetly fit into the bot, but just a measure of how kind or standoffish or toxic a sub is. Certain communities tend to forget that not everyone knows everything, and it'd be nice to avoid recommending those subs.

 - blog_Spam_Flagger():
 This is actually a large but distant future goal for the bot. There's often complaints about blog spam on the python sub, and it'd be nice to have a programmatic way to define it. Even if the spammy site sees the definition, and works around it, the definition can either be altered, or the work around can be allowed. Most redditors want to see good content, so the best way around an ideal blog spam filter would be to have variable, high quality content. In which case everyone wins. Using that idea, we can start to outline the basic components of what blog spam might be. 

 High quality content is safe. High quality with respect to the python sub is probably some function of what generally does well

 Low quality can be caused by a few reasons: r/python is not the proper sub for that: ie questions
 It was recently posted: this is probably best defined as content theft, though repost is a common name for it. 

 I'm tired, I'll come back to this. 

### Tests 


## [A0.2.01] 2019-03-05
Official
### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

### Short Term Roadmap

With the class wrappers in place, archiving should be significantly easier. 
This next update will probably decide a database structure, and either start archiving posts via the bot on the pi, or a clone bot on my primary computer. Before the SO search engine can be rigorously tested, I will need sample data, so archiving is finally a real priority, as oppose to an ideal priority. 

The bot summoning could use some work. While it's summons works well, it could classify when the bot has been summoned to reformat code that has indent errors, and say when it expects it can't help with reformatin, but refer to reformatting help



#### Add
 - Hardware: USB or USB connected Sata drive.
 - Migrate most files to usb/usb-sata drive to host. Watch power requirements. 
 - Build a 'light archive' which will save posts as either xml or json. This should build in db focused structure and function calls, without requiring a db commitment. 
 - With light archive, build a 'save state' and 'load state' function so records on new posts aren't lost during reboots.
 - Verify the key phrase response checks for self post v image post. Ok this code is written and in learningSubmissionClassifiers, but after looking through the older versions of this, it never was a requirement. And it's usually pretty spot on. The code is commented out, so think on it for a while. 
 - loggingSetup.py: a module to be imported first by rpiManager and main, which sets up the logging format so the program can be called by either module on any system and initialize in the same way
 - botHelperFunctions/botMetrics: Add ram usage check and log it in every 'awake' cycle of program, to try and tease out any possible MemeoryError's kicking up after long periods of time. Might as well save other diagnostics info, maybe call this from the hearbeat thread so it becomes a better representation of runtime
 - rpiManager.startupSwitchFlag(): 
 Moving this higher up.
 A function which polls one of the gpio pins to see if it's low (normally high) (or flipped levels). That pin will be tied to a jumper or switch. When set, the bot will not turn on at boot, allowing for simpler diagnostics, updates, etc. 
 Also a pull origin master from github state would be incredibly useful
 - Verify reddit post logs by grabbing most recent bot comments. This should reduce risk of two computers commenting on the same post which could happen if databases are de-synced and one computer is not in quiet mode because I typed in the wrong command. Opperator Error Risk Reduction. Only the most recent x+buffer hours of interaction are needed. This does not protect from multiple posts by the same user but should prevent multiple comments on the same post even if the bot runs on different computers. 
 - Full Test Suite: PRIORITY (Ok it'll have to wait until posts have been archived, but it'll still be nice)
 - Archive Posts: PRIORITY
    Solidify what values to save, and what to save them with. Probably build an SQL to XML or JSON exporter for third party testing.
 - botMetrics.measureUserReaction(): 
 A function focused on seeing if a user did in fact go to
 r/learnpython after the bot made its suggestion. Currently built (kind of, the praw wrappers messed it up a bit), now need to add 
 functionality in main.py to use it
 - Continue Documentation in functions, add documentation files too
 - [X] Built off of Bot Summons, DM to the bot with 'kplot:'+postID to get karma plotted by time for that post. Hopefully this will make it easier to see vote manipulation. Probably just for me, maybe mods as well
 - A queue which has inputs added to it by functions, and removed by the raspberry pi gpio handler, allowing the bot to change LED status based on what it's doing. Similar to the twitter event bot design (sepperate project).
 - Deprecate karma scatter plot: or change it post all posts in the past week to minimize size. It's no longer useful or very interesting. Maybe activate it once a week or something too
 


#### Change
- [X] Rework Roadmap: as the bot has progressed, some short term goals have dropped in priority and can be moved towards long term or dropped completely. (These are largely in the 'add' section) 
 - Move NLP functions from NLTK (used in many files) to a buffer module, allowing for simpler, universal changes to be made. For example, if there is a better POS tagger than nltk.pos_tag(sent) then we can easily switch to that. Right now NLTK is used over a fairly large filespace making adjustments of that sort difficult. 
 - Review all my logging notes. See what should be dropped, changed, etc. 
 - Make sure the bot defaults to commenting about formatting even if there's no code present
 - When errors occur, or a shutdown button is pressed, attempt to save current reddit info into a temp file. on startup, load that info in then connect with praw to expand the knowledge base. 


#### Deprecate

#### Remove

#### Fix
 - Standardize function name style. Either underscore or camelcase, just not both
 Probably preferable to use underscore, the despite camelcase being faster..

#### Security
#### Consider



---

### General to Long Term Expansion

 - Develop terms for a walk away condition. Either End of active development and the bot remains online, end of active development and death of bot, or end of active development and project is passed on to others. Terms will almost certainly be changed constantly and the project grows and evolves, but it's nice to have an idea of what I consider to be a "complete" project. 

 - Numbering system for items in roadmap to clear up what's being worked on and what is completed from an outside perspective. A master numbering system probably is a good idea, vX.X.XX[a,c,d,r,f,s,co]XX, following version, section, and specific roadmap suggestion number. But That seems bloated and unnecessary. (Maybe this isn't worth while, maybe it is and will help catch things in the changelog. Probably wont be seriously considered until alpha)

 - summarizeText.loadEnglishModel(sourceDataPath=paths["prebuiltEnglishDB"]):
 Prebuild and pickle the output tdm of 
 summarizeText.buildModelFromDocsInFolder(sourceDataPath=paths["englishDB"])
 so the raspberry pi doesn't have to hit memory errors in in main.startupBot()
 load the prebuilt database and build it if the prebuild database does not exist.
 Or just build a custom compression scheme and load that instead of using pickle.

 - test.EvaluatePost():
 Given recent restructuring, this should be much easier. Take a post given a post id, then run it through the classifier where the exitpoints are turned off from the functions, forcing it to classify the post in full. Because the praw wrappers are in place, there shouldn't be a concern about forcing full evaluation any more. This can be considered to be half completed: the silent mode the bot has helps evaluate posts. 
 
 - Reply To Common posts:
 Build semi scripted replies to frequently asked questions (probably largely pulled from the sidebar, since that's how the side bar gets populated)
 This includes "How do I install python" and "Is learning python worth it?" (Aka "Why learn python?")--A quality version of this is a full research task. Build off of internal sentence ordering models + soft skills. Pull text from comments on these posts to build up scripted reply. Look into adapting this (or maybe starting with this) to classifying the posts so their types can be diplayed as tags. 
 
 - local Flask website/dashboard to monitor the status and logs of the bot in realtime. Low priority. 
 
 - Log processing: a set of functions and visualizations to process the log files for various useful tidbits. Something nicer than grep




### Main
 - alreadyAnswered():
 Parse through OPs comments on the thread, and search for text that implies the question
 has been answered. Adjust comment on submission accordingly, probably to say, "Next time
 you have a question like this, consider using r/learnpython" blah blah  blah 


### rpiManager.py
 - update the commented gpio naming and numbering list
 - update grab-from-github functions
 - add a queue to work with rpiGPIO for LED displays for various tasks
 


### Libraries:


### archiveAndUpdateReddit.py
The big set of functions necessary in this module are database creation, and update functions.
There might be two databases: one of just posts, and another comprising of posts, and comments.
The just posts database would need to include all data that the bot makes it's classification
based on on, including but not limited to
Karma Growth of post over time
Number of comments 

 - saveSubmissions(submission, database)
Given a submission, save the post, comments, and other relevant data. 

 - archiveAndRemoveOldSubmissions()
Given a set of posts, add it 


ARCHIVE FUNCTIONS
TODO: Saves it into sqlite3 table after it's passed the time threshold to "not in 
use" 

"not in use" is probably going to be defined as 8 hours. Past that point the 
post will be either 'successful', 'mild', or 'unsuccessful', defined as 
x >= 8 points, 8 > x >= 1, 1 > x 

Adjust it so 'not in use' is not defined as 8 hours, but instead defined as 
a varible, which changes based on the time of day (either defined by utc or
cdt--cdt being my current local time) that the posts was made. 'Late at night' as
defined by the time where the fewest users/ r/python 'actions' (posts, upvotes, 
comments) are made, adjusted according to the day of the week and or holiday 
(unlikely that this bot will need to be that specific) the post is made on.

Other adjustments include making a specific database entry for each submission, 
allowing for each comment to be easily integrated into the database. 
While this isn't something I need or want, it would make sense to build a general
reddit post database for future programs and open source uses.

It would also be useful to plot posts by upvotes and use the program to define
the boundary between 'successful' and 'mild' rather than have it hard coded.
Again it would require more data than I have currently, but removing a hard 
coded value would be desirable. 

 r/learnpython is another source of data: 

it will act as a source of useful questions, and will allow the bot to direct
users to other reddit based questions rather than simply stack overflow (this
distinction should help allow the bot to be generalizable) 
posts between 3 and 8 upvotes will be determined as 'basic questions' and
will be used as suggested solutions if the similarity between the new r/python
post and the old r/learpython post is greater than some threshold

Necessary Features
Post title (str)
Post Text (str)
Post URL (str)
Post ID (str)
Username (str)
Post Time (UTC timestamp)
karma by age (list of tuples: (karma_points (int or float), karma percent (float), UTC TimeStamp))
removed by mod (bool)
reason removed (str)
learn python suggested (bool)



### botHelperFunctions.py

### botMetrics.py

 - measureUserReaction(): 
to see if redditor does post to r/learnpython. The post will have to be strongly similar
to their r/python post, and be posted not long after the python sub post

- questionAndAnswer(query): to attempt to reply to semi-scripted questions

- buildConfusionMatrix(): to measure performance

#### Confusion Matrix Traits
##### True Positive: 
[The bot has commented,] And
[[Either a mod has removed the post due to 'learning'], 
Or [the redditor posts their question on r/learnpython]]

##### False Negative: 
[The bot did not comment after 8 hours] And
[[Either a mod has removed the post due to learning,] 
Or, [[someone else has commented r/learnpython] and [has greater than 2 upvotes after 8 to 24 
hours after commenting,]]
Or, [the user posted their question on r/learnpython]]

##### False Positive: 
[The bot has commented],And [has less than -1 comment karma after 8 to 24 hours,]
And [[the post is not removed due to learning within 8-24 hours] or [by mods recent 
activity plus some threshold.]]
And [[the user does not make a similar post to r/learnpython within a timespan of 8
hours] or [4 hours after their next user activity monitored for no more than a week]]

##### True Negative:
[The bot did not comment after 8 hours] And
[[No mod has removed the post using a reference to 'learning' after 8 to 24 hours] or 
by mods recent activity plus some threshold.] And
[[No commenter has post made a post which contains 'r/learnpython'] And [has more than 2 upvotes]]

##### Fuzzy:
All Else. 
This class will be either require human moderation to place into the confusion matrix, Or
will be used for other classificaiton, such as "Blog Spam". It could be that topics placed 
in this area can be re-examined and labelled, helping the bot generalize preformance in 
other areas 

### botSummons.py
 - Finish makeFormatHelpMessage summons
### buildComment.py
### formatBagOfSentences.py
### formatCode.py
 - formatCode.py: Cleave sentence from comment and first line of code from one another 
 - formatCode.py: Using rewrapClassifications output, check to see if any indentation is present for lines that have been classified as code. If >5 lines of code are present and none of them have indents, classify block as "The reddit text editor royally screwed this one up", adjust comment to say it's unlikely that the code has been indented properly, and enter the special fixer.
 - formatCode.reformatFromHell(): Read in all previous code. Read in current line. If rfh classification Adds indent: current line is a child of the previous line. If it is the same indent level, current line is a sibling. If it is minus indent, line is a sibling of the previous lines parent. 
   - Previous code is stored in a tree like structure
   - Leverage sentence ordering ideology to say given the current line and the previous state of the code tree, which level of node in the tree should I be
 This should be an area of linguists where there's plenty of work already completed, look for it. I think Nevil-manning sequitor addresses it briefly, look at that+cited by for other work in the area.


### learningSubmissionClassifiers.py

### locateDB.py
 - load in path data from a prefernce file, and or take it as input that way the path isn't
 1. Hard coded and
 2. Hard coded in the module 
 Generic is better if it's generally useful. 

 That said, "check_though_these():" is a pretty good and simple function to move out of "locateDB.py" and into main.py

 - Call a function in this library to recast folder/file calls to the correct os format. Or just redo it everywhere in the code. 
 Whatever works best

### lsalib2.py

### questionIdentifier.py
It'd be nice to use stack overflow's user submissions and r/learnpython's 
submissions compared to 'successful' r/python submissions to build a 'programmers 
question' classifier (and expand the classifier to blogspammers). This would
make it generalizable so posts which are questions or requests ("HELP ME CODE") 
are directed to r/learnpython, posts which are clearly for click/ads are commented
on as such, and good posts are 'ignored': allowing redditors to act on it as they
choose. This is not an easy goal to acheive and is incredibly arbitary. but there
are still certain factors which can be measured and acted on. 

This will probably leverage a stack overflow search engine and compare n results 
with k or greater similarity. 

### rpiGPIOFunctions.py
### scriptedReply.py
### searchStackOverflowWeb.py
 - Scrap and rebuild with approved api and bound it to search for results between 
 local database build date and present day. Not important until after local copy of SO
 is up and running 
### summarizeText.py
 - Improve the english language model for topic modeling, and focus on programming topic modeling.
### textSupervision.py
### updateLocalSubHistory.py
### user_agents.py

### OTHER
(This is all functions that don't have a clear parent module)

 - moqaProgram

 - ELMO/BERT programs

 - reformat_User_Code():
 a function to identify python code blocks that aren't properly formated, and auto format the code
 for other reddit users. Might live it its own module.
 Currently being worked on.

 - Leverage reformat user code with automatic Q&A: Use classified code regions to match SO code regions, classified text regions to match SO text regions. Hopefully this improves the search engine and cuts the risk of added noise by a text to code block increasing precieved distance between the user query and the SO database post.
 Next If a majority of highly matching SO posts have sample code in the question, but the reddit query does not, strongly suggest adding the example code that caused the issue to the next itteration of the query.


 - question_topic_Modeling():
 This is going to take a few parts. 
   - Identify all related learning subreddits:

   - Model the topics of stack overflow questions. 

   - Model the topics in the learning subs
 Do network analysis to find the most active sub that addresses a topic: probably pagerank since it's simple and it works. It doesn't need to be state of the art, and if it can run on the pi, that's even better

   - Next take in the question, extract topics, feed the topics in the network, identify the sub that will get the best answer fastest. This means there also has to be some knowledge of the subs activity score

 - sub_Activity_Measure():
 Or score.. 
 This will probably return some arbatrary number that only makes sense in the context of other measures
 It might be a function of:
 The distance between the top 25 posts on Hot and the top 25 posts in New, where 'top' refers to 
 reddits ranking. 
 The number of comments and the absolute value of karma of those comments
 the number of unique users in those 25 posts
 The time between each activity

 Comparing the intersection of hot to new posts shows a glimps of how active the sub is without requiring the bot to look at the sub at multiple times. 

 This function would be useful with the question_topic_modeling() function and wouldn't need to run frequently. Though over multiple runs, it would have a solid understanding of how active a sub is at different times of day, which might encourage the bot to direct a user to a learning sub that is 
 active at that time. 


 - Auto Reply to common questions (Functional FAQ as it were)
  (This is probably going to be an early test of soft skills)
  * ["Possibly wanting to learn Python, is it worth it?"](https://www.reddit.com/r/Python/comments/917zxd/)

 - Use Automatic Sentence Ordering to construct the bots autoreply, reducing the mess of the code there. Should be mildly simple (ha, sure...), and allow for much more flexible commenting. Target is to have a defined intro, a 'bag of sentences' for the body, and a defined signature. The 'mildly simple' notion is built off the idea that there will be little the program can do incorrectly with that scaffolding. Look at two metrics: absolute sentence ordering, and new paragraph insertion. Maybe train on a ton of readme's, or wiki data for the new paragraph insertion. 


#### Question & Answer
Resources to draw from:
 - Stack Overflow (Primary)
 - Python Docs (Secondary)
 - Python Blog Posts (Out of Focus)
 - Scraped Github Code (Out of Focus)

Think about using a subset of highly matching SO posts code to OPs source code and using bayes in a MSAlignment fashion to guess on solution.
Most likely this is especially useful with syntax errors and stack traces. 


### Generalizing the bot: 
These are features which an ideal bot-mod would have, but which are not directly linked to a question-answer-and-redirector bot like u/pythonHelperBot (as of mid July 2018)
 - sub_Toxicisty_Score():
 Alternatively a friendly score. Bit ambigous, and doesn't immeadetly fit into the bot, but just a measure of how kind or standoffish or toxic a sub is. Certain communities tend to forget that not everyone knows everything, and it'd be nice to avoid recommending those subs.

 - blog_Spam_Flagger():
 This is actually a large but distant future goal for the bot. There's often complaints about blog spam on the python sub, and it'd be nice to have a programmatic way to define it. Even if the spammy site sees the definition, and works around it, the definition can either be altered, or the work around can be allowed. Most redditors want to see good content, so the best way around an ideal blog spam filter would be to have variable, high quality content. In which case everyone wins. Using that idea, we can start to outline the basic components of what blog spam might be. 

 High quality content is safe. High quality with respect to the python sub is probably some function of what generally does well

 Low quality can be caused by a few reasons: r/python is not the proper sub for that: ie questions
 It was recently posted: this is probably best defined as content theft, though repost is a common name for it. 

 I'm tired, I'll come back to this. 

### Tests 


## [A0.2.00] 2019-01-10
Official
### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

### Short Term Roadmap

There will probably be a large update to move the bot to v0.2.00. Moving to v0.2.00 will signify major changes in the way praw varibles are handled, including remapping them into a custom class to reduce unexpected errors caused by either the reddit server being down, or the bot exceeding api call limits. The custom class will hold a majority of the info the bot might need at any given classification level, as well as being simpler to save and repopulate from disk. This should then make more complex classifiers easier to build. Key values include whether or not the post was removed by a mod based on learning or spam, whether or not the user was suggested to 'read the sidebar' or go to r/learnpython, and the score of the commenter who made the suggestion. Other useful elements include if the bot commented, and what it's score was. These should all directly be useful with the bot confusion matrix. 


#### Add
    
 - [X] Submission, Comment, Users, and Messages are getting a new class structure. 
    This is going to be based heavily off of networkEval's design (a sepperate bot), and should provide a number of wonderful little side effects, but will come at an API call cost. This is currently being worked on and should hit the next change log, and also bring about a large version change this next time around.
    Side effects include but are not limited to archiving posts, samples a test suite can draw from, and fewer unexpected errors caused because I assumed praw populated that varible so I didn't put it in a try except block and oh god how are reddit servers so spotty. 

 - Numbering system for items in roadmap to clear up what's being worked on and what is completed from an outside perspective. A master numbering system probably is a good idea, vX.X.XX[a,c,d,r,f,s,co]XX, following version, section, and specific roadmap suggestion number. But That seems bloated and unnecessary. (Maybe this isn't worth while, maybe it is and will help catch things in the changelog)

 - Verify reddit post logs by grabbing most recent bot comments. This should reduce risk of two computers commenting on the same post which could happen if databases are de-synced and one computer is not in quiet mode because I typed in the wrong command. Opperator Error Risk Reduction. 

 - [X] LICENSE: PRIORITY
 - Full Test Suite: PRIORITY
 - Archive Posts: PRIORITY
    Probably should be priority as well, use to draw on for the test suite. This is actually going to be moved to priority. Having a test suite to draw on is really important. Probably will be dealt with in this update or one of the quick ones after. I do have to be mindful of the write-rate, and might need to buy an externally powered usb hub, and two usb hard drives to redundantly save the database and avoid killing the SD card for the pi by overwritting to it. 

 - botMetrics.measureUserReaction(): 
 A function focused on seeing if a user did in fact go to
 r/learnpython after the bot made its suggestion. Currently built, now need to add 
 functionality in main.py to use it

 - summarizeText.loadEnglishModel(sourceDataPath=paths["prebuiltEnglishDB"]):
 Prebuild and pickle the output tdm of 
 summarizeText.buildModelFromDocsInFolder(sourceDataPath=paths["englishDB"])
 so the raspberry pi doesn't have to hit memory errors in in main.startupBot()
 load the prebuilt database and build it if the prebuild database does not exist.
 Or just build a custom compression scheme and load that instead of using pickle

 - test.EvaluatePost():
 This is going to require some restructuring of the bot in main. Take a post given a post id, then run it through the classifier where the exitpoints are turned off from the functions, forcing it to classify the post in full

 - Reply To Common posts:
 Build semi scripted replies to frequently asked questions (probably largely pulled from the sidebar, since that's how the side bar gets populated)
 This includes "How do I install python" and "Is learning python worth it?" (Aka "Why learn python?")

 - local Flask website/dashboard to monitor the status and logs of the bot in realtime

 - rpiMain.dontRunSwitchFlag(): 
 A function which polls one of the gpio pins to see if it's low (normally high) (or flipped levels). That pin will be tied to a jumper or switch. When set, the bot will not turn on at boot, allowing for simpler diagnostics, updates, etc. 

 - Continue Documentation
 - [X] Adjust log format to record the source py file, function name, and line number of the code that triggered the log. Also consider adding the version atop the log file
 - Add ram usage check and log it in every 'awake' cycle of program, to try and tease out any possible MemeoryError's kicking up after long periods of time
 - Log processing: a set of functions and visualizations to process the log files for various useful tidbits. Something nicer than grep
 - [X] formatCode.py: a module to classify each line in a post to identify blocks of code, then to reformat the code for reddit by appending 4 spaces to the start of each newline

 - A queue which has inputs added to it by functions, and removed by the raspberry pi gpio handler, allowing the bot to change LED status based on what it's doing. Similar to the twitter event bot design (sepperate project).
 


#### Change
 - [X] module folder structure. It's a mess, make it easy to work through. Each little module could use it's own readme, roadmap, and changelog. Especially the more generic and useful functions.
 - [X] main.XComment(): fix so the base comment is actually the base comment, and there's varible headers/preambles. The message as a whole is also a bit unwieldy, rework the base comment to cut it down as best as possible. Be mindful that there is also an intended "I searched stack overflow and this is what I thought might be useful" section that will be added as well.
 - [X] Move key phrases to a .txt file rather than hard coded in a function, load it into memory at startup.
 - [X] Consider restructuring the bot to be able to autoreply faster than once every 15 minutes, making the keyphrase autoreply an independent and parallel classifier
 - Move NLP functions from NLTK (used in many files) to a buffer module, allowing for simpler, universal changes to be made. For example, if there is a better POS tagger than nltk.pos_tag(sent) then we can easily switch to that. Right now NLTK is used over a fairly large filespace making adjustments of that sort difficult. 
 - Review all my logging notes. See what should be dropped, changed, etc. 
 - [X] move classifier into its own module to make it cleaner and easier to build new ones off of

#### Deprecate
 - [X] Search Stack Overflow has not been functional in ages, the code doesn't really work, and back when it did it was rarely helpful. This version will deprecate the code, but not remove it on the off chance that the SO Database project path could use portions of it. 
#### Remove
 - Broken Search Stack Overflow code. It's been deprecated, on 0.2.01 it should be completely deleted.
#### Fix
 - Standardize function name style. Either underscore or camelcase, just not both
 Probably preferable to use underscore, the despite camelcase being faster..

#### Security
#### Consider
 - all timestamps in any form as UTC. (I Believe this is the case with the exception of log file timestamps, which should not be an issue)


---

### General to Long Term Expansion


 - [X] (Completed to currently reasonable limits) module folder structure. It's a mess, make it easy to work through. Each little module could use it's own readme, roadmap, and changelog. Especially the more generic and useful functions.

 - Develop terms for a walk away condition. Either End of active development and the bot remains online, end of active development and death of bot, or end of active development and project is passed on to others. Terms will almost certainly be changed constantly and the project grows and evolves, but it's nice to have an idea of what I consider to be a "complete" project. 



### Main
 - alreadyAnswered():
 Parse through OPs comments on the thread, and search for text that implies the question
 has been answered. Adjust comment on submission accordingly, probably to say, "Next time
 you have a question like this, consider using r/learnpython" blah blah  blah 
 - Redo the main runbot while loop to envoke certain actions once every time period, allowing for variable flexibility on different tasks, Ex: classifying posts infrequently, checking for summons frequently



### Libraries:


### archiveAndUpdateReddit.py
The big set of functions necessary in this module are database creation, and update functions.
There might be two databases: one of just posts, and another comprising of posts, and comments.
The just posts database would need to include all data that the bot makes it's classification
based on on, including but not limited to
Karma Growth of post over time
Number of comments 

 - saveSubmissions(submission, database)
Given a submission, save the post, comments, and other relevant data. 

 - archiveAndRemoveOldSubmissions()
Given a set of posts, add it 


ARCHIVE FUNCTIONS
TODO: Saves it into sqlite3 table after it's passed the time threshold to "not in 
use" 

"not in use" is probably going to be defined as 8 hours. Past that point the 
post will be either 'successful', 'mild', or 'unsuccessful', defined as 
x >= 8 points, 8 > x >= 1, 1 > x 

Adjust it so 'not in use' is not defined as 8 hours, but instead defined as 
a varible, which changes based on the time of day (either defined by utc or
cdt--cdt being my current local time) that the posts was made. 'Late at night' as
defined by the time where the fewest users/ r/python 'actions' (posts, upvotes, 
comments) are made, adjusted according to the day of the week and or holiday 
(unlikely that this bot will need to be that specific) the post is made on.

Other adjustments include making a specific database entry for each submission, 
allowing for each comment to be easily integrated into the database. 
While this isn't something I need or want, it would make sense to build a general
reddit post database for future programs and open source uses.

It would also be useful to plot posts by upvotes and use the program to define
the boundary between 'successful' and 'mild' rather than have it hard coded.
Again it would require more data than I have currently, but removing a hard 
coded value would be desirable. 

 r/learnpython is another source of data: 

it will act as a source of useful questions, and will allow the bot to direct
users to other reddit based questions rather than simply stack overflow (this
distinction should help allow the bot to be generalizable) 
posts between 3 and 8 upvotes will be determined as 'basic questions' and
will be used as suggested solutions if the similarity between the new r/python
post and the old r/learpython post is greater than some threshold

Necessary Features
Post title (str)
Post Text (str)
Post URL (str)
Post ID (str)
Username (str)
Post Time (UTC timestamp)
karma by age (list of tuples: (karma_points (int or float), karma percent (float), UTC TimeStamp))
removed by mod (bool)
reason removed (str)
learn python suggested (bool)



### botHelperFunctions.py

### botMetrics.py

 - measureUserReaction(): 
to see if redditor does post to r/learnpython. The post will have to be strongly similar
to their r/python post, and be posted not long after the python sub post

- questionAndAnswer(query): to attempt to reply to semi-scripted questions

- buildConfusionMatrix(): to measure performance

#### Confusion Matrix Traits
##### True Positive: 
[The bot has commented,] And
[[Either a mod has removed the post due to 'learning'], 
Or [the redditor posts their question on r/learnpython]]

##### False Negative: 
[The bot did not comment after 8 hours] And
[[Either a mod has removed the post due to learning,] 
Or, [[someone else has commented r/learnpython] and [has greater than 2 upvotes after 8 to 24 
hours after commenting,]]
Or, [the user posted their question on r/learnpython]]

##### False Positive: 
[The bot has commented],And [has less than -1 comment karma after 8 to 24 hours,]
And [[the post is not removed due to learning within 8-24 hours] or [by mods recent 
activity plus some threshold.]]
And [[the user does not make a similar post to r/learnpython within a timespan of 8
hours] or [4 hours after their next user activity monitored for no more than a week]]

##### True Negative:
[The bot did not comment after 8 hours] And
[[No mod has removed the post using a reference to 'learning' after 8 to 24 hours] or 
by mods recent activity plus some threshold.] And
[[No commenter has post made a post which contains 'r/learnpython'] And [has more than 2 upvotes]]

##### Fuzzy:
All Else. 
This class will be either require human moderation to place into the confusion matrix, Or
will be used for other classificaiton, such as "Blog Spam"


### getChatBotKeys.py
### getPythonHelperBotKeys.py


### locateDB.py
 - load in path data from a prefernce file, and or take it as input that way the path isn't
 1. Hard coded and
 2. Hard coded in the module 
 Generic is better if it's generally useful. 

 That said, "check_though_these():" is a pretty good and simple function to move out of "locateDB.py" and into main.py


### questionIdentifier.py
It'd be nice to use stack overflow's user submissions and r/learnpython's 
submissions compared to 'successful' r/python submissions to build a 'programmers 
question' classifier (and expand the classifier to blogspammers). This would
make it generalizable so posts which are questions or requests ("HELP ME CODE") 
are directed to r/learnpython, posts which are clearly for click/ads are commented
on as such, and good posts are 'ignored': allowing redditors to act on it as they
choose. This is not an easy goal to acheive and is incredibly arbitary. but there
are still certain factors which can be measured and acted on. 

### rpiGPIOFunctions.py
### rpiManager.py
 - update the gpio naming and numbering list
 - update grab-from-github functions
 
### searchStackOverflowWeb.py
### summarizeText.py
### textSupervision.py
### updateLocalSubHistory.py
### user_agents.py

### OTHER
(This is all functions that don't have a clear parent module)

 - moqaProgram

 - ELMO program

 - reformat_User_Code():
 a function to identify python code blocks that aren't properly formated, and auto format the code
 for other reddit users. Might live it its own module.
 Currently being worked on.

 - Leverage reformat user code with automatic Q&A: Use classified code regions to match SO code regions, classified text regions to match SO text regions. Hopefully this improves the search engine and cuts the risk of added noise by a text to code block increasing precieved distance between the user query and the SO database post.
 Next If a majority of highly matching SO posts have sample code in the question, but the reddit query does not, strongly suggest adding the example code that caused the issue to the next itteration of the query.


 - question_topic_Modeling():
 This is going to take a few parts. 
   - Identify all related learning subreddits:

   - Model the topics of stack overflow questions. 

   - Model the topics in the learning subs
 Do network analysis to find the most active sub that addresses a topic: probably pagerank since it's simple and it works. It doesn't need to be state of the art, and if it can run on the pi, that's even better

   - Next take in the question, extract topics, feed the topics in the network, identify the sub that will get the best answer fastest. This means there also has to be some knowledge of the subs activity score

 - sub_Activity_Measure():
 Or score.. 
 This will probably return some arbatrary number that only makes sense in the context of other measures
 It might be a function of:
 The distance between the top 25 posts on Hot and the top 25 posts in New, where 'top' refers to 
 reddits ranking. 
 The number of comments and the absolute value of karma of those comments
 the number of unique users in those 25 posts
 The time between each activity

 Comparing the intersection of hot to new posts shows a glimps of how active the sub is without requiring the bot to look at the sub at multiple times. 

 This function would be useful with the question_topic_modeling() function and wouldn't need to run frequently. Though over multiple runs, it would have a solid understanding of how active a sub is at different times of day, which might encourage the bot to direct a user to a learning sub that is 
 active at that time. 


 - Auto Reply to common questions (Functional FAQ as it were)
  (This is probably going to be an early test of soft skills)
  * ["Possibly wanting to learn Python, is it worth it?"](https://www.reddit.com/r/Python/comments/917zxd/)

 - Use Automatic Sentence Ordering to construct the bots autoreply, reducing the mess of the code there. Should be mildly simple (ha, sure...), and allow for much more flexible commenting. Target is to have a defined intro, a 'bag of sentences' for the body, and a defined signature. The 'mildly simple' notion is built off the idea that there will be little the program can do incorrectly with that scaffolding. Look at two metrics: absolute sentence ordering, and new paragraph insertion. Maybe train on a ton of readme's, or wiki data for the new paragraph insertion. 


#### Question & Answer
Resources to draw from:
 - Stack Overflow (Primary)
 - Python Docs (Secondary)
 - Python Blog Posts (Out of Focus)
 - Scraped Github Code (Out of Focus)

Think about using a subset of highly matching SO posts code to OPs source code and using bayes in a MSAlignment fashion to guess on solution.
Most likely this is especially useful with syntax errors and stack traces. 


### Generalizing the bot: 
These are features which an ideal bot-mod would have, but which are not directly linked to a question-answer-and-redirector bot like u/pythonHelperBot (as of mid July 2018)
 - sub_Toxicisty_Score():
 Alternatively a friendly score. Bit ambigous, and doesn't immeadetly fit into the bot, but just a measure of how kind or standoffish or toxic a sub is. Certain communities tend to forget that not everyone knows everything, and it'd be nice to avoid recommending those subs.

 - blog_Spam_Flagger():
 This is actually a large but distant future goal for the bot. There's often complaints about blog spam on the python sub, and it'd be nice to have a programmatic way to define it. Even if the spammy site sees the definition, and works around it, the definition can either be altered, or the work around can be allowed. Most redditors want to see good content, so the best way around an ideal blog spam filter would be to have variable, high quality content. In which case everyone wins. Using that idea, we can start to outline the basic components of what blog spam might be. 

 High quality content is safe. High quality with respect to the python sub is probably some function of what generally does well

 Low quality can be caused by a few reasons: r/python is not the proper sub for that: ie questions
 It was recently posted: this is probably best defined as content theft, though repost is a common name for it. 

 I'm tired, I'll come back to this. 

### Tests 

## [A0.1.01] 2018-12-14

### Contributors
Keith Murray
email: kmurrayis@gmail.com
twitter: [@keithTheEE](https://twitter.com/keithTheEE)
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

### Short Term Roadmap

There will probably be an update to solidify v0.1.01, followed by a large update to move the bot to v0.2.00. Moving to v0.2.00 will signify major changes in the way praw varibles are handled, including remapping them into a custom class to reduce unexpected errors caused by either the reddit server being down, or the bot exceeding api calls. The custom class will hold a majority of the info the bot might need at any given classification level, as well as being simpler to save and repopulate from disk. This should then make more complex classifiers easier to build. Key values include whether or not the post was removed by a mod based on learning or spam, whether or not the user was suggested to 'read the sidebar' or go to r/learnpython, and the score of the commenter who made the suggestion. Other useful elements include if the bot commented, and what it's score was. These should all directly be useful with the bot confusion matrix. 

#### Add
    
 - Submission, Comment, and Users are getting a new class structure. 
    This is going to be based heavily off of networkEval's design (a sepperate bot), and should provide a number of wonderful little side effects, but will come at an API call cost. This is currently being worked on and should hit the next change log, and also bring about a large version change this next time around.
    Side effects include but are not limited to archiving posts, samples a test suite can draw from. 



 - LICENSE: PRIORITY
 - Full Test Suite: PRIORITY
 - [X] Muted run, doesn't actually comment or add usernames and postids to log, but does go through the motions. command line input to do so 
 - Archieve Posts: PRIORITY
    Probably should be priority as well, use to draw on for the test suite. This is actually going to be moved to priority. Having a test suite to draw on is really important

 - botMetrics.measureUserReaction(): 
 A function focused on seeing if a user did in fact go to
 r/learnpython after the bot made its suggestion. Currently built, now need to add 
 functionality in main.py to use it

 - summarizeText.loadEnglishModel(sourceDataPath=paths["prebuiltEnglishDB"]):
 Prebuild and pickle the output tdm of 
 summarizeText.buildModelFromDocsInFolder(sourceDataPath=paths["englishDB"])
 so the raspberry pi doesn't have to hit memory errors in in main.startupBot()
 load the prebuilt database and build it if the prebuild database does not exist

 - test.EvaluatePost():
 This is going to require some restructuring of the bot in main. Take a post given a post id, then run it through the classifier where the exitpoints are turned off from the functions, forcing it to classify the post in full

 - Reply To Common posts:
 Build semi scripted replies to frequently asked questions (probably largely pulled from the sidebar, since that's how the side bar gets populated)
 This includes "How do I install python" and "Is learning python worth it?" (Aka "Why learn python?")

 - local Flask website to monitor the status and logs of the bot in realtime


#### Change
 - module folder structure. It's a mess, make it easy to work through. Each little module could use it's own readme, roadmap, and changelog. Especially the more generic and useful functions.
 - main.XComment(): fix so the base comment is actually the base comment, and there's varible headers/preambles 
 - Move NLP functions from NLTK (used in many files) to a buffer module, allowing for simpler, universal changes to be made. For example, if there is a better POS tagger than nltk.pos_tag(sent) then we can easily switch to that. Right now NLTK is used over a fairly large filespace making adjustments of that sort difficult. 

#### Deprecate
#### Remove
#### Fix
 - Standardize function name style. Either underscore or camelcase, just not both
 Probably preferable to use underscore, the despite camelcase being faster..

#### Security
#### Consider
 - all timestamps in any form as UTC. 


---

### General to Long Term Expansion


 - module folder structure. It's a mess, make it easy to work through. Each little module could use it's own readme, roadmap, and changelog. Especially the more generic and useful functions.



### Main
 - alreadyAnswered():
 Parse through OPs comments on the thread, and search for text that implies the question
 has been answered. Adjust comment on submission accordingly, probably to say, "Next time
 you have a question like this, consider using r/learnpython" blah blah  blah 



### Libraries:


### archiveAndUpdateReddit.py
The big set of functions necessary in this module are database creation, and update functions.
There might be two databases: one of just posts, and another comprising of posts, and comments.
The just posts database would need to include all data that the bot makes it's classification
based on on, including but not limited to
Karma Growth of post over time
Number of comments 

 - saveSubmissions(submission, database)
Given a submission, save the post, comments, and other relevant data. 

 - archiveAndRemoveOldSubmissions()
Given a set of posts, add it 


ARCHIVE FUNCTIONS
TODO: Saves it into sqlite3 table after it's passed the time threshold to "not in 
use" 

"not in use" is probably going to be defined as 8 hours. Past that point the 
post will be either 'successful', 'mild', or 'unsuccessful', defined as 
x >= 8 points, 8 > x >= 1, 1 > x 

Adjust it so 'not in use' is not defined as 8 hours, but instead defined as 
a varible, which changes based on the time of day (either defined by utc or
cdt--cdt being my current local time) that the posts was made. 'Late at night' as
defined by the time where the fewest users/ r/python 'actions' (posts, upvotes, 
comments) are made, adjusted according to the day of the week and or holiday 
(unlikely that this bot will need to be that specific) the post is made on.

Other adjustments include making a specific database entry for each submission, 
allowing for each comment to be easily integrated into the database. 
While this isn't something I need or want, it would make sense to build a general
reddit post database for future programs and open source uses.

It would also be useful to plot posts by upvotes and use the program to define
the boundary between 'successful' and 'mild' rather than have it hard coded.
Again it would require more data than I have currently, but removing a hard 
coded value would be desirable. 

 r/learnpython is another source of data: 

it will act as a source of useful questions, and will allow the bot to direct
users to other reddit based questions rather than simply stack overflow (this
distinction should help allow the bot to be generalizable) 
posts between 3 and 8 upvotes will be determined as 'basic questions' and
will be used as suggested solutions if the similarity between the new r/python
post and the old r/learpython post is greater than some threshold

Necessary Features
Post title (str)
Post Text (str)
Post URL (str)
Post ID (str)
Username (str)
Post Time (UTC timestamp)
karma by age (list of tuples: (karma_points (int or float), karma percent (float), UTC TimeStamp))
removed by mod (bool)
reason removed (str)
learn python suggested (bool)



### botHelperFunctions.py

### botMetrics.py

 - measureUserReaction(): 
to see if redditor does post to r/learnpython. The post will have to be strongly similar
to their r/python post, and be posted not long 

- questionAndAnswer(query): to attempt to reply to semi-scripted questions

- buildConfusionMatrix(): to measure performance

#### Confusion Matrix Traits
##### True Positive: 
[The bot has commented,] And
[[Either a mod has removed the post due to 'learning'], 
Or [the redditor posts their question on r/learnpython]]

##### False Negative: 
[The bot did not comment after 8 hours] And
[[Either a mod has removed the post due to learning,] 
Or, [[someone else has commented r/learnpython] and [has greater than 2 upvotes after 8 to 24 
hours after commenting,]]
Or, [the user posted their question on r/learnpython]]

##### False Positive: 
[The bot has commented],And [has less than -1 comment karma after 8 to 24 hours,]
And [[the post is not removed due to learning within 8-24 hours] or [by mods recent 
activity plus some threshold.]]
And [[the user does not make a similar post to r/learnpython within a timespan of 8
hours] or [4 hours after their next user activity monitored for no more than a week]]

##### True Negative:
[The bot did not comment after 8 hours] And
[[No mod has removed the post using a reference to 'learning' after 8 to 24 hours] or 
by mods recent activity plus some threshold.] And
[[No commenter has post made a post which contains 'r/learnpython'] And [has more than 2 upvotes]]

##### Fuzzy:
All Else. 
This class will be either require human moderation to place into the confusion matrix, Or
will be used for other classificaiton, such as "Blog Spam"


### getChatBotKeys.py
### getPythonHelperBotKeys.py


### locateDB.py
 - load in path data from a prefernce file, and or take it as input that way the path isn't
 1. Hard coded and
 2. Hard coded in the module 
 Generic is better if it's generally useful. 

 That said, "check_though_these():" is a pretty good and simple function to move out of "locateDB.py" and into main.py


### questionIdentifier.py
It'd be nice to use stack overflow's user submissions and r/learnpython's 
submissions compared to 'successful' r/python submissions to build a 'programmers 
question' classifier (and expand the classifier to blogspammers). This would
make it generalizable so posts which are questions or requests ("HELP ME CODE") 
are directed to r/learnpython, posts which are clearly for click/ads are commented
on as such, and good posts are 'ignored': allowing redditors to act on it as they
choose. This is not an easy goal to acheive and is incredibly arbitary. but there
are still certain factors which can be measured and acted on. 

### rpiGPIOFunctions.py
### rpiManager.py
 - update the gpio naming and numbering list
 
### searchStackOverflowWeb.py
### summarizeText.py
### textSupervision.py
### updateLocalSubHistory.py
### user_agents.py

### OTHER
(This is all functions that don't have a clear parent module)

 - moqaProgram

 - ELMO program

 - reformat_User_Code():
 a function to identify python code blocks that aren't properly formated, and auto format the code
 for other reddit users. Might live it its own module 


 - question_topic_Modeling():
 This is going to take a few parts. 
 Identify all related learning subreddits:

 Model the topics of stack overflow questions. 

 Model the topics in the learning subs
 Do network analysis to find the most active sub that addresses a topic: probably pagerank since it's simple and it works. It doesn't need to be state of the art, and if it can run on the pi, that's even better

 Next take in the question, extract topics, feed the topics in the network, identify the sub that will get the best answer fastest. This means there also has to be some knowledge of the subs activity score

 - sub_Activity_Measure():
 Or score.. 
 This will probably return some arbatrary number that only makes sense in the context of other measures
 It might be a function of:
 The distance between the top 25 posts on Hot and the top 25 posts in New, where 'top' refers to 
 reddits ranking. 
 The number of comments and the absolute value of karma of those comments
 the number of unique users in those 25 posts
 The time between each activity

 Comparing the intersection of hot to new posts shows a glimps of how active the sub is without requiring the bot to look at the sub at multiple times. 

 This function would be useful with the question_topic_modeling() function and wouldn't need to run frequently. Though over multiple runs, it would have a solid understanding of how active a sub is at different times of day, which might encourage the bot to direct a user to a learning sub that is 
 active at that time. 


 - Auto Reply to common questions (Functional FAQ as it were)
  (This is probably going to be an early test of soft skills)
  * ["Possibly wanting to learn Python, is it worth it?"](https://www.reddit.com/r/Python/comments/917zxd/)



### Generalizing the bot: 
These are features which an ideal bot-mod would have, but which are not directly linked to a question-answer-and-redirector bot like u/pythonHelperBot (as of mid July 2018)
 - sub_Toxicisty_Score():
 Alternatively a friendly score. Bit ambigous, and doesn't immeadetly fit into the bot, but just a measure of how kind or standoffish or toxic a sub is. Certain communities tend to forget that not everyone knows everything, and it'd be nice to avoid recommending those subs.

 - blog_Spam_Flagger():
 This is actually a large but distant future goal for the bot. There's often complaints about blog spam on the python sub, and it'd be nice to have a programmatic way to define it. Even if the spammy site sees the definition, and works around it, the definition can either be altered, or the work around can be allowed. Most redditors want to see good content, so the best way around an ideal blog spam filter would be to have variable, high quality content. In which case everyone wins. Using that idea, we can start to outline the basic components of what blog spam might be. 

 High quality content is safe. High quality with respect to the python sub is probably some function of what generally does well

 Low quality can be caused by a few reasons: r/python is not the proper sub for that: ie questions
 It was recently posted: this is probably best defined as content theft, though repost is a common name for it. I prefer content theft because repost is vague of whether or not the content has been rehosted or altered. content theft falls under various plagerism defintions. 

 I'm tired, I'll come back to this. 

### Tests 

## [A0.1.00] 2018-07-30

### Contributors
Keith Murray
email: kmurrayis@gmail.com
twitter: [@keithTheEE](https://twitter.com/keithTheEE)
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

### Short Term Roadmap

#### Add
 - LICENSE: PRIORITY
 - Full Test Suite: PRIORITY
 - Archieve Posts: Probably should be priority as well, use to draw on for the test suite
 - raspberry pi associated functions to start on bootup, catch and log errors, restart program after an error, and add gpio interaction including buttons and status LEDs
 - botMetrics.measureUserReaction(): 
 A function focused on seeing if a user did in fact go to
 r/learnpython after the bot made its suggestion. Currently built, now need to add 
 functionality in main.py to use it

 - summarizeText.loadEnglishModel(sourceDataPath=paths["prebuiltEnglishDB"]):
 Prebuild and pickle the output tdm of 
 summarizeText.buildModelFromDocsInFolder(sourceDataPath=paths["englishDB"])
 so the raspberry pi doesn't have to hit memory errors in in main.startupBot()
 load the prebuilt database and build it if the prebuild database does not exist

 - test.EvaluatePost():
 This is going to require some restructuring of the bot in main. Take a post given a post id, then run it through the classifier where the exitpoints are turned off from the functions, forcing it to classify the post in full

 - Reply To Common posts
 Build semi scripted replies to frequently asked questions (probably largely pulled from the sidebar, since that's how the side bar gets populated)
 This includes "How do I install python" and "Is learning python worth it?" (Aka "Why learn python?")


#### Change
 - module folder structure. It's a mess, make it easy to work through. Each little module could use it's own readme, roadmap, and changelog. Especially the more generic and useful functions.
 - main.XComment(): fix so the base comment is actually the base comment, and there's varible headers
 - Move NLP functions from NLTK (used in many files) to a buffer module, allowing for simpler, universal changes to be made. For example, if there is a better POS tagger than nltk.pos_tag(sent) then we can easily switch to that. Right now NLTK is used over a fairly large filespace making adjustments of that sort difficult. 

#### Deprecate
#### Remove
#### Fix
 - Standardize function name style. Either underscore or camelcase, just not both
 Probably preferable to use underscore, the lesser of the two options..

#### Security
#### Consider
 - all timestamps in any form as UTC. 


---

### General to Long Term Expansion


 - module folder structure. It's a mess, make it easy to work through. Each little module could use it's own readme, roadmap, and changelog. Especially the more generic and useful functions.



### Main
 - alreadyAnswered():
 Parse through OPs comments on the thread, and search for text that implies the question
 has been answered. Adjust comment on submission accordingly, probably to say, "Next time
 you have a question like this, consider using r/learnpython" blah blah  blah 



### Libraries:


### archiveAndUpdateReddit.py
The big set of functions necessary in this module are database creation, and update functions.
There might be two databases: one of just posts, and another comprising of posts, and comments.
The just posts database would need to include all data that the bot makes it's classification
based on on, including but not limited to
Karma Growth of post over time
Number of comments 

 - saveSubmissions(submission, database)
Given a submission, save the post, comments, and other relevant data. 

 - archiveAndRemoveOldSubmissions()
Given a set of posts, add it 


TODO: Saves it into sqlite3 table after it's passed the time threshold to "not in 
use" 

"not in use" is probably going to be defined as 8 hours. Past that point the 
post will be either 'successful', 'mild', or 'unsuccessful', defined as 
x >= 8 points, 8 > x >= 1, 1 > x 

Adjust it so 'not in use' is not defined as 8 hours, but instead defined as 
a varible, which changes based on the time of day (either defined by utc or
cdt--cdt being my current local time) that the posts was made. 'Late at night' as
defined by the time where the fewest users/ r/python 'actions' (posts, upvotes, 
comments) are made, adjusted according to the day of the week and or holiday 
(unlikely that this bot will need to be that specific) the post is made on.

Other adjustments include making a specific database entry for each submission, 
allowing for each comment to be easily integrated into the database. 
While this isn't something I need or want, it would make sense to build a general
reddit post database for future programs and open source uses.

It would also be useful to plot posts by upvotes and use the program to define
the boundary between 'successful' and 'mild' rather than have it hard coded.
Again it would require more data than I have currently, but removing a hard 
coded value would be desirable. 

 r/learnpython is another source of data: 

it will act as a source of useful questions, and will allow the bot to direct
users to other reddit based questions rather than simply stack overflow (this
distinction should help allow the bot to be generalizable) 
posts between 3 and 8 upvotes will be determined as 'basic questions' and
will be used as suggested solutions if the similarity between the new r/python
post and the old r/learpython post is greater than some threshold

### botHelperFunctions.py

### botMetrics.py

 - measureUserReaction(): 
to see if redditor does post to r/learnpython. The post will have to be strongly similar
to their r/python post, and be posted not long 

- questionAndAnswer(query): to attempt to reply to semi-scripted questions

- buildConfusionMatrix(): to measure performance

#### Confusion Matrix Traits
##### True Positive: 
[The bot has commented,] And
[[Either a mod has removed the post due to 'learning'], 
Or [the redditor posts their question on r/learnpython]]

##### False Negative: 
[The bot did not comment after 8 hours] And
[[Either a mod has removed the post due to learning,] 
Or, [[someone else has commented r/learnpython] and [has greater than 2 upvotes after 8 to 24 
hours after commenting,]]
Or, [the user posted their question on r/learnpython]]

##### False Positive: 
[The bot has commented],And [has less than -1 comment karma after 8 to 24 hours,]
And [[the post is not removed due to learning within 8-24 hours] or [by mods recent 
activity plus some threshold.]]
And [[the user does not make a similar post to r/learnpython within a timespan of 8
hours] or [4 hours after their next user activity monitored for no more than a week]]

##### True Negative:
[The bot did not comment after 8 hours] And
[[No mod has removed the post using a reference to 'learning' after 8 to 24 hours] or 
by mods recent activity plus some threshold.] And
[[No commenter has post made a post which contains 'r/learnpython'] And [has more than 2 upvotes]]

##### Fuzzy:
All Else. 
This class will be either require human moderation to place into the confusion matrix, Or
will be used for other classificaiton, such as "Blog Spam"


### getChatBotKeys.py
### getPythonHelperBotKeys.py


### locateDB.py
 - load in path data from a prefernce file, and or take it as input that way the path isn't
 1. Hard coded and
 2. Hard coded in the module 
 Generic is better if it's generally useful. 

 That said, "check_though_these():" is a pretty good and simple function to move out of "locateDB.py" and into main.py


### questionIdentifier.py
It'd be nice to use stack overflow's user submissions and r/learnpython's 
submissions compared to 'successful' r/python submissions to build a 'programmers 
question' classifier (and expand the classifier to blogspammers). This would
make it generalizable so posts which are questions or requests ("HELP ME CODE") 
are directed to r/learnpython, posts which are clearly for click/ads are commented
on as such, and good posts are 'ignored': allowing redditors to act on it as they
choose. This is not an easy goal to acheive and is incredibly arbitary. but there
are still certain factors which can be measured and acted on. 

### rpiGPIOFunctions.py
### rpiManager.py
 - update the gpio naming and numbering list
 
### searchStackOverflowWeb.py
### summarizeText.py
### textSupervision.py
### updateLocalSubHistory.py
### user_agents.py

### OTHER
(This is all functions that don't have a clear parent module)

 - moqaProgram

 - ELMO program

 - reformat_User_Code():
 a function to identify python code blocks that aren't properly formated, and auto format the code
 for other reddit users. Might live it its own module 


 - question_topic_Modeling():
 This is going to take a few parts. 
 Identify all related learning subreddits:

 Model the topics of stack overflow questions. 

 Model the topics in the learning subs
 Do network analysis to find the most active sub that addresses a topic: probably pagerank since it's simple and it works. It doesn't need to be state of the art, and if it can run on the pi, that's even better

 Next take in the question, extract topics, feed the topics in the network, identify the sub that will get the best answer fastest. This means there also has to be some knowledge of the subs activity score

 - sub_Activity_Measure():
 Or score.. 
 This will probably return some arbatrary number that only makes sense in the context of other measures
 It might be a function of:
 The distance between the top 25 posts on Hot and the top 25 posts in New, where 'top' refers to 
 reddits ranking. 
 The number of comments and the absolute value of karma of those comments
 the number of unique users in those 25 posts
 The time between each activity

 Comparing the intersection of hot to new posts shows a glimps of how active the sub is without requiring the bot to look at the sub at multiple times. 

 This function would be useful with the question_topic_modeling() function and wouldn't need to run frequently. Though over multiple runs, it would have a solid understanding of how active a sub is at different times of day, which might encourage the bot to direct a user to a learning sub that is 
 active at that time. 


 - Auto Reply to common questions (Functional FAQ as it were)
  (This is probably going to be an early test of soft skills)
  * ["Possibly wanting to learn Python, is it worth it?"](https://www.reddit.com/r/Python/comments/917zxd/)



### Generalizing the bot: 
These are features which an ideal bot-mod would have, but which are not directly linked to a question-answer-and-redirector bot like u/pythonHelperBot (as of mid July 2018)
 - sub_Toxicisty_Score():
 Alternatively a friendly score. Bit ambigous, and doesn't immeadetly fit into the bot, but just a measure of how kind or standoffish or toxic a sub is. Certain communities tend to forget that not everyone knows everything, and it'd be nice to avoid recommending those subs.

 - blog_Spam_Flagger():
 This is actually a large but distant future goal for the bot. There's often complaints about blog spam on the python sub, and it'd be nice to have a programmatic way to define it. Even if the spammy site sees the definition, and works around it, the definition can either be altered, or the work around can be allowed. Most redditors want to see good content, so the best way around an ideal blog spam filter would be to have variable, high quality content. In which case everyone wins. Using that idea, we can start to outline the basic components of what blog spam might be. 

 High quality content is safe. High quality with respect to the python sub is probably some function of what generally does well

 Low quality can be caused by a few reasons: r/python is not the proper sub for that: ie questions
 It was recently posted: this is probably best defined as content theft, though repost is a common name for it. I prefer content theft because repost is vague of whether or not the content has been rehosted or altered. content theft falls under various plagerism defintions. 

 I'm tired, I'll come back to this. 

### Tests 

## [A0.0.06] 2018-07-22

### Contributors
Keith Murray
email: kmurrayis@gmail.com
twitter: [@keithTheEE](https://twitter.com/keithTheEE)
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

### Short Term Roadmap

#### Add
 - LICENSE: PRIORITY
 - Full Test Suite: PRIORITY
 - Archieve Posts: Probably should be priority as well, use to draw on for the test suite
 - raspberry pi associated functions to start on bootup, catch and log errors, restart program after an error, and add gpio interaction including buttons and status LEDs
 - botMetrics.measureUserReaction(): 
 A function focused on seeing if a user did in fact go to
 r/learnpython after the bot made its suggestion. Currently built, now need to add 
 functionality in main.py to use it

 - summarizeText.loadEnglishModel(sourceDataPath=paths["prebuiltEnglishDB"]):
 Prebuild and pickle the output tdm of 
 summarizeText.buildModelFromDocsInFolder(sourceDataPath=paths["englishDB"])
 so the raspberry pi doesn't have to hit memory errors in in main.startupBot()
 load the prebuilt database and build it if the prebuild database does not exist

 - test.EvaluatePost():
 This is going to require some restructuring of the bot in main. Take a post given a post id, then run it through the classifier where the exitpoints are turned off from the functions, forcing it to classify the post in full

 - Reply To Common posts
 Build semi scripted replies to frequently asked questions (probably largely pulled from the sidebar, since that's how the side bar gets populated)
 This includes "How do I install python" and "Is learning python worth it?" (Aka "Why learn python?")


#### Change
 - module folder structure. It's a mess, make it easy to work through. Each little module could use it's own readme, roadmap, and changelog. Especially the more generic and useful functions.
 - main.XComment(): fix so the base comment is actually the base comment, and there's varible headers

#### Deprecate
#### Remove
#### Fix
 - Standardize function name style. Either underscore or camelcase, just not both
 Probably preferable to use underscore, the lesser of the two options..

#### Security
#### Consider
 - all timestamps in any form as UTC. 


---

### General to Long Term Expansion


 - module folder structure. It's a mess, make it easy to work through. Each little module could use it's own readme, roadmap, and changelog. Especially the more generic and useful functions.



### Main
 - alreadyAnswered():
 Parse through OPs comments on the thread, and search for text that implies the question
 has been answered. Adjust comment on submission accordingly, probably to say, "Next time
 you have a question like this, consider using r/learnpython" blah blah  blah 



### Libraries:


### archiveAndUpdateReddit.py
The big set of functions necessary in this module are database creation, and update functions.
There might be two databases: one of just posts, and another comprising of posts, and comments.
The just posts database would need to include all data that the bot makes it's classification
based on on, including but not limited to
Karma Growth of post over time
Number of comments 

 - saveSubmissions(submission, database)
Given a submission, save the post, comments, and other relevant data. 

 - archiveAndRemoveOldSubmissions()
Given a set of posts, add it 


TODO: Saves it into sqlite3 table after it's passed the time threshold to "not in 
use" 

"not in use" is probably going to be defined as 8 hours. Past that point the 
post will be either 'successful', 'mild', or 'unsuccessful', defined as 
x >= 8 points, 8 > x >= 1, 1 > x 

Adjust it so 'not in use' is not defined as 8 hours, but instead defined as 
a varible, which changes based on the time of day (either defined by utc or
cdt--cdt being my current local time) that the posts was made. 'Late at night' as
defined by the time where the fewest users/ r/python 'actions' (posts, upvotes, 
comments) are made, adjusted according to the day of the week and or holiday 
(unlikely that this bot will need to be that specific) the post is made on.

Other adjustments include making a specific database entry for each submission, 
allowing for each comment to be easily integrated into the database. 
While this isn't something I need or want, it would make sense to build a general
reddit post database for future programs and open source uses.

It would also be useful to plot posts by upvotes and use the program to define
the boundary between 'successful' and 'mild' rather than have it hard coded.
Again it would require more data than I have currently, but removing a hard 
coded value would be desirable. 

 r/learnpython is another source of data: 

it will act as a source of useful questions, and will allow the bot to direct
users to other reddit based questions rather than simply stack overflow (this
distinction should help allow the bot to be generalizable) 
posts between 3 and 8 upvotes will be determined as 'basic questions' and
will be used as suggested solutions if the similarity between the new r/python
post and the old r/learpython post is greater than some threshold

### botHelperFunctions.py

### botMetrics.py

 - measureUserReaction(): 
to see if redditor does post to r/learnpython. The post will have to be strongly similar
to their r/python post, and be posted not long 

- questionAndAnswer(query): to attempt to reply to semi-scripted questions

- buildConfusionMatrix(): to measure performance

#### Confusion Matrix Traits
##### True Positive: 
[The bot has commented,] And
[[Either a mod has removed the post due to 'learning'], 
Or [the redditor posts their question on r/learnpython]]

##### False Negative: 
[The bot did not comment after 8 hours] And
[[Either a mod has removed the post due to learning,] 
Or, [[someone else has commented r/learnpython] and [has greater than 2 upvotes after 8 to 24 
hours after commenting,]]
Or, [the user posted their question on r/learnpython]]

##### False Positive: 
[The bot has commented],And [has less than -1 comment karma after 8 to 24 hours,]
And [[the post is not removed due to learning within 8-24 hours] or [by mods recent 
activity plus some threshold.]]
And [[the user does not make a similar post to r/learnpython within a timespan of 8
hours] or [4 hours after their next user activity monitored for no more than a week]]

##### True Negative:
[The bot did not comment after 8 hours] And
[[No mod has removed the post using a reference to 'learning' after 8 to 24 hours] or 
by mods recent activity plus some threshold.] And
[[No commenter has post made a post which contains 'r/learnpython'] And [has more than 2 upvotes]]

##### Fuzzy:
All Else. 
This class will be either require human moderation to place into the confusion matrix, Or
will be used for other classificaiton, such as "Blog Spam"


### getChatBotKeys.py
### getPythonHelperBotKeys.py


### locateDB.py
 - load in path data from a prefernce file, and or take it as input that way the path isn't
 1. Hard coded and
 2. Hard coded in the module 
 Generic is better if it's generally useful. 

 That said, "check_though_these():" is a pretty good and simple function to move out of "locateDB.py" and into main.py


### questionIdentifier.py
It'd be nice to use stack overflow's user submissions and r/learnpython's 
submissions compared to 'successful' r/python submissions to build a 'programmers 
question' classifier (and expand the classifier to blogspammers). This would
make it generalizable so posts which are questions or requests ("HELP ME CODE") 
are directed to r/learnpython, posts which are clearly for click/ads are commented
on as such, and good posts are 'ignored': allowing redditors to act on it as they
choose. This is not an easy goal to acheive and is incredibly arbitary. but there
are still certain factors which can be measured and acted on. 

### rpiGPIOFunctions.py
### rpiManager.py
 - update the gpio naming and numbering list
 
### searchStackOverflowWeb.py
### summarizeText.py
### textSupervision.py
### updateLocalSubHistory.py
### user_agents.py

### OTHER
(This is all functions that don't have a clear parent module)

 - moqaProgram

 - ELMO program

 - reformat_User_Code():
 a function to identify python code blocks that aren't properly formated, and auto format the code
 for other reddit users. Might live it its own module 


 - question_topic_Modeling():
 This is going to take a few parts. 
 Identify all related learning subreddits:

 /r/cs career questions * FIND THIS SUB *
 
 Model the topics of stack overflow questions. 

 Model the topics in the learning subs
 Do network analysis to find the most active sub that addresses a topic: probably pagerank since it's simple and it works. It doesn't need to be state of the art, and if it can run on the pi, that's even better

 Next take in the question, extract topics, feed the topics in the network, identify the sub that will get the best answer fastest. This means there also has to be some knowledge of the subs activity score

 - sub_Activity_Measure():
 Or score.. 
 This will probably return some arbatrary number that only makes sense in the context of other measures
 It might be a function of:
 The distance between the top 25 posts on Hot and the top 25 posts in New, where 'top' refers to 
 reddits ranking. 
 The number of comments and the absolute value of karma of those comments
 the number of unique users in those 25 posts
 The time between each activity

 Comparing the intersection of hot to new posts shows a glimps of how active the sub is without requiring the bot to look at the sub at multiple times. 

 This function would be useful with the question_topic_modeling() function and wouldn't need to run frequently. Though over multiple runs, it would have a solid understanding of how active a sub is at different times of day, which might encourage the bot to direct a user to a learning sub that is 
 active at that time. 


 - Auto Reply to common questions (Functional FAQ as it were)
  (This is probably going to be an early test of soft skills)
  * ["Possibly wanting to learn Python, is it worth it?"](https://www.reddit.com/r/Python/comments/917zxd/)



### Generalizing the bot: 
These are features which an ideal bot-mod would have, but which are not directly linked to a question-answer-and-redirector bot like u/pythonHelperBot (as of mid July 2018)
 - sub_Toxicisty_Score():
 Alternatively a friendly score. Bit ambigous, and doesn't immeadetly fit into the bot, but just a measure of how kind or standoffish or toxic a sub is. Certain communities tend to forget that not everyone knows everything, and it'd be nice to avoid recommending those subs.

 - blog_Spam_Flagger():
 This is actually a large but distant future goal for the bot. There's often complaints about blog spam on the python sub, and it'd be nice to have a programmatic way to define it. Even if the spammy site sees the definition, and works around it, the definition can either be altered, or the work around can be allowed. Most redditors want to see good content, so the best way around an ideal blog spam filter would be to have variable, high quality content. In which case everyone wins. Using that idea, we can start to outline the basic components of what blog spam might be. 

 High quality content is safe. High quality with respect to the python sub is probably some function of what generally does well

 Low quality can be caused by a few reasons: r/python is not the proper sub for that: ie questions
 It was recently posted: this is probably best defined as content theft, though repost is a common name for it. I prefer content theft because repost is vague of whether or not the content has been rehosted or altered. content theft falls under various plagerism defintions. 

 I'm tired, I'll come back to this. 

### Tests 


## [A0.0.05] 2018-07-16

### Contributors
Keith Murray
email: kmurrayis@gmail.com
twitter: [@keithTheEE](https://twitter.com/keithTheEE)
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

### Short Term Roadmap

#### Add
 - botMetrics.measureUserReaction(): 
A function focused on seeing if a user did in fact go to
r/learnpython after the bot made its suggestion.

- summarizeText.loadEnglishModel(sourceDataPath=paths["prebuiltEnglishDB"]):
Prebuild and pickle the output tdm of 
summarizeText.buildModelFromDocsInFolder(sourceDataPath=paths["englishDB"])
so the raspberry pi doesn't have to hit memory errors in in main.startupBot()
load the prebuilt database and build it if the prebuild database does not exist

 - summarizeText.stripURL():
remove the url present in any given string. Evaluate ways to replace the url 
with some other placeholder

 - main.basicUserClassify() and main.getSubsUsersInteractedIn()

 - test.EvaluatePost():
 This is going to require some restructuring of the bot in main. Take care of 


#### Change
#### Deprecate
#### Remove
#### Fix
 - Standardize function name style. Either underscore or camelcase, just not both
 Probably preferable to use underscore, the lesser of the two options..

#### Security


---

### General to Long Term Expansion


 - module folder structure. It's a mess, make it easy to work through. Each little module could use it's own readme, roadmap, and changelog. Especially the more generic and useful functions. On this note it might be a good idea to dump them into a utils folder, and call them from there. 



### Main
 - alreadyAnswered():
 Parse through OPs comments on the thread, and search for text that implies the question
 has been answered. Adjust comment on submission accordingly, probably to say, "Next time
 you have a question like, consider using r/learnpython" blah blah  blah 

  - basicUserClassify() and getSubsUsersInteractedIn():
  Adjust the 'posted in learnpython' function to identify when the most recent learnpython post was made.
  In getSubsUsersInteractedIn: adjust it so it returns the most recent timestamp of each sub interacted in. this should help 


### Libraries:


### archiveAndUpdateReddit.py
The big set of functions necessary in this module are database creation, and update functions.
There might be two databases: one of just posts, and another comprising of posts, and comments.
The just posts database would need to include all data that the bot makes it's classification
based on on, including but not limited to
Karma Growth of post over time
Number of comments 

 - saveSubmissions(submission, database)
Given a submission, save the post, comments, and other relevant data. 

 - archiveAndRemoveOldSubmissions()
Given a set of posts, add it 


TODO: Saves it into sqlite3 table after it's passed the time threshold to "not in 
use" 

"not in use" is probably going to be defined as 8 hours. Past that point the 
post will be either 'successful', 'mild', or 'unsuccessful', defined as 
x >= 8 points, 8 > x >= 1, 1 > x 

Adjust it so 'not in use' is not defined as 8 hours, but instead defined as 
a varible, which changes based on the time of day (either defined by utc or
cdt--cdt being my current local time) that the posts was made. 'Late at night' as
defined by the time where the fewest users/ r/python 'actions' (posts, upvotes, 
comments) are made, adjusted according to the day of the week and or holiday 
(unlikely that this bot will need to be that specific) the post is made on.

Other adjustments include making a specific database entry for each submission, 
allowing for each comment to be easily integrated into the database. 
While this isn't something I need or want, it would make sense to build a general
reddit post database for future programs and open source uses.

It would also be useful to plot posts by upvotes and use the program to define
the boundary between 'successful' and 'mild' rather than have it hard coded.
Again it would require more data than I have currently, but removing a hard 
coded value would be desirable. 

 r/learnpython is another source of data: 

it will act as a source of useful questions, and will allow the bot to direct
users to other reddit based questions rather than simply stack overflow (this
distinction should help allow the bot to be generalizable) 
posts between 3 and 8 upvotes will be determined as 'basic questions' and
will be used as suggested solutions if the similarity between the new r/python
post and the old r/learpython post is greater than some threshold

### botMetrics.py

 - measureUserReaction(): 
to see if redditor does post to r/learnpython. The post will have to be strongly similar
to their r/python post, and be posted not long 

- questionAndAnswer(query): to attempt to reply to semi-scripted questions

- buildConfusionMatrix(): to measure performance

#### Confusion Matrix Traits
##### True Positive: 
The bot has commented, And
Either a mod has removed the post due to 'learning', 
Or the redditor posts their question on r/learnpython

##### False Negative: 
The bot did not comment after 8 hours And
Either a mod has removed the post due to learning, 
Or, someone else has commented r/learnpython and has greater than 2 upvotes after 8 to 24 
hours after commenting, 
Or, the user posted their question on r/learnpython

##### False Positive: 
The bot has commented, has less than -1 comment karma after 8 to 24 hours,
And the post is not removed due to learning within 8-24 hours or by mods recent 
activity plus some threshold. 
And the user does not make a similar post to r/learnpython within a timespan of 8
hours or 4 hours after their next user activity monitored for no more than a week

##### True Negative:
The bot did not comment after 8 hours And
No mod has removed the post using a reference to 'learning' after 8 to 24 hours or 
by mods recent activity plus some threshold. And
No commenter has post made a post which contains 'r/learnpython' And has more than 2 upvotes

##### Fuzzy:
All Else. 
This class will be either require human moderation to place into the confusion matrix, Or
will be used for other classificaiton, such as "Blog Spam


### getChatBotKeys.py
### getPythonHelperBotKeys.py


### locateDB.py
 - load in path data from a prefernce file, and or take it as input that way the path isn't
 1. Hard coded and
 2. Hard coded in the module 
 Generic is better if it's generally useful. 

 That said, "check_though_these():" is a pretty good and simple function to move out of "locateDB.py" and into main.py


### questionIdentifier.py
It'd be nice to use stack overflow's user submissions and r/learnpython's 
submissions compared to 'successful' r/python submissions to build a 'programmers 
question' classifier (and expand the classifier to blogspammers). This would
make it generalizable so posts which are questions or requests ("HELP ME CODE") 
are directed to r/learnpython, posts which are clearly for click/ads are commented
on as such, and good posts are 'ignored': allowing redditors to act on it as they
choose. This is not an easy goal to acheive and is incredibly arbitary. but there
are still certain factors which can be measured and acted on. 

### searchStackOverflowWeb.py
### summarizeText.py
### textSupervision.py
### updateLocalSubHistory.py
### user_agents.py

### OTHER
(This is all functions that don't have a clear parent module)

 - moqaProgrammer

 - reformat_User_Code():
 a function to identify python code blocks that aren't properly formated, and auto format the code
 for other reddit users. Might live it its own module 


 - question_topic_Modeling():
 This is going to take a few parts. 
 Identify all related learning subreddits:

 /r/cs career questions * FIND THIS SUB *
 
 Model the topics of stack overflow questions. 

 Model the topics in the learning subs
 Do network analysis to find the most active sub that addresses a topic: probably pagerank since it's simple and it works. It doesn't need to be state of the art, and if it can run on the pi, that's even better

 Next take in the question, extract topics, feed the topics in the network, identify the sub that will get the best answer fastest. This means there also has to be some knowledge of the subs activity score

 - sub_Activity_Measure():
 Or score.. 
 This will probably return some arbatrary number that only makes sense in the context of other measures
 It might be a function of:
 The distance between the top 25 posts on Hot and the top 25 posts in New, where 'top' refers to 
 reddits ranking. 
 The number of comments and the absolute value of karma of those comments
 the number of unique users in those 25 posts
 The time between each activity

 Comparing the intersection of hot to new posts shows a glimps of how active the sub is without requiring the bot to look at the sub at multiple times. 

 This function would be useful with the question_topic_modeling() function and wouldn't need to run frequently. Though over multiple runs, it would have a solid understanding of how active a sub is at different times of day, which might encourage the bot to direct a user to a learning sub that is 
 active at that time. 



### Generalizing the bot: 
These are features which an ideal bot-mod would have, but which are not directly linked to a question-answer-and-redirector bot like u/pythonHelperBot (as of mid July 2018)
 - sub_Toxicisty_Score():
 Alternatively a friendly score. Bit ambigous, and doesn't immeadetly fit into the bot, but just a measure of how kind or standoffish or toxic a sub is. Certain communities tend to forget that not everyone knows everything, and it'd be nice to avoid recommending those subs.

 - blog_Spam_Flagger():
 This is actually a large but distant future goal for the bot. There's often complaints about blog spam on the python sub, and it'd be nice to have a programmatic way to define it. Even if the spammy site sees the definition, and works around it, the definition can either be altered, or the work around can be allowed. Most redditors want to see good content, so the best way around an ideal blog spam filter would be to have variable, high quality content. In which case everyone wins. Using that idea, we can start to outline the basic components of what blog spam might be. 

 High quality content is safe. High quality with respect to the python sub is probably some function of what generally does well

 Low quality can be caused by a few reasons: r/python is not the proper sub for that: ie questions
 It was recently posted: this is probably best defined as content theft, though repost is a common name for it. I prefer content theft because repost is vague of whether or not the content has been rehosted or altered. content theft falls under various plagerism defintions. 

 I'm tired, I'll come back to this. 

### Tests 
