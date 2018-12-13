
# Reddit Helper Bot: Version Pre Alpha A0.1.01
pythonHelperBot is a reddit bot built to analyze r/python post and determine if 
they're better suited for the r/learnpython sub. 
If they are it suggests that the user post to that sub rather than to r/python.

## What is it doing? 


The bot currently runs on a simple algorithm.
In short, it waits a bit then looks to see if the post is performing poorly and if the post is asking a question.
If those two basic conditions are met, it'll probably comment. 

A bit more in depth, it'll read the title of the post, if there's a keyphrase present, build a helpful comment. 
If not, then wait a while.
If a post is scoring poorly after a bit, check to see if there's a question in either
the title or the body of the submission. 
If the submission body is a url that is not the same as the url you'd get if you selected the comments on the thread, (ie if the submission is a 'link post') then the post is ignored.
If not, then the post is a 'self post'.
In that case scan the text of the title and the body, and break it into sentences. 
After that, classify each sentence and see if a question is being asked. 
If there's a question, the bot will probably comment. 
But first it'll look through the top level comments to see if there's already someone else who mentioned r/learnpython. 
If it's been mentioned it'll acknowledge that, and adjust its comment to focus on formatting the users question acording to the subreddit's rules. (Though if it was mentioned and the OP has already taken the advice, the bot will not comment.)
If no one has suggested r/learnpython, it'll suggest the subreddit, say why it's useful, and emphasize following the subreddit rules. 


## Where are the bot in its development?
The bot is currently in a pre alpha stage. This means that the founding goals of the bot have not been met. Once they have been, the bot will enter alpha, where the simple classifier that is currently being used can be compared to more complex classifiers. 
#### Pre Alpha Goals:
 - [X] Simply comment on redditors posts who look like they should post in r/learnpython
 - [X] Run on the raspberry pi
 - Archive reddit posts for future classification evaluation
 - Use Stack Overflow to gauge the simplicity of a redditors question
 - Use Stack Overflow to implement a naive Question and Answer system

### Questions and Question and Answer Databases
Not all are used, but they're a good starting point

https://archive.org/details/stackexchange
https://trec.nist.gov/data/qamain.html
http://www.cs.cmu.edu/~ark/QA-data/
https://webscope.sandbox.yahoo.com/catalog.php?datatype=l
https://stackoverflow.blog/2009/06/04/stack-overflow-creative-commons-data-dump/
https://rajpurkar.github.io/SQuAD-explorer/
https://github.com/deepmind/rc-data
http://jmcauley.ucsd.edu/data/amazon/qa/


##### Q&A Database found through
https://www.quora.com/Datasets-How-can-I-get-corpus-of-a-question-answering-website-like-Quora-or-Yahoo-Answers-or-Stack-Overflow-for-analyzing-answer-quality
https://machinelearningmastery.com/datasets-natural-language-processing/



### Ethics
Spam is one of the most annoying things on reddit, and a primary goal of this bot is to not contribute to more spam. 
This bot is intended to make a healthy recommendation that the user go to the appropriate sub to ask their question. 

Therefore, this bot should not be spammy. 

This is enforced by never allowing the bot to suggest r/learnpython to a user more than once, as it is assumed that after that point the user should be aware of the sub. 
This assumption is known to be invalid because I've been on the internet before, and [people really are just the worst](https://www.youtube.com/watch?v=m0KFY6o6unw) ([further](https://www.youtube.com/watch?v=fZv_TARX3lI)). 

Unless a key phrase is used in the title of the post, the bot is not allowed to comment on a post until a certain amount of time has passed, which allows votes to be added to the feature vector as a secondary classification step. 

The bot is not currently allowed to remove a comment after it's clearly made a mistake. This is typically defined as having a comment score of less than -3 and the post having a karma score of greater than 1

### Author Notes
This bot is powered by coffee and the WestWorld Soundtrack. 

