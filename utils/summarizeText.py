

import nltk
nltk.data.path.append('/home/pi/nltk_data')
from nltk.corpus import stopwords
#from nltk.tokenize.moses import MosesDetokenizer 
# # Deprecated due to licensing issues 
#https://github.com/nltk/nltk/issues/2000
from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer

import datetime
import time
import math
import numpy as np
from numpy.linalg import inv
import scipy as sp
import codecs
import re
import networkx as nx


from utils import lsalib2 as lsalib
import kmlistfi


'''  
Keith Murray 
email: kmurrayis@gmail.com
'''

def stripURL(text):
    return re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text, flags=re.MULTILINE)

def parseStringSimple01(text, removeStopWords=False, removeURL=True):
    """
    Cleans text input by removing unicode characters that
    don't directly map to ascii and lowering text

    Parameters
    ----------
    text : string
        String of text
    removeStopWords : boolean
        Boolean Value set to False. If true removes stopwords
    removeURL : boolean
        Boolean Value set to True. If True removes url like strings from text
    Returns
    -------
    cleanText : list
        list of strings that has unicode characters removed and cases lowered.
        Optionally also removed are URLs (by default) and stopwords (Not by default)
    """

    # NLTK (in py 2.7) doesn't tokenize unicode afaik
    text = re.sub(r'[^\x00-\x7F]+',' ', text).lower()
    if removeURL:
        text = stripURL(text)
    cleanText = nltk.word_tokenize(text)
    if removeStopWords:
        stop_words = set(stopwords.words('english'))
        cleanText = [w.lower() for w in cleanText if not w in stop_words]
    return cleanText
    

def detokenize(token_text):
    # CHANGE 

    # CHANGE
    #detokenizer = MosesDetokenizer()
    #return detokenizer.detokenize(token_text, return_str=True)
    detokenizer = TreebankWordDetokenizer()
    return detokenizer.detokenize(token_text)

    
def tokenTextToDict(text):
    """
    Prepares input text for use in latent semantic analysis by shifting it from 
    a list to a dictionary data structure
    Parameters
    ----------
    text : list of strings
        A list of strings where each string is a word and the list is a document
    Returns
    -------
    wordD : dictionary
        A dictionary structure where the key is a word, and the item is the word count
    """
    wordD = {}
    for word in text:
        if word in wordD:
            wordD[word] += 1
        else:
            wordD[word] = 1
    return wordD

def buildModelFromDocsInFolder(sourceDataPath, k=12, gutenberg=True):
    """
    Build a term doc matrix and reduce it's dimensionality based on the 
    input fileset.
    Parameters
    ----------
    sourceDataPath : string
        String file path to the folder containing the training dataset
        Files in this path must be text files. 
        Each file is treated as a unique document
    k : int
        Default of 12, k is the dimension the factorization will reduce to
    Returns
    -------
    tdm : termDocMatrix class object
        A termDocMatrix object from lsalib that has been reduced and has P and Q 
        factorized matrices ready for use, trained on the input document corpus
    Other Parameters
    ----------------
    gutenberg : Boolean
        A boolean flag indicating if the text files are from gutenberg, where the start 
        and end of the doc need to be trimmed 
    Notes
    -----
    Still figuring this out, docs likely will change
    References
    ----------
    Examples
    --------
    """

    docSetFolder = kmlistfi.les(sourceDataPath)
    print(len(docSetFolder))
    tdm = lsalib.termDocMatrix()
    for docFl in docSetFolder:
        docName = docFl.split('/')[-1]
        docName = docName[:-4]
        document = open(docFl, 'r')
        text = document.read()
        document.close()
        text = parseStringSimple01(text, removeStopWords=True)
        if gutenberg == True:
            text = text[500:-500]
        if len(text) > 1:
            tdm.add(text, docName)
    
    # All docs are added, time to adjust matrix and reduce dimensionality
    tdm.weight_idf()
    P, Q = tdm.nmf(k)

    return tdm


# ~~~~~~~~~~ Summarization Method 01 ~~~~~~~~~~ #
# Basic IDF
def sentScore_IDF(sent, tdm):
    """
    Score a single sentence by its average Inverse Document Frequency value of the 
    words in the sentence with stopwords removed
    Parameters
    ----------
    sent : string
        a sentences from the source document
    tdm : termDocMatrix object
        the trained term document matrix object that has gone through matrix factorization
    Returns
    -------
    AvgScore : float
        The n sentence summary of the document 
    Notes
    -----
    

    References
    ----------
    Examples
    --------
    """
    sent = parseStringSimple01(sent, removeStopWords=True)
    score = 0.
    for word in sent:
        if word in tdm.terms:
            index = tdm.terms.index(word)
            score += tdm.idfs[index]
            #score += np.linalg.norm(tdm.P[index])*tdm.idfs[index]
    AvgScore = score / float(len(sent))
        
    return AvgScore
def summarizeDoc_IDF(text, tdm, topSentCount=3):
    """
    Returns n sentences that summarize the document according the the average
    inverse document frequency score of the words in that sentence. 
    Parameters
    ----------
    text : string
        The string of the original document to be summarized
    tdm : termDocMatrix object
        the trained term document matrix object that has gone through matrix factorization
    topSentCount : int
    Returns
    -------
    Summary : string
        The n sentence summary of the document 
    Notes
    -----
    The average idf per word is a naive way to measure the information of the sentence
    While in truth this yields a poor summary, this simple method may provide useful
    other information the document contains, and can be used as a secondary summary

    TODO
    ----
    In what may become its own summarization function,
    Calculate the idf score given the previous top ranking idf sentence,
    that way unique to the corpus but repetitive sentences don't get shown and we can 
    maximize the information in the summary

    References
    ----------
    Examples
    --------
    """
    
    
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    sents = nltk.sent_tokenize(text)
    scores = []
    for sent in sents:
        score = sentScore_IDF(sent, tdm)
        scores.append(score)
        #print score
    
    # I should be able to bind this with sents and just return the top 3 sents but...
    indexSet = sorted(range(len(scores)), key=lambda i: scores[i])[-topSentCount:]
    print(indexSet)
    summarized = ""
    for i in range(len(sents)):
        if i in indexSet:
            #print i
            summarized = summarized + " " + sents[i]
    
    return summarized






# ~~~~~~~~~~ Summarization Method 02 ~~~~~~~~~~ #
# Document vs sentence profile comparison 
def profileMap(query, basis):
    return sp.spatial.distance.cdist(query, basis, 'correlation')


def mapDictToProfile(wordD, tdm):
    """
    Take the document in as a dictionary with word:wordcount format, and map
    it to a p profile
    Parameters
    ----------
    wordD : Dictionary
        Dictionary where the keys are words, and the values are the corrosponding word
        count
    tdm : termDocMatrix object
        The trained and factorized term-document matrix structure
    Returns
    -------
    p : numpy array
        The mapped vector profile for the string 
    Notes
    -----
    References
    ----------
    Examples
    --------
    """
    p = np.zeros(len(tdm.terms))
    tfweight = float(sum(wordD.values()))
    for i in range(len(tdm.terms)):
        if tdm.terms[i] in wordD:
            p[i] = wordD[tdm.terms[i]]/tfweight
    #print len(p)
    p = np.multiply(tdm.idfs, p).transpose()
    return p

def profileString(text, tdm):
    # Build projection matrix
    x = np.mat(tdm.P)
    y = np.dot(tdm.P, tdm.Q.T)
    B = np.dot(inv(np.dot(x.T, x)),x.T)
    
    # Build Profile    
    words = parseStringSimple01(text, removeStopWords=True)
    wordD = tokenTextToDict(words)
    p = mapDictToProfile(wordD, tdm)
    
    # Project P onto Document set
    kp = np.dot(B, p)
    
    return kp
    
def summarizeDoc_SentToDoc(text, tdm, topSentCount=3):
    # clean text for NLTK
    
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    
    kBasis = profileString(text, tdm)
    
    #topSentCount = 3
    
    sents = nltk.sent_tokenize(text)
    sentProjections = False
    #print sents
    for sent in sents:
        kp = profileString(sent, tdm)
        if type(sentProjections) == bool:
            sentProjections = kp
        else:
            sentProjections = np.concatenate((sentProjections, kp))
        #sentProjections.append(kp)
        #print score
    #sentProjections = np.append(sentProjections, axis=0)
    
    #print len(sentProjections)
    scores = profileMap(sentProjections, kBasis)
    # Needed to address sents without words in the term-doc matrix
    # Such as empty strings found by the nltk sent_tokenizer
    scores = np.nan_to_num(scores)
    
    indexSet = sorted(range(len(scores)), key=lambda i: scores[i])[-topSentCount:]
    #for i in range(len(scores)):
    #    print i, scores[i]
    print(indexSet)
    
    
    summarized = ""
    for i in range(len(sents)):
        if i in indexSet:
            #print i
            #print sents[i]
            summarized = summarized + " " + sents[i]
    
    return summarized





# ~~~~~~~~~~ Summarization Method 03 ~~~~~~~~~~ #
# TextRank 



# *********** KEYWORD EXTRACTION *************** #
#  ~~~~~~~ Text Rank Keyword Method 01 ~~~~~~~~~ #
    

def rank_graph(G):
    g = nx.Graph(G)
    calculated_page_rank = nx.pagerank(g, weight='weight')
    sorted_x = sorted(calculated_page_rank.items(), key=lambda x: x[1])
    return sorted_x[::-1]

def wordRankKeywords(text):
    '''
    Follow the wordrank algorithm presented in TextRank paper in 2004



    Notes
    -----
    Different POS taggers will impact the accuracy of the result
    as does the scope of types of nounds and adjetives used
    '''


    # Section 3.1: TextRank for Keyword Extraction
    window = 2
    noun_set = ['NN', 'NNP', 'NNS', 'NNPS', 'PRP']#, 'PRP$'] 
    adj_set = ['JJ', 'JJR', 'JJS', ]
    noun_adj_Filter = noun_set + adj_set
    keyWordTheshold = 1./3.
    
    
    # Tokenize and Annotate
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    joined_tagged_sentences = []
    for sent in tagged_sentences:
        # Adjust casing to uniformly lower case
        #  Has to be done after POS tagging for effective tags
        sent = [(i.lower(), j) for i, j in sent]
        joined_tagged_sentences += sent
    #print joined_tagged_sentences
    
    # Syntactic Filter
    # Using 
    syntactic_Filter = noun_adj_Filter
    textGraph = {}
    for i in range(len(joined_tagged_sentences)-window):
        pos_pair = joined_tagged_sentences[i]
        if pos_pair[1] in syntactic_Filter:
            for j in range(window):
                downstream_pos_pair = joined_tagged_sentences[i+j]
                if downstream_pos_pair[1] in syntactic_Filter:
                    # Maybe lemma-ize these too
                    prefix_word = pos_pair[0].lower()
                    suffix_word = downstream_pos_pair[0].lower()
                    if prefix_word in textGraph:
                        if suffix_word not in textGraph[prefix_word]:
                            textGraph[prefix_word].append(suffix_word)
                    else:
                        textGraph[prefix_word] = [suffix_word]
                        
                  
    # Make graph undirected
    keySet = list(textGraph.keys())
    for key in keySet:
        for item in textGraph[key]:
            if item in textGraph:
                if key not in textGraph[item]:
                    textGraph[item].append(key)
            else:
                textGraph[item] = [key]
    
    # Rank the graph
    sorted_words = rank_graph(textGraph)
    just_words = [i[0] for i in sorted_words]

    #print just_words
    
    
    # Post Processing
    limit = int(keyWordTheshold*len(just_words))
    canidates = just_words[:limit+1]
    #canidates = canidates[:3]
    #print canidates


    full_phrase_set = []
    i = 0
    phrase = ""
    while True:
        if i >= len(joined_tagged_sentences):
            break
        word = joined_tagged_sentences[i][0]
        word_tag = joined_tagged_sentences[i][1]
        if  word_tag in syntactic_Filter:
            phrase += " " + word
        else:
            if phrase != "":
                phrase = phrase.strip()
                inCanidate = False
                for word in phrase.split():
                    if word in canidates:
                        inCanidate = True
                if (phrase not in full_phrase_set) and inCanidate:
                    full_phrase_set.append(phrase)
            phrase = ""
        i += 1
    
    final_phrases = []
    #print full_phrase_set
    for word in canidates:
        #print word
        final_phrases += [phrase for phrase in full_phrase_set if word in phrase.lower().split() and phrase not in final_phrases]
        #print '>', final_phrases
        if len(final_phrases) >= limit:
            break



    
    
    #print sorted_words
    #print keyword_phrases
    #print full_phrase_set
    #print final_phrases
    #print canidates
    return final_phrases

#  ~~~~~~~~~~ Keyword Method 02 ~~~~~~~~~~~~~~~~ #


def getTF(text):
    text = nltk.word_tokenize(text)
    tf = {}
    termCount = float(len(text))
    for word in text:
        word = word.lower()
        if word in tf:
            tf[word]+=1
        else:
            tf[word]=1
    for key in tf:
        tf[key] = float(tf[key])/termCount
    return tf
        

def extract_Keywords_and_IDF(text, tdm):
    # Section 3.1: TextRank for Keyword Extraction
    window = 2
    noun_set = ['NN', 'NNP', 'NNS', 'NNPS', 'PRP', 'PRP$']
    adj_set = ['JJ', 'JJR', 'JJS', ]
    noun_adj_Filter = noun_set + adj_set
    keyWordTheshold = 1./3.
    
    
    # Tokenize and Annotate
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    tf = getTF(text)
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    joined_tagged_sentences = []
    for sent in tagged_sentences:
        joined_tagged_sentences += sent
    #print joined_tagged_sentences
    
    # Syntactic Filter
    # Using 
    syntactic_Filter = noun_adj_Filter
    textGraph = {}
    for i in range(len(joined_tagged_sentences)-window):
        pos_pair = joined_tagged_sentences[i]
        if pos_pair[1] in syntactic_Filter:
            for j in range(window):
                downstream_pos_pair = joined_tagged_sentences[i+j]
                if downstream_pos_pair[1] in syntactic_Filter:
                    # Maybe lemma-ize these too
                    prefix_word = pos_pair[0].lower()
                    suffix_word = downstream_pos_pair[0].lower()
                    if prefix_word in textGraph:
                        if suffix_word not in textGraph[prefix_word]:
                            textGraph[prefix_word].append(suffix_word)
                    else:
                        textGraph[prefix_word] = [suffix_word]
                        
                  
    # Make graph undirected
    keySet = list(textGraph.keys())
    for key in keySet:
        for item in textGraph[key]:
            if item in textGraph:
                if key not in textGraph[item]:
                    textGraph[item].append(key)
            else:
                textGraph[item] = [key]
    
    # Rank the graph
    sorted_words = rank_graph(textGraph)
    adjusted_scores = []
    for word_score_pair in sorted_words:
        word = word_score_pair[0]
        score = word_score_pair[1]
        if word in tdm.terms:
            index = tdm.terms.index(word)
            idf_Val = tdm.idfs[index]
        else:
            idf_Val = math.log((tdm.docCount)/1.)
        newScore = score*idf_Val*tf[word.lower()]
        #print newScore
        adjusted_scores.append((word, newScore))
    sorted_words = sorted(adjusted_scores, key=lambda x: x[1])[::-1]
    #print sorted_words
        
        
    just_words = [i[0] for i in sorted_words]
    
    
    
    # Post Processing
    canidates = just_words[:int(keyWordTheshold*len(just_words))+1]
    #print '>', canidates
    i = 0
    keyword_phrases = []
    phrase = ""
    while True:
        if i >= len(joined_tagged_sentences):
            break
        word = joined_tagged_sentences[i][0]
        if word in canidates:
            phrase += " " + word
        else:
            if phrase != "":
                phrase = phrase.strip()
                if phrase not in keyword_phrases:
                    keyword_phrases.append(phrase)
            phrase = ""
        i += 1
    
    
    #print sorted_words
    return keyword_phrases