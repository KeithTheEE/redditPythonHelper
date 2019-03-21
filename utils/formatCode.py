
import nltk
import time
import os
import datetime
import gzip
import kmlistfi
import random
from random import shuffle
import logging
from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer
from nltk.corpus import brown
from nltk.metrics import ConfusionMatrix


from utils import archiveAndUpdateReddit
from utils import buildComment

'''
Tools to take a reddit message and classify lines as code or text


Keith Murray
email: kmurrayis@gmail.com

Notes
---
`buildTextCodeClassifier` uses NLTK's Naive Bayes Classifier to 
build a classifier based on the nltk provided Brown 'news' dataset

Future Improvements:
Explore better classifiers. Under this incarnation of the bayes 
classifier, the line is either code or text with near complete 
confidence, even when it's wrong. 



Markdown Parsers and other Useful Links
http://piumarta.com/software/peg/
https://github.com/jgm/peg-markdown/blob/master/markdown_parser.leg




'''



def loadAndShuffleCodeSample(flsource,returnSize):
    randomSeed = random.randint(0,1000)
    with open(flsource,'r') as fl:
        code = fl.readlines()
    random.Random(randomSeed).shuffle(code)
    logging.debug("Random Seed for Code Samples Shuffle: " + str(randomSeed))
    return [(x, 'code') for x in code[:returnSize]]

def mod_lz78(s, D={}, k=4):
    '''Almost the LZ78 compression scheme
    '''
    s = s.lower()
    s = s+'\n'
    s=s*k
    #print(s)
    i = 0
    word_len = 1
    while True:
        word_len = 1
        while s[i:i+word_len] in D:
            D[s[i:i+word_len]] +=1
            word_len += 1           
            if (i+word_len)>=len(s):    
                break
        if (i+word_len)<=len(s):
            D[s[i:i+word_len]] = 1
        else:
            break
        # Here is the LZ78 modification, based on my previous work with DNA profiling
        # This mod ruins data compression, but increases the profiling accuracy with DNA
        i = i+1#+word_len 
        #print(i, word_len, D)
        #if i
    return D
            

def detokenize(token_text):
    detokenizer = TreebankWordDetokenizer()
    return detokenizer.detokenize(token_text)

        
def code_text_features(text):
    d = mod_lz78(text, {})
    d[0] = len(text)
    return d

def buildTextCodeClassifier(sourceDataPath):
    '''
    Takes in a training file filled with coding samples
    and uses the NLTK provided Brown News sentence corpus and builds
    
    '''
    
    randomSeed = random.randint(0,1000)
    sampleSize = 2000
    # Load code samples
    #flsource = "misc/pyProgramTrainingLines.txt"
    code = loadAndShuffleCodeSample(sourceDataPath, returnSize=int(sampleSize/2))
    if len(code) < int(sampleSize/2):
        sampleSize = len(code)*2
        logging.warning("Warning: Not enough code. New sample size = " + str(sampleSize))
    #print(len(code))
    #print(code[:10])
    # Load comment samples
    #comments = [(x.text, 'text') for x in nltk.corpus.nps_chat.xml_posts()[:int(sampleSize/2)]]
    sents = brown.sents(categories='news')
    sents = [detokenize(sent) for sent in sents]
    #print(sents[0])
    comments = [(x, 'text') for x in sents[:int(sampleSize/2)]]
    logging.debug("Shuffling Code")
    posts = code+comments
    random.Random(randomSeed).shuffle(posts)
    #print(posts[:10])

    logging.debug("Random Seed for Training Shuffle: " + str(randomSeed))
    logging.debug("getting features")
    featureSets=[(code_text_features(post[0]), post[1]) for post in posts]
    test_cut = 0.1
    size = int(len(featureSets) * test_cut)
    train_set, test_set = featureSets[size:], featureSets[:size]
    logging.debug("Training Size: " + str( len(train_set)))
    logging.debug("Testing Size:  " + str( len(test_set)))
    logging.debug("  Training Model")
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    logging.debug("  Model Accuracy: " + str(nltk.classify.accuracy(classifier, test_set)))
    '''
    ref = []
    tagged = []
    for i in range(len(test_set)):
        c = classifier.classify(test_set[i][0])
        tagged.append(c)
        ref.append(test_set[i][1])
        if i < 5:
            #print("Text:\n", test_set[i][0])
            print(test_set[i][1] + ':' + c + ' | Actually:Classified')
            #print("Classified: ", c)
            #print("Actually:   ", test_set[i][1])
    '''
    # I can't get the confusion matrix to work in a saved format. 
    #logging.debug(str(ConfusionMatrix(ref, tagged)))
    return classifier#, train_set, test_set




def rewrapClassifications(line):
    '''
    This is a by hand curriated list of markdown circumstances which 
    define code blocks. 

    This function classifies a line as either empty, codeblock, code,
    or NA,
    
    empty: the line is either a newline character, or the value `&#x200B;`

    codeblock: A tripple ` is present, starting or ending a codeblock

    code: Either the line leads with at least 4 spaces, or the line starts 
        and ends with a ` character.

    NA: The line contains text of some form, but it definetly isn't 
        formatted as code
        
    '''
    # Function to by hand classify lines
    #  Should be used to bolster the naive bayes classifier
    if line.strip() in ['&#x200B;', '']:
        # 0 width space character, effective newline or standard newline
        c = 'emptyline'
    elif line.strip()[0:3] == '```':
        c = 'codeblock'
    elif line.strip()[0] == '`' and line.strip()[-1] == '`':
        c = 'code'
    elif line[:4] == '    ':
        c = 'code'
    else:
        c = 'NA'
    return c

def valid_python_syntax(line):
    '''
    Takes line and evalutes whether or not it follows BNF Grammar rules
    for the python language 

    only returns false if the line definetly does not evaluate 

    Does not care about the existence of varibles

    '''


    return 

def id_Missing_Whitespace(codeBlock):
    '''
    Simple Hand Curiated 'missing whitespace' classifier.

    The code parses the text looking for a line which when stripped
    leads with an indent trigger. The unstripped indent level is noted
    then the next non emptyline is looked at

    Parses through presented message line by line, looks for code blocks
    In code blocks, checks for the pressence of 'def', 'if', 'elif', 'try',
    'except', 'else', 'while' 

    This function assumes it's being handed valid code, not text

    references:
    https://docs.python.org/2.0/ref/logical.html
    https://docs.python.org/2.0/ref/indentation.html


    '''

    indentTriggerHeads = ['def', 'if', 'elif', 'else', 'try', 'except', 'while', 'for'
                            'class', 'with']
    indentTriggerTails = [':']
    emptyLine = ['&#x200B;', '']


    lines = codeBlock#.split('\n')
    root = 0
    level = root
    wsCount = 0
    i = 0
    while i < len(lines)-1:
        line = lines[i]
        if line.strip() not in emptyLine:
            tokens = line.strip().split()
            if (tokens[0] in indentTriggerHeads) and (tokens[-1][-1] in indentTriggerTails):
                # Whitespace Indent Should Occur
                pass
        i += 1


    return False

def whitespace_Error_Recovery():



    return

def classifyPostLines(textBlock, classifier):
    '''
    This classifier is pretty consistenly all or nothing
    A larger code base to train from will help significantly, but is not currently
    a critical requirement 
    '''
    lines = textBlock.split('\n')
    classifications = []
    rwclassifications = []
    for line in lines:
        c = classifier.classify(code_text_features(line))
        classifications.append(c)
        rwc = rewrapClassifications(line)
        rwclassifications.append(rwc)
        #print(c, rwc, line)
        '''
        print('\t>',c, line)
        dist = classifier.prob_classify(code_text_features(line.strip()))
        for label in dist.samples():
            print("\t\t>%s: %f" % (label, dist.prob(label)))
        '''
    return classifications, rwclassifications   


def alreadyCorrectlyFormatted(c, rwc):
    '''
    Function itterates through the by rewrapped classifications
    and compares them to the naive bayes classifications. If there 
    are no rewrapped 'NA' lines classified as 'code' by the naive bayes 
    classifier, then it determines that the code has already been 
    correctly formatted.

    Assumes there is no code present and if there is, it has been 
    correctly formatted. 
    '''
    codePresent = False
    correctlyFormatted = True
    for i in range(len(rwc)):
        if rwc[i] == 'code' or c[i] == 'code':
            codePresent = True
        if rwc[i] == 'NA' and c[i] == 'code':
            correctlyFormatted = False
    return codePresent, correctlyFormatted

def reformat(text, classifier):
    # "/u/pythonHelperBot !reformat"
    # Assume that has been called already

    # Also assume bot is only called when reformat is needed
    msgPrefix = "Here's the best I could do:\n\n***\n"
    msgSuffix = """\n\n***\n[^(Code Formatting Help)](https://www.reddit.com/r/learnpython/wiki/faq#wiki_how_do_i_format_code.3F) 
^(|)
[^(README)](https://github.com/CrakeNotSnowman/redditPythonHelper) 
^(|)
[^(FAQ)](https://github.com/CrakeNotSnowman/redditPythonHelper/blob/master/FAQ.md) 
^(|)
^(this bot is written and managed by /u/IAmKindOfCreative) 
"""

    # Classify the lines in the text
    c, rwc = classifyPostLines(text, classifier)
    codePresent, correctlyFormatted = alreadyCorrectlyFormatted(c, rwc)
    sourceText = text.split('\n')
    #print(len(sourceText), len(c), len(rwc))
    assert (len(sourceText) == len(c)) and (len(c) == len(rwc))
    #print(sourceText, c, rwc)

    # Block out/split regions on 'emptyline' class
    # For block, if region is mostly code, add 4 spaces to the start of it
    # Remove leading and trailing "`" as necessary

    newMSG = ""

    msgBlock = []
    i = 0

    changesMade = False
    while i <len(c):
        textBlock = []
        codeLines = 0
        # Classify a block
        if len(c)>0:
            while  i <len(c) and (rwc[i] != 'emptyline'):
                textBlock.append(sourceText[i])
                if rwc[i] == 'code' or c[i] == 'code': 
                    codeLines += 1
                i += 1

        # ID if block was a coding region
        if len(textBlock) > 0:
            if codeLines/float(len(textBlock)) >= 0.5:
                codeRegion = True
            else:
                codeRegion = False


            # Evaluate if the block is missing expected indent
            if codeRegion:
                missingWS = id_Missing_Whitespace(textBlock)

            # Add to the message block with spacer as necessary
            for line in textBlock:
                if codeRegion:
                    spacer = ' '*4
                    msgBlock.append(spacer+line)
                    changesMade = True
                else:
                    msgBlock.append(line)

        msgBlock.append('')
        i += 1
    newMSG = "\n".join(msgBlock)
    msg = msgPrefix + newMSG + msgSuffix
    #logging.info("Code Present: " + str(codePresent) + " | Correctly Formatted" + str(correctlyFormatted))
    return msg, changesMade, codePresent, correctlyFormatted

def loadSummoningHistory(sourcefl):
    submissions = {}
    reformatted = []
    summoners = []

    with open(sourcefl, 'r') as fl:
        for line in fl:
            if line.strip() != "":
                vals = line.strip().split('\t')
                subm = vals[0]
                ref = vals [1]
                summ = vals[3]
                if subm in submissions:
                    submissions[subm] += 1
                else:
                    submissions[subm] = 1
                reformatted.append(ref)
                summoners.append(summ)


    return submissions, reformatted, summoners

def saveSummoningAction(sourcefl,saveLine):
    # Submission ID, Parent Comment ID, Parent Author, Summoning Comment ID, Summoning Author, Summoning Comment Timestamp, summoning comment, Boolean if changes were made, was there code present, was the code correctly formated

    with open(sourcefl, 'a') as fl:
        fl.write(saveLine)
        fl.write('\n')

    return 

def handleSummons(reddit, msg, codeVTextClassifier, quietMode, phbArcPaths, ageLimitHours=4):
    # Add more logging info to see who summoned etc
    # This is the reformat summons

    # Get necessary values:
    # Summoning Comment
    summonDBPath = os.path.join(phbArcPaths['phbActionsDir'], 'summoningHistory.txt')
    if msg.was_comment:
        summoning_comment = archiveAndUpdateReddit.get_comment_by_ID(reddit, comment_id= msg.id)
        if datetime.datetime.utcnow() - summoning_comment.created_utc > datetime.timedelta(hours=ageLimitHours):
            # It was too long ago
            logging.info("Post is older than allowed, "+ str(datetime.datetime.utcnow() - summoning_comment.created_utc))
            #logging.debug("Continuing action for testing")
            #pass
            return

        # Parent comment
        #parentID = 
        parentID = summoning_comment.parent_id.split('_')[-1]
        if summoning_comment.parent_id == summoning_comment.link_id:
            # Parent comment is the post
            parent = archiveAndUpdateReddit.get_submission_by_ID(reddit, submission_id=parentID)
            textBlock = parent.selftext 
        else:
            parent = archiveAndUpdateReddit.get_comment_by_ID(reddit, comment_id=parentID)
            textBlock = parent.body

        if summoning_comment.author == 'pythonHelperBot' or parent.author == 'pythonHelperBot':
            logging.info("Summoned and interacting with self, ignoring.")
            return
            
        # Verify that I haven't already reformated the parent comment 
        #print(parent.id, summoning_comment.id, summoning_comment.created_utc)
        submissions, reformatted, summoners = loadSummoningHistory(summonDBPath)
        if summoning_comment.link_id in submissions:
            if submissions[summoning_comment.link_id] >= 3:
                logging.info("I've commented on this thread too many times, I'm ignoring all other summons")
                return
        if parent.id in reformatted:
            logging.info("I've already reformatted either this comment or the parent, I'm ignoring it")
            return
        if parent.id in summoners:
            logging.info("I've responding to this summoner, and will not reformat the summons")
            return
        if summoning_comment in reformatted:
            logging.info("I've reformatted this summons, I'm not responding to this summons")
            return
        if summoning_comment in summoners:
            logging.info("I've already responded to this summons")
            return
            

        # Attempt to reformat
        if parent.author == summoning_comment.author:
            # Add help formating prefix
            same_user_prefix = """Before I reformat this

            """
        msg, changesMade, codePresent, correctlyFormatted = reformat(textBlock, codeVTextClassifier)

        # Comment below the summoning comment with msg
        #  Only if comment is recent enough

        #quietMode = False # used for testing
        if not quietMode:
            # Save data saying I've commented on it 
            saveLine = str(summoning_comment.link_id) + '\t'
            saveLine += str(parent.id) + '\t' + str(parent.author) + '\t'
            saveLine += str(summoning_comment.id)+ '\t' + str(summoning_comment.author) + '\t' + str(summoning_comment.created_utc) +'\t'+ str(summoning_comment.body.encode('ascii', 'ignore')).strip().replace('\n', ' ') + '\t'
            saveLine += str(changesMade) + '\t'+ str(codePresent) + '\t' + str(correctlyFormatted)

            logging.debug(saveLine)
            if codePresent and changesMade:
                saveSummoningAction(summonDBPath, saveLine)
                archiveAndUpdateReddit.commentOnComment(summoning_comment, msg, reddit, quietMode)
                logging.debug(msg.encode('ascii', 'ignore'))
            else:
                logging.info("Code Present: " +  str(codePresent) + " | Changes Made: " + str(changesMade) + " | Correctly Formatted: "+str(correctlyFormatted))
        else:
            logging.debug("Quiet Mode is active, no reformat comment made.")
            print(msg)

    return


def makeFormatHelpMessage(reddit, msg, quietMode, phbArcPaths):

    # Classify Formatting Issues

    # Build message based on specific issues present

    # Craft General Message to cover other bases


    return