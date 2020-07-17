
# FREQUENTLY ASKED QUESTIONS

Granted, these are just questions I anticipate. Since no one has seen the source code, 'frequently' in Frequently Asked Questions is a bit of a joke. Every possible questions is as legitimate as any other possible question with respect to which questions have been frequently asked. Hopefully this document reflects this status accordingly.


#### How does the bot decide to comment?
The bot currently runs on a simple algorithm.
In short, it waits a bit then looks to see if the post is performing poorly and if the post is asking a question.
If those two basic conditions are met, it'll probably comment. 


 A bit more in depth,
 - It'll read the title of the post, if there's a keyphrase present, build a helpful comment. 
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



#### Why didn't the bot comment on this post? 
There could be a number of reasons the bot doesn't comment on any given post. In fact, there's probably more reasons the bot doesn't comment than reasons the bot comments. 

The post could be performing well enough that the bot classifies the post as a 'possibly interesting question'. What "is" and "isn't" interesting is not really for the bot to decide, so it looks to the post karma to help make that decision. 

If the post isn't performing well enough to be 'possibly interesting', it looks at the text in the post, and searches for a question. 
The post could be written in a way that the classifier is unable to classify a sentences as a question, which is a fairly common problem. The person could be also requesting help as oppose to asking for help. While it's easy for a human to understand that there isn't a major, functional difference between those types of posts, the bot has trouble. 

The bot keeps a list of users who's posts it has commented on. To prevent spam the bot doesn't comment on posts made by those users in the future. (This is under the assumption that once someone is aware of the r/learnpython, they'll use it in the future. This assumption has proven to be rather strongly false and I'm reevaluating this action, but for now I'm maintaining this behavior.) 

If a user has already posted in r/learnpython by the time the bot decides to comment, but the post wasn't made at about the same time as the original, the bot decides its comment isn't needed.



#### The bot shouldn't have commented
That's very possible. The bot has a lot of trouble distinguishing between questions that are asking about the basics of python, "What is wrong with my code?" and questions which are primarily future-speculative, "What is the state of python?". It's bound to make some mistakes.

There are also key phrases that auto-trigger the bot, because they're ngrams which are almost always used when someone is asking for help. On rare occasion, that phrase will be used in a different way, causing an auto reply when any human would know that the OP wasn't asking for help. 

Acknowledging these issues, the bot is set to have fewer false positives than false negatives, so hopefully this isn't a frequent issue. 

If the bot really shouldn't have commented, downvote it. This gives the bot a metric that's more useful than 'good bot'/'bad bot' comments as more users vote than comment. 

#### I'm not learning python, I'm asking an advanced question
r/learnpython isn't a subreddit for beginners. While it might be specifically geared so that questions common to new programmers are easily addressed, the sub functions as a sister sub to r/python. Together one handles most news based submissions, and the other handles most questions. There is of course some overlap, but being a capable python programmer does not prevent anyone from asking a question and getting an answer on r/learnpython.

#### Shouldn't the bot Direct Message the OP rather than commenting? 
I thought about private messaging, but then you'll have multiple people (or bots) performing the same action without anyone being able to see. From the perspective of anyone on the receiving end, this could be a massive amount of spam.

Beyond that (and more importantly), if the bot makes a mistake, it deserves downvotes, not to hide in obscurity. A comment creates ownership. Other redditors votes determine usefulness. Moderators are more easily able to step in if necessary and ban it. 




#### Why doesn't the bot delete its comment when it's clearly wrong
It doesn't delete it's comments at any point because I feel like hiding from its mistakes is unethical and the bot deserves the downvotes. (Though I'm still torn between keeping the comment to own its mistakes, and deleting the comment to reduce clutter. I think owning the mistake is more important though, since it lets everyone, not just myself, see the bots success next to its failure rather than reweighing it so the bot looks like it performs better.)




#### Can chocolate be used in place of silicon in semiconductor materials?
While that has little to do with the bot, I appreciate the ingenuity of the question. 

Right of the bat I'd say probably not. Unpurified chocolate (Or would it be purified? After all, isn't chocolate in its most chocolate-y state purified chocolate? Though from the point of view of any semiconductor-canidate material, pure chocolate would make a very impure semiconductor) has a lot of chemicals that would act as impurities in any attempt to use it as a semiconductor. Your chocolate is probably best used as in insulator. 

If you purified it down to its base element, carbon, you might be able to make something useful out of it. [This paper](https://www.sciencedirect.com/science/article/pii/S025405840700675X) appears to describe a similar methodology, but used rice husk char instead of chocolate. If the methodology is robust enough to handle some front end changes to process the chocolate, you might be able to produce something functional. 

The most important thing to consider here is the fact that I have no idea what I'm talking about, and shouldn't be listened to on the topic of material engineering. 

#### Why comment when someone else already directed the user to r/learnpython
The bot decides to acknowledge the user but still comment in this case because the bot has a scripted 'help' note that emphasizes how to ask the question, and includes helpful links to help format the code. Its important to make sure new programmers understand how to ask a question and what information they need to help others help them.


#### The question was already answered, why did the bot still comment
The bot has a hard time telling whether or not an answer was already given, and if it was useful. There's code in the works to try to see if the OP has said "Thank you" or "That worked" or "It works now" but it's hard to test and not very reliable. 

Even acknowledging that the submission was answered, the post probably should have been made to r/learnpython, and the bot is intended to help make users aware of this. 


#### Why not use Deep Learning
Before I can use deep learning in any form, I need a lot of infrastructure code built up. That infrastructure lets me interact with reddit easily, switch computers I'm running on without much headache, make changes to the code and hopefully see the impact before anyone else. Deep learning could help the bot make decisions, but it will still need to be able to enact whatever decision the 'artificially intelligent' portion of the code decides. A lot of this early stage of the bot is built to make sure the next (and more complex) stages can be built smoothly. It's much easier to fight one battle at a time, and the first battle I wanted to fight was just getting the bot to interact with posts. 

I'm still not done with what I've called my "pre alpha" version of the bot. There's a lot of interaction capacity I want to build out: most notably I want to search stack overflow for plausible answers to some of the redditors questions. This might not make it into the bot before the end of the pre alpha phase. But it's a key function the bot is intended to have.

The final part is getting the bot and all of its infrastructure to run on a raspberry pi. 
The raspberry pi is my target hardware because it's a functional computer that uses low amounts of power and is relatively small making it easy to leave running all the time. 

Once a majority of the infrastructure for the bot has been dealt with, the various classification methods can be compared. Among them, deep learning will probably be looked at but just saying a program uses deep learning doesn't mean it's any good. Early on, I'm not sure whether or not there'll be enough training data for a neural net, or whether or not it'll be a significant improvement over simpler classification methods. There's also a lot of components to an 'ideally functioning' bot, and any individual component could be replaced with some form of NN, and each function will need plenty of training data, and then need to be evaluated. That in and of itself isn't too terribly difficult, but the infrastructure for the bot need(s/ed) to be built before that's something we can look at and even then it isn't a guarantee it'll be worth it. 

Thinking about deep learning, it's important to be mindful that the primary purpose of the bot is to be helpful. Any deep learning will only be implemented if there is a measurable improvement in helpfulness. The second limitation is the target hardware: the raspberry pi is cheap and low power, so it's ideal for the long term hosting. It comes at the cost of computing power and memory, which will limit how fancy any advanced classifier gets.

#### Could you add this Feature?
There's a lot of planned areas of expansion. The Roadmap outlines a large chunk of the things I want, but it doesn't really define an absolute order that any of the features will have. Some features (automatic question and answer) are features I'm nearly constantly working on, but are difficult to build and get working. 

Since the bot isn't in alpha yet, I'm probably not going to add features beyond what is touched on in the roadmap. That said, the roadmap has plenty of features outlined in it that aren't intended to be worked on until after alpha, (semi scripted conversations are a good example) so this isn't to say I won't consider it at all. 

If you have a feature you think would really help, feel free to message me or open an issue explaining what the feature would do, how it would impact the bots behavior including as why it fits a python helper bot role, and what resources you anticipate the feature using (more api calls, ram for a deep neural net, a new library to process something, etc). That will help me prioritize what is possible, and look into how it could be made.

#### When will you update the bot next?
This is a hobby project, so when I have free time, I work on it. If I get swamped with work, or home life gets hectic, the bot takes a back seat. If I tried to adhere to a strict schedule, the bot would probably eat up all of my free time and stop becoming fun. Since the bot is a part of the larger reddit community, I want to enjoy the work I put into it. Building on that, I want to feel like a given update will improve the bot, and not just push an update because it's on an arbitrary schedule. 

#### Aren't you tired of split ends in your carpet?
No, I moisturize my carpet so I never have to worry about walking over split ends. Dyson Carpet Moisturizing Cream is the best! 

#### The question was already posted to r/learnpython
This can get tricky. If the r/python post was made first, then someone suggested r/learnpython, then the r/learnpython post was made, the bot should be quiet. 

That said, there are usually a few ways this can happen: 
the posts were made at around the same time (usually less than 10 minutes of each other) or 
the posts were made more than a few hours apart. 

If the posts were made at about the same time, the bot should still comment.
(though this is up for discussion: the driving ethic is don't be spammy, and the driving goal is be helpful) 
The guiding principle here is if a user posts the same question in a lot of places, they should be told which places are not appropriate and which are. 

If the posts were a few hours apart or more, the bot guesses that they might be unique, unrelated posts. 

If the python post was made, then the suggestion was given, then the learnpython post was made, the bot shouldn't comment. But there could be a bug. I've been watching the bot fairly close so if this does happen, hopefully I'll be able to track down the bug before too long. 


#### Can I, and how can I contribute? 
Right now I'm not looking for contributors. The bot isn't in a position where I can manage the changes I need to make to it, as well as changes others are making. Once the bot hits alpha or beta, and the roadmap becomes less dramatic, then I'll be exceedingly happy to have contributors. 

When I get to that point, I'll probably just have folks tackle specific elements of the roadmap, but from my point of view that's a long way off.

#### What about snakes? 
They seem cool. I've got no problem with them.


#### Version Pre Alpha A0.5.00