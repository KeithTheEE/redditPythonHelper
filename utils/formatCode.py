
import nltk
import time
import datetime
import gzip
import kmlistfi
import random
from random import shuffle
import logging
from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer
from nltk.corpus import brown
from nltk.metrics import ConfusionMatrix



'''
Keith Murray
email: kmurrayis@gmail.com

Markdown Parsers and other Useful Links
http://piumarta.com/software/peg/
https://github.com/jgm/peg-markdown/blob/master/markdown_parser.leg




'''



'''
Itterate through every py file in a subdirectory
append each line to a sample py file, used as the programming training set
Count the number of lines

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
    return d

def buildTextCodeClassifier(sourceDataPath):
    
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
    size = int(len(featureSets) * 0.1)
    train_set, test_set = featureSets[size:], featureSets[:size]
    logging.debug("Training Size: " + str( len(train_set)))
    logging.debug("Testing Size:  " + str( len(test_set)))
    logging.debug("  Training Model")
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    logging.debug("  Model Accuracy: " + str(nltk.classify.accuracy(classifier, test_set)))
    ref = []
    tagged = []
    '''
    for i in range(len(test_set)):
        c = classifier.classify(test_set[i][0])
        tagged.append(c)
        ref.append(test_set[i][1])
        if i < 5:
            #print("Text:\n", test_set[i][0])
            print("Classified: ", c)
            print("Actually:   ", test_set[i][1])
    '''
    # I can't get the confusion matrix to work in a saved format. 
    #logging.debug(str(ConfusionMatrix(ref, tagged)))
    return classifier#, train_set, test_set




def rewrapClassifications(line):
    '''
    This is a by hand curriated list of markdown circumstances which 
    define code blocks.
    
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

def classifyPostLines(textBlock, classifier):
    lines = textBlock.split('\n')
    classifications = []
    rwclassifications = []
    for line in lines:
        c = classifier.classify(code_text_features(line))
        classifications.append(c)
        rwc = rewrapClassifications(line)
        rwclassifications.append(rwc)
        print(c, rwc, line)
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
    msgSuffix = """\n\n***\n[^(CODE FORMATTING HELP)](https://www.reddit.com/r/learnpython/wiki/faq#wiki_how_do_i_format_code.3F) 
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
        while (rwc[i] != 'emptyline') and i <len(c):
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
    return msg, changesMade, codePresent, correctlyFormatted
