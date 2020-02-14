
# Reddit Helper Bot: Version Pre Alpha A0.4.00
pythonHelperBot is a reddit bot built to analyze r/python post and determine if 
they're better suited for the r/learnpython sub. 
If they are it suggests that the user post to that sub rather than to r/python.

- [FAQ](https://github.com/CrakeNotSnowman/redditPythonHelper/blob/master/FAQ.md)

The current incarnation of the bot is aimed at encouraging the use of the r/learnpython sub.
It may flag all learning posts, but it only comments if it (in a naive way) determines that the user does not know about or chooses not to use the learning sub.

## What is it doing? 


The bot currently runs on a simple algorithm.
In short, it waits a bit then looks to see if the post is performing poorly and if the post is asking a question.
If those two basic conditions are met, it'll probably comment. 

 A bit more in depth,
 -  it'll read the title of the post, if there's a keyphrase present, build a helpful comment. 
 - It'll read the flair of the post, and if in the first two hours the post is flaired as 'Help', it'll comment. 
 - If not, then wait a while.
 - If a post is scoring poorly after a bit, check to see if there's a question in either the title or the body of the submission. 
 - If the submission body is a url that is not the same as the url you'd get if you selected the comments on the thread, (ie if the submission is a 'link post') then the post is ignored. If not, then the post is a 'self post'.
 - In that case scan the text of the title and the body, and break it into sentences. 
 - After that, classify each sentence and see if a question is being asked. 
 - If there's a question, the bot will probably comment. 
But first it'll look through the top level comments to see if there's already someone else who mentioned r/learnpython. 
 - If it's been mentioned it'll acknowledge that, and adjust its comment to focus on formatting the users question according to the subreddit's rules. (Though if it was mentioned and the OP has already taken the advice, the bot will not comment.)
 - If no one has suggested r/learnpython, it'll suggest the subreddit, say why it's useful, and emphasize following the subreddit rules. 

 
## Summoning The Bot
While the bot can be summoned for some small tasks, it really isn't a feature that is being used nor is it a feature that I feel offers much to the end user.

### Commands:
 - `/u/pythonHelperBot !reformat`
 - `/u/pythonHelperBot !format_howto` (not yet active)

### `/u/pythonHelperBot !reformat`
The bot can be summomed to reformat text blocks that have code in them. To summon the bot, simply type `/u/pythonHelperBot !reformat` as a comment below the post/comment you want to see reformatted. The bot will reply to your comment with a reformated version of the parent text if it thinks a change can be made. There are some edge cases the bot misses, but it can help users autoformat their comments if the user wasn't aware of reddit formatting. 

The bot is only allowed to make three reformatting comments on the same submission (be they on the submission itself which is only allowed once, or on comments on the thread). After that, it ignores summons. This hopefully will reduce the chance of summoning loops with other bots or overuse with specific users.


#### `/u/pythonHelperBot !format_howto`
Currently inactive.

The bot can also be summoned to display a helpful message about how to format code for reddit. This message will appear below the summoning comment, and tag the part post/comment in its message. Because of this, it tags a user unprompted, it's only allowed to interact with that user once, unless the summoner and parent post/comment are by the same user. 



## Where is the bot in its development?
The bot is currently in a pre alpha stage. This means that the founding goals of the bot have not been met. Once they have been, the bot will enter alpha, where the simple classifier that is currently being used can act as a performance baseline and be compared to more complex classifiers. Hopefully a better classifier will improve accuracy and response time a measurable amount.



#### Pre Alpha Goals:
 - [X] Simply comment on redditors posts who look like they should post in r/learnpython
 - [X] Run on the raspberry pi
 - [X] Archive reddit posts for future classification evaluation
 - Build a reddit post classifier using the archive and LDA
 - Build a local Stack Overflow Search Engine
 - Use Stack Overflow to gauge the simplicity of a redditors question
 - Use Stack Overflow to implement a naive Question and Answer system


## Other Aspects


 ### Interesting Research Areas this Bot Explores
 - Various Tiers of Classification
 - Automatic Answering in Question and Answer scenarios
 - Text Summarization 
 - Key Word Extraction
 - Sentence Ordering
 - Compound Sentence Generation 


### License
PythonHelperBot is open source [licensed under the MIT License](https://github.com/CrakeNotSnowman/redditPythonHelper/blob/master/LICENSE)

### Questions and Question and Answer Databases
Not all are used, but they're a good starting point

 - https://archive.org/details/stackexchange
 - https://trec.nist.gov/data/qamain.html
 - http://www.cs.cmu.edu/~ark/QA-data/
 - https://webscope.sandbox.yahoo.com/catalog.php?datatype=l
 - https://stackoverflow.blog/2009/06/04/stack-overflow-creative-commons-data-dump/
 - https://rajpurkar.github.io/SQuAD-explorer/
 - https://github.com/deepmind/rc-data
 - http://jmcauley.ucsd.edu/data/amazon/qa/


##### Q&A Database found through
 - https://www.quora.com/Datasets-How-can-I-get-corpus-of-a-question-answering-website-like-Quora-or-Yahoo-Answers-or-Stack-Overflow-for-analyzing-answer-quality
 - https://machinelearningmastery.com/datasets-natural-language-processing/



### Ethics
Spam is one of the most annoying things on reddit, and a primary goal of this bot is to not contribute to more spam. 
This bot is intended to make a healthy recommendation that the user go to the appropriate sub to ask their question. 

Therefore, this bot should not be spammy. 

This is enforced by almost never allowing the bot to suggest r/learnpython to a user more than once, as it is assumed that after that point the user should be aware of the sub. 
This assumption is known to be invalid because I've been on the internet before, and [people really are just the worst](https://www.youtube.com/watch?v=m0KFY6o6unw) ([further](https://www.youtube.com/watch?v=fZv_TARX3lI)). The currently allowed exception to this is if they flair their submission as 'Help', as that is a self applied classification and the bot can be confident in it's actions.

Unless a key phrase is used in the title of the post, or the post has 'Help' flair, the bot is not allowed to comment on a post until a certain amount of time has passed, which allows votes to be added to the feature vector as a secondary classification step. 

The bot is not currently allowed to remove a comment after it's clearly made a mistake. This is typically defined as having a comment score of less than -3 and the post having a karma score of greater than 1

### Author Notes
This bot is powered by coffee and the WestWorld Soundtrack. 

If you're able, take some time to watch something amazing and beautiful: [the ISS live stream of Earth](https://eol.jsc.nasa.gov/ESRS/HDEV/). The Earth is pretty cool. 