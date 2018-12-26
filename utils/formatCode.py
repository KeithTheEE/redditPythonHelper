
import nltk
import time
import datetime
import gzip
import kmlistfi
import random
from random import shuffle
import logging




def loadAndShuffleCodeSample(returnSize):
    randomSeed = random.randint(0,1000)
    flsource = "misc/pyProgramTrainingLines.txt"
    with open(flsource,'r') as fl:
        code = fl.readlines()
    random.Random(randomSeed).shuffle(code)
    logging.debug("Random Seed for Code Samples Shuffle: " + str(randomSeed))
    return [(x, 'code') for x in code[:returnSize]]

def lz78(s, D={}):
    '''Almost the LZ78 compression scheme
    '''
    s = s.lower()
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
        i = i+word_len
    return D
            
        
def code_text_features(text):
    d = lz78(text)
    return d

def buildTextCodeClassifier(fls):
    randomSeed = random.randint(0,1000)
    sampleSize = 20000
    # Load code samples
    code = loadAndShuffleCodeSample(returnSize = int(sampleSize/2))
    # Load comment samples
    comments = [(x.text, 'text') for x in nltk.corpus.nps_chat.xml_posts()[:int(sampleSize/2)]]

    posts = code+comments
    random.Random(randomSeed).shuffle(posts)

    logging.debug("Random Seed for Training Shuffle: " + str(randomSeed))
    featureSets=[(code_text_features(post[0]), post[1]) for post in posts]
    size = int(len(featureSets) * 0.1)
    train_set, test_set = featureSets[size:], featureSets[:size]
    print("  Training Model")
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print("  Model Accuracy: ", nltk.classify.accuracy(classifier, test_set))



def classifyLine(s, classifier):
    features = lz78(s)
    assignment = classifier.classify(features)
    return assignment


def classifyLines(textBlock, classifier):
    lines = textBlock.split('\n')
    classifications = []
    for line in lines:
        classified = classifyLine(line, classifier)




def reformat(text):
    "/u/pythonHelperBot !reformat"



'''
Itterate through every py file in a subdirectory
append each line to a sample py file, used as the programming training set
Count the number of lines

'''