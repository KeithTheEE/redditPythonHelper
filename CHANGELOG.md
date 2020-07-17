

# CHANGELOG: Python Helper Bot Version pre Alpha A0.5.00
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


## [A0.5.00] 2020-07-XX

In Progress

### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

This project is not currently looking for other contributors

#### Big Picture: What happened, what was worked on

Major redesign and beginning new roles

#### Added
#### Changed
#### Deprecated
#### Removed
#### Fixed
#### Security
#### Tests 




### Main

### rpiManager.py

### Util Libraries

#### archiveAndUpdateReddit.py
#### botHelperFunctions.py
#### botMetrics.py
#### botSummons.py
#### buildComment.py
#### fix_json_archive_bug.py
#### formatBagOfSentences.py
#### formatCode.py
#### locateDB.py
#### lsalib2.py
#### nb_text_classifier.py
#### nb_text_classifier_2.py
#### questionIdentifier.py
#### rpiGPIOFunctions.py
#### scriptedReply.py
#### searchStackOverflowWeb.py
#### startupLoggingCharastics.py
#### summarizeText.py
#### textSupervision.py
#### updateLocalSubHistory.py
#### user_agents.py

### Tests



## [A0.4.01] 2020-07-17

Official.

### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

This project is not currently looking for other contributors

#### Big Picture: What happened, what was worked on
The Naive Bayes classifier is still in the code, but it is currently turned off. 

There are more pressing features, so the code for those functions is frozen until it can be addressed again in the near future. 

#### Added
#### Changed
- `nb_submission_classifier` in main's startup bot function is now `None`.
- `title_classifier` in main now returns false by default and the code which uses `nb_submission_classifier` is commented out. 
- `archiveAndUpdatedReddit` now imports praw's `NotFound` exception, and catches it when grabbing a non existent user.
- `phb_Reddit_User` has a attribute `_fake_account` which is set to false unless reddit throws a `NotFound` during lookup. At that point the user is remapped to a collection of fake values. 
- `phb_Reddit_User.getUserPosts` now returns and empty list if `_fake_account`
- `phb_Reddit_User.getUserComments` new returns an empty list if `_fake_account`
- Old error listed below `phb_Reddit_user` in a comment has been removed, the above changes now cover it.
- main `getReadyToComment` ignores submissions posted by `User._fake_account` by default as there's no real sense in commenting. 

#### Deprecated
#### Removed

#### Fixed
#### Security
#### Tests 




### Main
To get this version ready to go, the new nb classifiers are commented out since they're not up to snuff. 

### rpiManager.py

### Util Libraries

#### archiveAndUpdateReddit.py
- To get around the issue of users who have an account page that does not exist, the bot populates the user fields with false values, and adds a flag to the user: `_fake_account`.
- The fake account values are empty lists for comments and submissions, account creation time of `datetime.datetime.utcnow()`, an id of `0`, as well as 0 comment and link karma. 
#### botHelperFunctions.py
#### botMetrics.py
#### botSummons.py
#### buildComment.py
#### fix_json_archive_bug.py
#### formatBagOfSentences.py
#### formatCode.py
#### locateDB.py
#### lsalib2.py
#### nb_text_classifier.py
#### nb_text_classifier_2.py
#### questionIdentifier.py
#### rpiGPIOFunctions.py
#### scriptedReply.py
#### searchStackOverflowWeb.py
#### startupLoggingCharastics.py
#### summarizeText.py
#### textSupervision.py
#### updateLocalSubHistory.py
#### user_agents.py

### Tests


## [A0.4.00] 2020-07-15

Official.

### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

This project is not currently looking for other contributors

#### Big Picture: What happened, what was worked on
The python subreddit has undergone some changes, and now includes flair
on posts. This allows the bot to have a third classifier which it uses to instantly reply on in much the same way the keyword classifier functions. If a post has the 'Help' flair and it was applied within two hours of the original submission, the bot now auto comments on it, presuming it's never commented on that user before.

If a user has had the bot comment on them before, but uses the help tag, the bot is now allowed to comment again. 

The help message has been adjusted to have all caps on the block which talks about formatting your code. 

Logging has been changed to reduce notes from modules outside of the bot (praw and requests now only shows warnings or higher)

Some tests have also been added, however it does not cover a majority of the bot yet. 

A new classifier has been introduced and is being integrated into the bot. It's built off of a naive bayes classifier, but is aimed at classifying based on sentence structure. It's an ugly bodge but its proof of concept seems functional. Further information can be found below and in the header of the file, `nb_text_classifier.py` under utils.

Off of the new classifier, a larger naive bayesian has been built which is generally more functional. It has a fairly low false negative rate, but far too  high of a false positive rate. Both classifiers have been added and commented out in this version. 




#### Added
 - `check_for_help_flair` in main: a function that looks to see if the new flair is being used on the submission and if it's 'Help'. 
 - `grab_set_of_submissions_flair` in main: given a set of submissions, returns a dictionary with their id as the key, and their attached flair as the value
 - `check_for_help_flair_update`: as users can put flair on after they post, the bot needs to be able to compare the old flair with the new flair to see if a 'Help' flair has been added. This check currently runs for two hours after a post has been made. 
 - The bot now should auto reply to help flair added within two hours of the original submission, using the previously listed tools to keep track 
 - In utils, `startupLoggingCharacteristics` now exists. It adjusts non-python helper bot logs to warning level, and sets up the structure of the logs thereafter, defining the log structure use to be covered in main.
 - Added logging info in `archiveAndUpdateReddit`'s `comment_duplication_by_ratelimit_check` to make it more useful on review. It's still unclear if this patch solves the issue but this logging should make it easier to notice.
 - Added `nb_text_classifier.py`: a classifier which uses naive bayes over word pairs to calculate whether or not the title of a post is probably learning. It will get torn apart and reworked going foward, but the proof of concept might be worth integrating into the bot right now. Future work will look at a much more expansive naive bayes classifier over all the post features, so when it achieves a specific confidence it'll auto comment, independent of the age of the post. 
 - In `formatCode`: `astAndCodeopClassifications` uses modules `ast` and `codeop` to classify lines as code or not: requires their syntax to be valid. This may completely replace the classifier passed into `formatCode` as a whole. 
 - in `formatCode`: `remove_code_blocks` is added which remaps the code into a string '' 

#### Changed
 - Updated Year in License
 - Added Flair auto-reply explaination in README, de-emphasized bot summons to reflect the lack of active development, added a pre-alpha goal of a reddit post classifier, and adjusted the ethics section to acknowledge the newly allowed rule of commenting on a user multiple times under specific conditions.
 - Expanded on FAQ
 - Logging should now be more strongly defined by this bot, not `sessions` and `connectionpool`, hopefully that'll clean up bug hunts a bit.
 - Adjusted the 'format your code comment' to make it more noticable 
 - In `botHelperFunctions` `logPostFeatures`: it now records flair
 - In `learningSubmissionClassifiers`, `basicUserClassify` now is allowed to comment on a post by a user who had a prior post the bot commented on IF that user uses the 'Help' flair.
 - In `learningSubmissionClassifiers`, `basicUserClassify`: Bot is now allowed to comment even if user has directed others to learnpython before in the past. 
 - In `botHelperFunctions`, added `submission_flair_text` to the logged post features
 - Reworded a lot of the bot's comments in `buildComments` to emphasize that answers aren't instantanious and added emphasis to the format your code link, since that's the most often ignored aspect of users to follow the bots direction. 
 - Added a comment that r/learnpython is the place for questions regardless of how advanced the question is. 
 - `classifyPostLines` in `formatCode.py` now also takes in `astAndCodeopClassifications`'s classification for each line and returns it.
 - `alreadyCorrectlyFormatted` in `formatCode.py` takes in the astClassificaiton (it's really the pair of ast and codeop plus a hand written (artisanal?) dedent classification), and it classifies a line as code if the rwc, classifier, or astClassifier calls it code. (Given that the classifier--a simple naive bayes classifier is a bit overzelous--it might be adjusted or removed)

#### Deprecated
 - Commented out the call to karmaPlot in botMetrics. It'll need to be more fully removed later on, but the bot no longer needs it.
 - Not yet deprecated, but moving towards it: the classifier built by `buildTextCodeClassifier` in `formatCode.py` might be removed because it might be replaced by the `astAndCodeopClassifications` classifier. Use this as a chance to build an evaluation metric for this feature as a whole. 
#### Removed
#### Fixed
 - Under `archiveAndUpdateReddit`, when evaluating a submission, the bot checks the user of a post and grabs and rewraps it into the wrapper user class. On rare occasions, if a post would be deleted at just the right time, the bot would populate info for the post, the post would be deleted, then the bot would try to populate info for the user which is no longer tied to the now deleted/removed post. A try/except block has been added and now the submissionList waits until both the post and the user info has been successfully built out before it adds it to the list. 
#### Security

#### Tests 
 - Adding comment tree tests: basically purpose different inputs into buildHelpfulComment under main, and ensure the string needed is present
 - Added test to make sure test_check_for_help_tag() functions



### Main
 - The whole logging structure has been updated so that it's now defined in `utils`/`startupLogginCharacteristics`. This helps clean up the main and makes it easier to maintain a logging format through the program, preserve and transfer the format to other projects, and suppress uninformative logging messages by imported modules. 
 - `check_for_help_flair`, `grab_set_of_submissions_flair`, and `check_for_help_flair_update` have been added as have calls to these functions. This collection of functions helps track flair on posts as they've been added as it is not usually added by users right away. The most common reason the bot misses help flair is if the flair was added more than two hours after the initial submission time--reddit rewrites the post age to reflect the age it should be after subtracting the amount of time the submission was removed for. The bot assumes this doesn't happen and may need another change soon to address this issue as well. 
 - It now checks flair for the full 24 hours it watches a submission. 
 - `nb_text_classifier` and `nb_text_classifier_2` are imported in an experimental capacity
 - `lookForKeyPhrasePosts` now takes the naive bayes classifier, `nb_submission_classifier` as an input variable. From here it classifies the post as boolean: `learning_title`, and adds that submission to the list `submissionsToCommentOn_KP
 - `title_classifier` is the function which evalutes a submission on the naive bayes classifier side of things. Currently there's a lot of printing so I can see how it's working. 
 - Startup loads the naive bayes classifiers, only the full submission classifier is actually returned (`nb_text_classifier_2`). Similarly run bot takes it as input, and `if __name__ == "__main__":` handles the return and function call.

### rpiManager.py
 - `botStuff` loads the naive bayes classifiers, only the full submission classifier is actually returned (`nb_text_classifier_2`). Similarly run bot takes it as input, and `if __name__ == "__main__":` handles the return and function call.

### Util Libraries

#### archiveAndUpdateReddit.py
 - The user issue had been a rare but fatal problem that required a mod to be actively removing a post while the bot was reviewing the same post. Adding the flair bot as a mod increased the chance of this happening, as more posts were removed within 5 minutes of posting if they didn't add flair. I got lucky and was watching the bot when it died and I'm fairly sure this fix will address it, and increase it's resilancy. However the fix logging comment has yet to be saved so it's not absolutely clear that it'll address the issue as a whole. 
 - In `comment_duplication_by_ratelimit_check`, I've added some comments and a new logging message to increase the information logged when reddit starts breaking and  sends a 500 error when it tries to comment. It'll now log all usernames it can see on that post. This should help clairify if the bot's comment is logged by reddit. If reddit is super behind on displaying comments, this error/comment duplication will still occur, but hopefully I'll have more information going forward. 
#### botHelperFunctions.py
 - Flair is now recorded in logPostFeatures 
#### botMetrics.py
#### botSummons.py
#### buildComment.py
 - commented_on_before has been added to acknowledge that users have interacted with it before. (This should only activate during help flair--we'll see)
 - followSubRules has been adjusted to remind users that people take time to answer questions, and they may not get a reply right away
 - formatCodeAndOS has been adjusted to emphasize the link to how to format your code
#### fix_json_archive_bug.py
 - Created to handle trailing comments in the archive which were mistakenly given a new file due to a bug in the file spliter of `saveClassJson`. This is not yet functional and will not be used by the bot, but by an archive manager.
#### formatBagOfSentences.py
#### formatCode.py
 - Now imports `ast` and `codeop`
 - `astAndCodeopClassifications` now exists. It takes in a line of text. This just checks whether or not a line has valid syntax for python code. 
 - `astAndCodeopClassifications` is now called by the rewrapClassifications function.
 - `alreadyCorrectlyFormatted` now declares code is present if any line is called code by any of the three code classifiers. 
 - function `remove_code_blocks` has been added. If a line is called 'code' by either the rwc or astc, then it is replaced with a flag. Blocks of flags are stripped into a single replacement flag, `CODE` for text processing. 
#### learningSubmissionClassifiers.py
 - As a result of this version's changes, basic user classify now only prevents comments on users if they've been commented on by the bot before AND are not using the 'Help' Flair. Given this trend, it's reasonable to assume the bot will soon move to comment on users regardless of it's past history with them, as byinlarge the bot is usually correct within a reasonable degree when it's other classifiers activate.
#### locateDB.py
#### lsalib2.py
#### nb_text_classifier.py
This module was added in full in this version. 

It will be removed and replaced by `nb_text_classifier_2`. It was a proof of concept to see how well the naive bayesian classifier worked on titles of submissions. The prior experiment which failed, but built towards this was an LDA topic model, which never picked up on 

The module explains in depth what it does, so we'll briefly address its shortfalls here.

The model is pretty useful, getting a solid true positive rate, but always hitting false positive on anything that has a structure similar to "Data manipulation with Numpy":  titles which just state the subject. Half the time posts of that style are showcases of projects or explainations about that subject, and the other half of the time they're questions centered on the topic.  

The model in `nb_text_classifier_2` has this same shortfall.

Specific to `nb_text_classifier`, the code is written in a way that's difficult to extend to a full submission classifier, as well as difficult to tweak to test with different thresholds. It remains as a solid first shot which is why it is being committed, but it almost certainly wont be preserved past this. 


#### nb_text_classifier_2.py
The key change to this classifier is the ability to add various submission features to the classifier. Though it's large shortfall is the lack of using the LogSumExp trick to handle that addition. 

Using Aziraphale (personal database manager) and `mod_judged_posts` to gather posts from the archive, it splits the archive into a train and test set, and 'successful' and 'learning' classes. 

It is passed to the reddit submission classifier class (`reddit_submission_classifier`) which splits the 'judged' posts into two categories and an undefined collection, 'Learning', 'Successful', and 'unclassified'. Submission features are broken down to 

Features it currently evaluates between the classes are: Title word pairs, selftext word pairs, and link type (selftext, outlink, image, video, crosspost). 

The `reddit_submission_classifier` splits the submissions into the three groups, and passes the labeled classes ('successful' and 'learning') into `build_classifiers` one by one, which populates `reddit_submission_class_fields_naivebayes`. Titles and selftext are preprocessed by `text_preprocessor` and link types are preprocessed by `reddit_link_simplifications` then placed into `simple_feature`.  

After the `reddit_submission_class_fields_naivebayes` object is built for each class, you can pass a submission to each one using the `get_p_of_submission_in_class` attribute to get the probability that some given submission alpha is generated by the distrobution in the model for that class (be it the learning or successful class). 

The parent class, `get_p_of_submission_in_class` will classify a submission by getting the likelhood it belongs to both models, and classifying the submission according to which class has a greater negative log likelyhood. It then creates a hand wavey confidence score based on the difference between the two most likely classes normalized by the largest negative log likelyhood. This isn't valid science, but this was a proof of concept and I needed to get a number value which made some tactile sense that I could use as a threshold for letting the bot comment. 

Under the current version, confidence is defined as `(np.log(np.abs(score_diff)))/(-s_score)` where `score_diff` is the difference between the two most likely classes (and since there's only two classes--successful or learning--it's the difference between those two), and `s_score` is the negative log likelyhood of the most likely class. From there the bot was 'allowed' (in a testing/quiet mode capacity) to comment if the confidence was greater than 0.004 and the s_score was greater than -1000. Again, these are hand wavy values only used to get a sense of whether or not the classifier needed more work. Which, in short it does.

`get_p_of_submission_in_class`, an attribute of `reddit_submission_class_fields_naivebayes` needs to use the LogSumExp trick instead of a simple summation since the presence of selftext, and the content of that selftext is an attribute of the link type feature: so it can't simply be summed with the same weight as title text, or have the same impact as linking to a blog post. There was a hope that this statistical sin would still be functionally allowable, but that isn't the case. 

In all, the code will remain, the logsumexp trick shouldn't be rough to add, and it was a useful improvement off of the `nb_text_classifier` file. 

#### questionIdentifier.py
#### rpiGPIOFunctions.py
#### scriptedReply.py
#### searchStackOverflowWeb.py
#### startupLoggingCharastics.py
#### summarizeText.py
#### textSupervision.py
#### updateLocalSubHistory.py
#### user_agents.py

### Tests


## [A0.3.02] 2019-09-16

Official.

### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

This project is not currently looking for other contributors

#### Big Picture: What happened, what was worked on
The bot was commenting multiple times on the same post if a ratelimit error occured, and a bodge is now in place to check this behavior, the previous page checked its own comment history to minimize api calls (assuming grabbing the most recent 2 bot comments was enough). However, when reddit's servers have an issue it became apparent that the bots user history and the submission's comments do not necessarily match up. 

Now the bot checks the submission for multiple comments, and also automatically assumes that the comment went through just in case.


#### Added
#### Changed
 - Bug Fix [Issue 1](https://github.com/CrakeNotSnowman/redditPythonHelper/issues/1#issue-473053676): To address Issue 1, in Archive and Update Reddit: comment_duplication_by_ratelimit_check() which takes in reddit and the submission,  and now grabs an instance of the submissions top level comments. It then itterates through the comments checking for a match with its own username, and if that is found, it adds it to a list of its comments on that submission. In the event that multiple comments by the bot are found, it logs an error
 - The bot then ignores the previous bug fix and assumes the comment went through. This change should be reverted eventually, but until another server issue occurs, I can't see how the bot will behave and as such have to assume that despite the 500 error, the server will show the comment eventually. 
#### Deprecated
#### Removed
#### Fixed
#### Security


### Main

### rpiManager.py


### Util Libraries

#### archiveAndUpdateReddit.py
#### botHelperFunctions.py
#### botMetrics.py
#### botSummons.py
#### buildComment.py
#### formatBagOfSentences.py
#### formatCode.py
#### learningSubmissionClassifiers.py
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

## [A0.3.01] 2019-07-26

Official.

### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

This project is not currently looking for other contributors

#### Big Picture: What happened, what was worked on
The bot was commenting multiple times on the same post if a ratelimit error occured, and a bodge is now in place to check this behavior 


#### Added
 - Bug Fix [Issue 1](https://github.com/CrakeNotSnowman/redditPythonHelper/issues/1#issue-473053676): To address Issue 1, in Archive and Update Reddit: comment_duplication_by_ratelimit_check() which takes in reddit and the submission, grabs an instance of the bot as a user, and checks the 2 most recent comments link id against the submission in question's id. 
#### Changed
 - In commentOnSubmmission: RateLimitError Catch now checks if comment went through anyway. If so, it breaks out of the try again loop. 
#### Deprecated
#### Removed
#### Fixed
#### Security


### Main

### rpiManager.py


### Util Libraries

#### archiveAndUpdateReddit.py
#### botHelperFunctions.py
#### botMetrics.py
#### botSummons.py
#### buildComment.py
#### formatBagOfSentences.py
#### formatCode.py
#### learningSubmissionClassifiers.py
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


## [A0.3.00] 2019-03-22

Official 

### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

This project is not currently looking for other contributors

#### Big Picture: What happened, what was worked on

Archiving for submissions, comments, reddit bot actions, mod actions, and a collection of users responses to comments and the source comment has been added. A majority of these archives are in json and they're now saved to an external drive to reduce the risk of a short sd card lifespan on the raspberry pi. Front end bot functionality should be relatively unchanged, but the backend got a lot of updates. 

#### Added
 - archiveAndUpdateReddit submission class now has a num_comments attribute. This impacts the karma plots because this attribute gets updated as well.
 - archiveAndUpdateReddit submission class now has make_shortlink() returns short url for submission
 - archiveAndUpdateReddit submission and comment class now has export_to_dict() and load_from_dict(submission_dict) to help archiving
 - a block of code which runs once every 12 hours has been added in the main runBot() loop, allowing for mod action archive to be run. A similar function will be added for the database backup soon.
 - A whole bunch of functionality in archiveAndUpdateReddit which finally makes the module archive reddit related things! Specifics below. 
 - A submission focused archive has been created
 - A combined submission and comments archive has been created
 - A mod action archive has been created for bot training/classificaiton
 - A bot action archive has been created for redundancy in case of sd card failure
 - A user reaction archive has been created for future machine learning goals to help the bot adjust its comments as needed. 
 - locateDB() now looks for external drives. One drive is intended to host a local copy of stackoverflow and the indexing needed to quickly search it, and two other usb drives are intended to be the reddit focused archive. This structured is intended to isolate a majority of the high frequency write processes followed by a less frequent backup write process, and keep it away from the sd card hosting the pi os, and away from the large SO database as well. 
#### Changed
 - submission class score_History is reordered, now each element in history reflects: [self.score, self.upvote_ratio, self.num_comments, now]
 - submission class now has an added feature to load from dict instead of populating from a praw class. It assumes the popuation call will be next
#### Deprecated
#### Removed
#### Fixed
#### Security


### Main
 - phbArchPaths is returned from archiveAndUpdateReddit.startupDatabase() and has been added as an input to a number of functions, including runBot, buildHelpfulComment, getReadyToComment, botSummons.handleInbox, archiveAndUpdateReddit.updatePosts
 - list of mods is now grabbed from archiveAndUpdateReddit.getMods(reddit, sub='python') for redundancy and reddit error isolation
 - if the bot comments on a submission, botMetrics.predictUserReaction(reddit, user, phbArcPaths) is called for a later project. 
### rpiManager.py


### Util Libraries

#### archiveAndUpdateReddit.py
 - num_comments attribute has been added to submissions class. This should be an interesting metric which could help classification. Note that due to removed or deleted comments, this might not reflect the actual count of comments because they don't appear but are still counted
 - make_shortlink() is simple and should prove useful, especially when refering to a post in a text message status update
 - export_to_dict() converts the class features into a dictionary structure. This should allow for simple implementations of various archiving methods, (sql, xml, or json) which should let me try multiple structures during pre alpha and alpha and decide on what works best later on. Seperate functions can take the dictionary and move it straight to the end data structure in a more modular fashion
 - load_from_dict(submission_dict) will be used to pull and populate from archives. This includes the ability to have a 'save state' for reboots/updates that way data is lost less frequently.
 - submission class score_History is reordered, now each element in history reflects: [self.score, self.upvote_ratio, self.num_comments, now]
 - json module has been added
 - shutil's copyfile module has been added
 - kmlistfi module has been added
 - export_to_dict and load_from_dict functions have been added to the submission and comment class
 - Fixed a bug with submission.get_all_comments, now successfully gets all comments (praw object 'submission' does not return a list of comments when submission.comments.replace_more(limit=None) is envoked, so to itterate through you itterate over praw object submission.comments.list())
 - Fixed a bug with custom User class where if a user is deleted, it populated that info to self.author when it should actually be self.name. Now self.name gets populated. 
 - Using keyword arguements ageLimitHours and ageLimitTime in user.getUserPosts() and user.getUserComments() it's now possible to get users submissions and comments from x hours in the past up until now, and from a datetime instance up to now. (this assumes they have commented or submitted fewer times than the limit keyword arguement is set to)
 - get_comment_by_ID now splits on an underscore character hopefully making it easier to pass comment IDs directely from parent_IDs. It does need an added check that the prefix to the underscore is the prefix of a comment though
 - phbArchPaths is returned from archiveAndUpdateReddit.startupDatabase() and has been added as an input to a number of functions, including grabAndUpdateNewPosts(), updatePosts()
 - getMods() has been added which returns a list of moderators in a subreddit when provided with a praw reddit instance and keyword arguement sub. In this case it's default is python.
 - makeCommentKarmaReport will be deprecated soon. But I figure I'll wait just a bit longer. The scatter plots aren't needed, though the line plot will be maintained. This is noted because there's comments along this set of function calls about deprecation.
 - joinAndMakeDir() has been added to flexibly generate an archive file structure in a provided folder location. With respect to the pi, it'll be the USB drive.
 - createFile() has been added which opens a file for appending and closes it right away to ensure a file with the input name exists
 - startupDatabase now takes in archive_Locations which has the path to the root of the archive and root of the backup which are outputs of the database focused portion of locateDB.
 - In startupDatabase() the archive file structure is (mostly) laid out. All currently needed subdirectories to the archive are generated, and if the archive does not have a copy of the bot actions (postHistory.txt, summoningHistory.txt, and UsernamessList.txt (which I'm now noticing has a typo)), the files are copied to the archive. The archive paths are bundled and returned as phbArchPaths along with the previous returns of userNames and postHistory.
 - updateDatabase() now takes in phbArcPaths and updates the username and postHistory files in the archive as well as in the previous location for redundancy.
 - getModifiedDate() and sortFileByModification() are added for saveClassJson()
 - saveClassJson() takes in a class_struct, database_path, and max_MB (with a default size of 10). Given a path for a json database, the function grabs a list of all files at that location, and grabs the most recently modified file. Then it checks if the file is too large, if so it closes the file with a end bracket ']' so the file is full json. Then it creates a new nearly json file. Class_struct is expected to have an export to dict function, then the saveClassJson with take that dictionary, convert it to a json string, and save that string to the file.
 - in removeOldPosts for each popped post, it saves the submission, and submission and comments into the archive.
 - export_dict_to_json() converts a dictionary to a json string, and if there's an unknown datatype it's classed as a string (this is enacted on datetime classes)
 - reDateTimeify_submission() takes a dictionary that was converted into one from a json string and grabs the datetime strings and reclasses them as datetime instances
 - load_submission_from_json() takes a json string and returns it to a submission class. 
#### botHelperFunctions.py
#### botMetrics.py
 - predictUserReaction() takes a user and grabs their 15 most recent comments. It then checks if the comment is a reply to another comment. If so, it grabs and saves to the archive the parent comment and the user comment.
 - archiveModActions() takes the python mods and their last recorded actions and grabs all comments since then, then records all comments in the python sub. This will be used for crowd sourced classification of learning posts, and used to measure the bots usefulness. Automod is excluded from this list for obvious reasons. 
 - processKarmaRequest now takes in phbArchPaths and saves the plot to the archive location rather than the sd card.
#### botSummons.py
- actOnSummons() and handleInbox() now take phbArchPaths as inputs
#### buildComment.py
#### formatBagOfSentences.py
#### formatCode.py
 - os module is now imported
 - handleSummons() and makeFormatHelpMessage() now take phbArchPaths as inputs.
 - handleSummons() loads and saves summoning history to and from the archive
#### learningSubmissionClassifiers.py
#### locateDB.py
 - SSD, and two thumb drives have been added to the pi. The databases will be for wiki and SO on the ssd, and a post archive and archive backup on the thumb drives
 - archiveDB() has been added for this express purpose
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



## [A0.2.01] 2019-03-05
Official
### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

This project is not currently looking for other contributors

#### Big Picture: What happened, what was worked on

Primary focus is bug identification and fixes from the 0.2.00 udate.

#### Added
 - Added 'ResponseException' in archieveAndUpdateReddit to the except statement on the server error level. Apperently ServerError is not the only exception thrown for 500 errors, though response exception is classified as a server error. For some reason catching serverError does not catch responseException as I had previously interpurted the documentation 
 - Added 'APIException' from praw.exceptions in archieveAndUpdateReddit. This then checks the exception to see if it was a rate limit error that reddit threw, and if it was it retries after a backoff time for rate limiting, and if not it escelates the error out of the exception catch. 
 - Generate Karma Plot: under bot summons, if an approved user (currently only myself) messages the bot, it will generate and email a plot for karma vs time. This is used to double check if a post looks to be naturally gaining karma or judge if there's manipulation behind it. Functions added are in botSummons, botMetrics, and textSupervision
 - in archiveAndUpdateReddit, function updateYoungerThanXPosts: a function which is handed set of posts and updates all post younger than x hours, allowing for a higher resolution of upvotes/downvotes for young posts than older posts. 

#### Changed
 - Bug Fix [56be1fc]: getReadyToComment now passes quietMode
 - Bug Fix [c8897b0]: removed prefix 'botHelperFunctions' from a get_learning_sub_Names() call since the calling function now resides in botHelperFunction Module as well
 - Bug Fix [21def4c]: learningSubmissionClassifiers should import itself to itself
 - Bug Fix [37765bd]: Adjusted bot summons so capitalization of username doesn't matter
 - Bug Fix [d760d1f]: Key Phrase Autoreply oldPosts now is set to setOfPosts.copy().  was never triggering because oldPosts automatically updated as new posts were added to setOfPosts due to a shallow copy. 
 - Bug Fix [dc9d4d9]: in formatCode the summoning message was saved with no stripping of newline characters. That is no longer the case as newline characters should now be replaced with a space character
 - Adjusted max age of a reformat summons from 2 hours to 4 hours. While I like two hours better, I'm just not likely to notice and respond to an error in 2 unless I'm lucky. 4 hours isn't too old but it gives me a chance to get the message reformatted after an error crops up
 - Added line length as a feature to the code V text classifier. Hopefully it's not classifying just on this and also not ignoring this, but it seems to be doing well in early testing. (update: It doesn't appear to be impacting the classification)

#### Deprecated
#### Removed
 - In main: idealQuery(), stackOverflowInfo(),buildHelpfulComment_DEPRECATED(), xrequest_Key_Word_Filter(), xbasicQuestionClassify(), xgetSubsUsersInteractsIn(), xbasicUserClassify(), xuser_Already_Took_Advice(), xpopOldSpammers(), AND xrunBotX() 
#### Fixed
#### Security


### Main
 - Old functions which were previously deprecated were removed: idealQuery(), stackOverflowInfo(),buildHelpfulComment_DEPRECATED(), xrequest_Key_Word_Filter(), xbasicQuestionClassify(), xgetSubsUsersInteractsIn(), xbasicUserClassify(), xuser_Already_Took_Advice(), xpopOldSpammers(), AND xrunBotX(). They have all been officially removed as they were moved in v a0.2.00, and the move did not break the code so the old copy was no longer useful. 

### rpiManager.py
 - under if main added structure to read a gpio switch to change startup behavior so the bot can either act as normal, pull from github on starup, or exit the program preventing automatic running on a reboot. Code is not yet active.

### Util Libraries

#### archiveAndUpdateReddit.py
 - function updateYoungerThanXPosts: a function which is handed set of posts and updates all post younger than x hours, allowing for a higher resolution of upvotes/downvotes for young posts than older posts. In the future this will be used to help the bot decide to comment on a post earlier.

#### botHelperFunctions.py
#### botMetrics.py
 - userTookAdvice is currently commented out. 
 - processKarmaRequest(): Given a submission ID, checks current set of posts for a matching ID. If there's one, it takes the score history and plots it by time. 
#### botSummons.py
 - added kplot summon via direct message to the bot. This lets me look at upvote/downvotes for a post by time. 
#### buildComment.py
#### formatBagOfSentences.py
#### formatCode.py
 - created a few hollow functions for more useful code formatting. 
#### learningSubmissionClassifiers.py
#### locateDB.py
#### lsalib2.py
#### questionIdentifier.py
#### rpiGPIOFunctions.py
 - Building out startup switch functions. Define a few new pins to check on startup, and define them as input. 
#### scriptedReply.py
#### searchStackOverflowWeb.py
#### summarizeText.py
#### textSupervision.py
 - send_karma_plot() added. The karma plot is sent either via email or mms (or both) depending on the subject line of the summoning dm. 
#### updateLocalSubHistory.py
#### user_agents.py

### Tests 



## [A0.2.00] 2019-01-10
Official
### Contributors
Keith Murray

email: kmurrayis@gmail.com |
twitter: [@keithTheEE](https://twitter.com/keithTheEE) |
github: [CrakeNotSnowman](https://github.com/CrakeNotSnowman)

Unless otherwise noted, all changes by @kmurrayis

This project is not currently looking for other contributors

#### Big Picture: What happened, what was worked on

Folder structure has been redone, most helper functions have been moved to the utils folder. The code for vA0.1.01 has been posted to github so it's easier to completely mess up the vA0.2.00 update and have the ability to undo it. In that vein the work for the bot is now conducted in the development branch. 

A majority of reddit api calls with praw are now wrapped in custom methods to handle more variety of issues, including reddit server downtime. Most reddit related actions are now exclusively done in archiveAndUpdateReddit, with very few reddit calls which are not passed through that module. The custom wrappers are a huge change and should increase the length of time the bot can run on the pi without random errors killing it (With the exception of memory and threading errors, which will be investigated soon). 

The bot can now be summoned to reformat code by making a comment on reddit that says, "/u/pythonHelperBot !reformat". The classifier is not perfect, but it's a starting point and should help some reformating. 

#### Added
 - The bot is now licensed under the MIT license
 - Source code has been posted to github (it's a big deal: woo!)
 - .gitignore file has been made
 - associated personal libraries have also been posted to github
 - botHelperFunctions.coolPlacesToDonate(): a function (currently empty) that returns a website asking for donations. Ideally it's be sites that are non profit, and are for causes that either center around the bots actions, or center around my own favorite charities. Should rarely trigger.
 - botHelperFunctions.ramCheck(): Currently empty function. will return how much ram is being used and how much is free. Hopefully this will help when the pi runs for months then suddenly stops working, giving me a chance to see if there was a slow and creeping memory error. 
 - botHelperFunctions.load_autoreply_key_phrases(): rather than hard coding, key phrases can be loaded into a text file.
 - formatCode.py: a module to take in a submission or comment, and reformat it adding 4 spaces to help display the code on reddit. It's a simple classifier right now, and has room for improvement 
 - botSummons.py: a module to process any and all keyword summoning. 
 - misc/pyProgramTrainingLines.txt: training file for the 'code' classification, the 'text' is taken from the nltk Brown sentence corpus on 'news'. 
 - buildComment.py has been added, now functions as the holding ground for variations on the primary bot comment. 
 - learningSubmissionClassifiers.py has been added. It's intended to be base home of the post classifiers, clearing up the main and making modifications easier. This means a large number of functions in the main will soon be deleted (marked with prefix x) since they should be sucessfully migrated.
 - archiveAndUpdateReddit: Ho Boy we're in for a lot here. Almost everything in this file has been changed to wrap all possible praw api calls into a custom class which has ugly but hopefully functional try/excepts wrapped in a while True loop attached to a backoff timer such that any time any anticipated exception gets raised. This should prevent the reddit server timeouts from causing random bot deaths as well as help isolate api calls to functions which are prepared for the concequences. It's big, it's ugly, but it's in a nice rubber padded room that's shielded from reality. So it works I guess. We'll see. A lot of breaking changes have been made. To comment on a submission or comment the bot now requires "quiteMode" to be passed, helping reduce errors caused by impropperly silencing the bot 




#### Changed
 - logs now record source module, function name, and line number when a log entry is named. New format is now: 
 YYYY-MM-DD HR:MN:SC,MSC - Level - module:function():line - Message
 - Most helper functions have been moved to a seperate folder named utils. This should help reduce clutter 
 - learningSubs.txt has been moved to misc/learningSubs.txt
 - codeVTextClassifier is now added to the startup and runbot functions, changing the return and in args respectively
 - shortenRedditURL(url) has been moved from main to botHelperFunctions module
 - The main runBot loop has been redone to be more responsive and easier to understand, breaking it's wall of code into a few smaller functions as well as only sleeping for 30 seconds on each itteration. Then it checks a couple of blocks which are set to run after different sleeping periods (currently oneis once every 3 minutes, and the other is once every 15 minutes). Because of the risk of breaking changes, the 'moved' functions have been copied, and their legacy 




#### Deprecated
 - buildHelpfulComment has been changed and rename as buildHelpfulComment_DEPRECATED with a new buildHelpfulComment acting in the same namespace. The new one does not have the stack overflow answer section included as that's been non functional for too long, and not needed. The new one is also cleaner and easier to understand.  
 idealQuery() and stackOverflowInfo() have been commented out and will be removed soon. 
 - a number of functions in the main file will soon be removed, as it stands they've been renamed with the prefix x. Their removal will take place with the update is stable on the pi
#### Removed

#### Fixed
 - Fixed some of the changelog formatting

#### Security


### Main
A solid amount of restructuring took place. The praw structures should now be custom classes to help isolate where server errors are handled. Thankfully main() doesn't really feel a large impact from this as most of the attributes are the same with the exception of 'created_utc', which is now cast as a datetime object. 

The main runBot loop has been restructured to make it easier to add classifiers, change how often the bot runs specific classifiers, and add extra functions (in this itteration the !reformat command). It will continue to be redesigned in the future.

A large number of functions have been moved away from the main into their own modules (classifiers and comment skeleton)
### rpiManager.py
Relatively little changed here with the exception of the codeVtextClassifier varible being added to the return of startupBot() and input of runBot(). I expect in the next few updates this will start pulling updates from the master branch, reducing the amount of manual updates I need to make. 

### Util Libraries

#### archiveAndUpdateReddit.py
So much has been redone. Hopefully this reduces the number of bot killing errors due to various types of internet issues, and increases the amount of time the bot can run without maintainance, by hand rebooting, and handling of other issues which can be anticipated and coded out. 

Class wrappers for users, submissions, comments, and inbox messages have been added, as well as wrappers for reteriving any of those values. 
#### botHelperFunctions.py
Multiple functions have been moved here from main
#### botMetrics.py
#### formatBagOfSentences.py
A module to order a handed bag of sentences, and insert new lines to make paragraphs. Currently does not function. 
#### formatCode.py
Trains a classifier on code vs text, returns the classifier. Later, takes in a textBlock and classifies it on a 'newline' basis, rather than a tokenized sentence basis. The feature profile is build from a modified lz78 algorithm, where 
#### locateDB.py
Added entry for Code database for the code and text classifier
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


***

> TV Reporter: "It's just gone 8 o'clock and time for the penguin on top of your television set to explode."

> *Boom*

> Woman watching TV: "How did he know that was going to happen?"

> TV Reporter: "It was an inspired guess."

Episode 22 in Monty Python's Flying Circus
