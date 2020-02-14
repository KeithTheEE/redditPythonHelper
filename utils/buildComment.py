




'''  
Keith Murray 
email: kmurrayis@gmail.com
'''

# Post to reddit text block
def botIntro():
    msg = "Hello! I'm a bot!\n"
    return msg


def standardIntro():
    msg = '''It looks to me like your post might be better suited for r/learnpython, 
a sub geared towards questions and learning more about python **regardless of how advanced your question might be**. 
That said, I am a bot and it is hard to tell.'''
    return msg
def alreadySuggestedComment():
    msg = '''I see someone has already suggested going to r/learnpython, 
a sub geared towards questions and learning more about python **regardless of how advanced your question might be**. 
I highly recommend posting your question there. '''
    return msg
def alreadyAnsweredComment():
    msg = '''It looks to me like someone might have already answered your question. 
That said, I am a bot and it is hard to tell. 
In the future, I suggest asking questions like this in r/learnpython, a sub geared 
towards questions and learning more about python **regardless of how advanced your question might be**. '''
    return msg
def userCrossPosted():
    # Figure out what to say to the spray and pray
    msg = '''It looks like you posted this in multiple subs in a short period of time. 
In the future, I suggest asking questions like this in learning focused subs like 
r/learnpython, a sub geared towards questions and learning more about python **regardless of how advanced your question might be**. '''
    return msg

def commented_on_before():
    msg = '''I'm sure you've seen this information before, but just in case here it is as a reminder: 
    '''
    return msg

def baseComment():
    msg = '''Please follow the subs rules and guidelines when you do post there, it'll help you get better answers faster. 

Show /r/learnpython the code you have tried and describe where you are stuck. 
If you are getting an error message, include the full block of text it spits out.
**[Here is HOW TO FORMAT YOUR CODE For Reddit](https://www.reddit.com/r/learnpython/wiki/faq#wiki_how_do_i_format_code.3F)** 
and be sure to include which version of python and what OS you are using.

You can also ask this question in the [Python discord](https://discord.gg/3Abzge7), 
a large, friendly community focused around the Python programming language, open to those who wish to learn the language 
or improve their skills, as well as those looking to help others. 
'''
    return msg

def followSubRules():
    msg = '''Please follow the subs rules and guidelines when you do post there, it'll help you get better answers faster.

Show /r/learnpython **the code you have tried and describe in detail where you are stuck.** 
If you are getting an error message, include the full block of text it spits out.
Quality answers take time to write out, and many times other users will need to ask clarifying questions. Be patient and help them help you. '''
    return msg

def formatCodeAndOS():
    msg = '''**[Here is HOW TO FORMAT YOUR CODE For Reddit](https://www.reddit.com/r/learnpython/wiki/faq#wiki_how_do_i_format_code.3F)** 
and be sure to include which version of python and what OS you are using.
'''
    return msg

def discord():
    msg = '''
You can also ask this question in the [Python discord](https://discord.gg/3Abzge7), 
a large, friendly community focused around the Python programming language, open to those who wish to learn the language 
or improve their skills, as well as those looking to help others. 
'''
    return msg


def supervisedComment():
    msg ="\n\n###I am currently running in a supervised mode for testing and only comment when it's been approved"
    return msg

def signatureComment():
    msg = """\n\n***\n\n[^(README)](https://github.com/CrakeNotSnowman/redditPythonHelper) 
^(|)
[^(FAQ)](https://github.com/CrakeNotSnowman/redditPythonHelper/blob/master/FAQ.md) 
^(|)
^(this bot is written and managed by /u/IAmKindOfCreative) 
"""
    return msg

def inDevelopmentComment():
    msg = "\n\n^(This bot is currently under development and experiencing changes to improve its usefulness)"
    return msg