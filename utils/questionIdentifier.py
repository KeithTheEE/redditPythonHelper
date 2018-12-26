import nltk
import time
import datetime
import gzip
import kmlistfi
from random import shuffle
import logging


'''  
Keith Murray 
email: kmurrayis@gmail.com
'''


def parse(path):
    g = gzip.open(path, 'rb')
    for l in g:
        yield eval(l)

def getData(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    #print df[0]
    #return pd.DataFrame.from_dict(df, orient='index')
    return df

def followNLTKStyle(data):
    posts = []
    for i in range(len(data)):
        entry = data[i]
        if entry['questionType'] == 'yes/no':
            posts.append((entry['question'], 'ynQuestion'))
            posts.append((entry['answer'], entry['answerType']+"Answer"))
        else:
            posts.append((entry['question'], 'openQuestion'))
            posts.append((entry['answer'], "openAnswer"))
            
    return posts

def followNLTKStyleSimple(data):
    posts = []
    for i in range(len(data)):
        entry = data[i]
        posts.append((entry['question'], 'Question'))
        posts.append((entry['answer'], "Answer"))
            
    return posts

def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

def classifyString(s, classifier):
    features = dialogue_act_features(s)
    assignment = classifier.classify(features)
    return assignment

def buildClassifier01Amazon(fls):
    #fls = kmlistfi.les("D:/TempDownload/jMcAuleyAmazon/")
    posts = []
    print("Building Classifier\n  Loading Data")
    i = 0
    for fl in fls:
        data = getData(fl)
        posts = posts + followNLTKStyleSimple(data)
        break # Break used during testing, keeps system faster
    shuffle(posts)
    print("  Building Features")
    featureSets = [(dialogue_act_features(post[0]), post[1]) for post in posts]
    size = int(len(featureSets) * 0.1)
    train_set, test_set = featureSets[size:], featureSets[:size]
    print("  Training Model")
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print("  Model Accuracy: ", nltk.classify.accuracy(classifier, test_set))
    return classifier

def buildClassifier02NLTKChat():
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]
    featuresets = [(dialogue_act_features(post.text), post.get('class'))
                for post in posts]
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    logging.debug("NLTK Classifier accuracy:" + str( nltk.classify.accuracy(classifier, test_set)))
    return classifier