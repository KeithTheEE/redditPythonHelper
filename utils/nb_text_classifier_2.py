


import numpy as np
import nltk
import datetime
import logging
import json
import re

import ast
import codeop


from aziraphale.data_handlers import redditData 
from aziraphale.utils import dataSetTools




def mod_judged_posts(reddit_submissions):

    '''
    If a post has been removed by a mod,
    all posts for the previous 6 hours are
    dumped into out_posts on the assumption
    that the mod is active, and has allowed the 
    previous posts to stay up.
    '''
    out_posts = []
    posts_buffer = []
    age_limit_hours = 6
    age_limit = datetime.timedelta(hours=age_limit_hours)
    learning_post_count = 0
    high_vote_post_count = 0

    train = []
    test = []
    in_test = False
    for post in reddit_submissions:
        # Add it to the buffer
        if post.created_utc.year >= 2020:
            if not in_test:
                #print(post.created_utc)
                in_test = True
                train = out_posts[:]
                out_posts = test
        posts_buffer.append(post)
        youngest_post_dt = post.created_utc
        pop_posts = 0
        # Pop old posts
        for i in range(len(posts_buffer)):
            oldest_post_dt = posts_buffer[i].created_utc
            if youngest_post_dt-oldest_post_dt < age_limit:
                break
        posts_buffer = posts_buffer[i:]
        # Check if learning post
        if not isinstance(post.link_flair_text, type(None)):
            if 'removed: Learning' == post.link_flair_text:
                out_posts += posts_buffer
                posts_buffer = []
                learning_post_count += 1
                
    #print(learning_post_count, len(out_posts))
    test = out_posts
    print(len(train), len(test))
    return train, test

def get_k_most_used_words(samples, k=1000, min_allowed_occurance=2):
    '''
    Grab k most used words in the dataset
    Anticipates a list of strings

    '''
    word_c = {}
    for text in samples:
        words = nltk.word_tokenize(text)
        words = [x.lower() for x in words]
        for word in words:
            if word in word_c:
                word_c[word] += 1
            else:
                word_c[word] = 1
    counts = list(word_c.values())
    words = list(word_c.keys())
    large_indicies = np.array(counts).argsort()[-k:][::-1]
    max_words = [words[i] for i in large_indicies]

    return max_words


def rework_sentence(s, allowed_words):
    try:
        t = nltk.word_tokenize(s.lower())
    except TypeError:
        print('Tokenize_error')
        t = s.lower().split()
    pos = nltk.pos_tag(s)
    s_out = []
    for i in range(len(t)):
        word = t[i]
        if word not in allowed_words:
            word = pos[i][1].upper()
        s_out.append(word)
    s_out = ['START'] + s_out + ['END']
    return s_out




def get_word_pair_probability(S, allowed_words, D=None):
    '''
    assumes S is a list of strings
    
    '''
    if isinstance(D, type(None)):
        D = {}
    word_pair_count = 0
    for s in S:
        s = rework_sentence(s, allowed_words)
        word_pair_count += len(s)-1
        for i in range(len(s)-1):
            pre_word = s[i] # prefix
            suf_word = s[i+1] # suffix
            if pre_word in D:
                pre_d = D[pre_word]
                if suf_word in pre_d:
                    pre_d[suf_word] += 1
                else:
                    pre_d[suf_word] = 1
            else:
                D[pre_word] = {suf_word:1}
                
    return D, word_pair_count


def unescape_slash(text):
    ueex = re.compile(r'(\\)(.)')
    #print(ueex.findall(text))
#     out_text = ''
#     i = 0
#     n = len(text)
#     while True:
#         if i >= n:
#             break
#         if text[i] == '\\':
#             i += 1
#         if i < n:
#             out_text += text[i]
#         i += 1
    ex_text = ueex.sub(r'\2',text)
    #if out_text != ex_text:
    #    print('\t>\t', '\n\t>\t'.join(ex_text.split('\n')))
    return ex_text#out_text
        

def astAndCodeopClassifications(line):
    dedent_triggers = ['elif', 'else', 'except']
    dedent_triggers += [x+':' for x in dedent_triggers]
    line=line.strip() # Needed to remove whitespace
    if line.strip() in ['&#x200B;', '']:
        return 'emptyline'
    try:
        ast.parse(line.strip())
        c = 'code'
    except SyntaxError:
        # Possible it's still code, just the opening of a statement
        try:
            comp = codeop.compile_command(line)
            c = 'code' # regardless of comp being none or code object
        except SyntaxError:
            tokens = line.split()
            if tokens[0] in dedent_triggers and line[-1] == ':':
                # Need to manually handle dedent case, kinda hand wavey
                c = 'code'
            else:
                c = 'text'
        except ValueError:
            # Possible output, not sure how it's triggered though
            # https://docs.python.org/3/library/codeop.html#codeop.compile_command
            c = 'text'
        
    return c

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
def classifyPostLines(textBlock, classifier):
    '''
    This classifier is pretty consistenly all or nothing
    A larger code base to train from will help significantly, but is not currently
    a critical requirement 
    '''
    lines = textBlock.split('\n')
    classifications = []
    rwclassifications = []
    astClassifieds = []
    for line in lines:
        line = line.rstrip()
        c = 0#classifier.classify(code_text_features(line))
        classifications.append(c)
        rwc = rewrapClassifications(line)
        astc = astAndCodeopClassifications(line)
        if rwc not in ['code', 'codeblock', 'emptyline'] and astc  != 'code':
            line = worry_about_autolinks_in_code(line)
            if '_LINK_' not in line:
                rwc = rewrapClassifications(line)
                astc = astAndCodeopClassifications(line)
            
        rwclassifications.append(rwc)
        astClassifieds.append(astc)
        #print(c, rwc, line)
        '''
        print('\t>',c, line)
        dist = classifier.prob_classify(code_text_features(line.strip()))
        for label in dist.samples():
            print("\t\t>%s: %f" % (label, dist.prob(label)))
        '''
    return classifications, rwclassifications, astClassifieds  

def remove_code_blocks(text):
    '''
    Strip out all lines of code for the bot to rework 
    as [code block] for the selftext naive bayes classifier

    '''
    
    
    classifier = ''
    code_blocked_text = ''

    # Classify the lines in the text
    c, rwc, astc = classifyPostLines(text, classifier)
    text = text.split('\n')

    line_types = []
    for i in range(len(c)):
        # was just `in ['codeblock']` not `in ['code','codeblock']`
        # Figure out why and make a comment about it, 
        if rwc[i] in ['code','codeblock'] or astc[i] == 'code':
            line_types.append('c')
        elif rwc[i] == 'emptyline':
            if i > 0:
                line_types.append(line_types[-1])
            else:
                line_types.append('t')
        else:
            line_types.append('t')

    cb = False
    for i in range(len(text)):
        if line_types[i] == 'c':
            if cb == False:
                code_blocked_text += '_CODE_\n'
                cb = True
        else:
            code_blocked_text += text[i] + '\n'
            cb = False



    return code_blocked_text


def filter_urls(text):
    # Filter out markdown links
    mdex = re.compile(r'''\[      # Start of possible link 
    ([^\]\n]+)     # text in link
    \]\(   # End braket beginning parenthesis
    (https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))\S*)     # url block
    \)     # End Url Block
    ''', re.VERBOSE)
    text = mdex.sub(r'\1', text)
    urlex = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))\S*')
    text = urlex.sub('_LINK_', text)
    return text

        
def remove_enum(text):
    enex = re.compile(r'[\d](.|:) ')
    return enex.sub('* ', text)
def remove_nospace_character(text):
    nsex = re.compile(r'&#x200B;')
    return nsex.sub('', text)

def worry_about_autolinks_in_code(text):
    return filter_urls(unescape_slash(text))

def hide_inline_code(text):
    icex = re.compile(r'`(.*)`')
    return icex.sub('_INLINECODE_', text)

def preprocess_text(text):
    text = remove_code_blocks(text)
    text = unescape_slash(text)
    text = filter_urls(text)
    text = remove_nospace_character(text)
    text = hide_inline_code(text)
    text = remove_enum(text)
    return text


class Word_Usage_Feature(object):
    '''
    A class that'll handle text between submission classes
    it'll use n grams so it wont be restricted to words or word pairs
    
    Given Bayes Equation is $P(A|w_{i}) = /frac{P(A)P(w_{i}|A)}{P(w_{i})}$
    and Given Naive Bayes ignores the normalization via $P(w_{i}$,
    this returns the summed log probability of the words given a class
    
    '''
    def __init__(self, preprocessor, ngram_size=1):
        assert ngram_size > 0
        assert type(ngram_size) == int
        
        self.k = ngram_size
        self.member_count = 0
        self.D = {}
        
        self.text_preprocessor = preprocessor
        
        # build value for absent ngrams
        missing_ngram_modifier = 10*(10**ngram_size) # If it's not in the dataset, 
                          # it's less than random but not impossible 
                          # the modifier helps keep stuff 'possible'
        self.missing_ngram = (len(self.text_preprocessor.text_max_words)+\
                             self.text_preprocessor.pos_tag_count)**-2 / missing_ngram_modifier
        
    def add_sample(self, text):
        '''
        assuming sents is 
        assumes space character is not a token
        
        '''
        if text.strip() == "":
            return
        sents = self.text_preprocessor.process(text)
        for s in sents:
            for i in range(len(s)-self.k+1):
                token = ' '.join(s[i:i+self.k])
                if token in self.D:
                    self.D[token] += 1
                else:
                    self.D[token] = 1
        self.member_count += 1
        return
    def get_rolling_p(self, text):
        rolling_p = 0
        sents = self.text_preprocessor.process(text)
        any_representative = False
        for s in sents:
            for i in range(len(s)-self.k+1):
                token = ' '.join(s[i:i+self.k])
                if token in self.D:
                    raw_p = self.D[token] / self.member_count
                    rolling_p += np.log(raw_p)
                    any_representative = True
                else:
                    rolling_p += np.log(self.missing_ngram)
        return rolling_p
        
    
        
        
        
class simple_feature(object):
    def __init__(self, D_Map):
        '''
        Dmap is the means to map whatever feature
        is provided in add sample to a keyable
        value that the dictionary can use
        '''
        self.D = {}
        self.d_map = D_Map
        self.member_count = 0

    def add_sample(self, s):
        key = self.d_map[s]
        if key in self.D:
            self.D[key] += 1
        else:
            self.D[key] = 1
        self.member_count += 1
    def get_rolling_p(self, s):
        key = self.d_map[s]
        if key in self.D:
            return np.log(self.D[key])
        else:
            return np.log(1/(self.member_count*100)) # Handles stupid mistakes
        
        

class text_preprocessor(object):
    def __init__(self, selftext=True, title=False):
        self.isselftext = selftext
        self.istitle = title
        self.remove_uncommon_words = True
        self.case_insensative = True
        self.n_common_words = 1000
        self.n_added_key_words = 0
        self.pos_tag_count = 36 # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    def clean_text(self, text):
        text = remove_code_blocks(text)
        text = unescape_slash(text)
        text = filter_urls(text)
        text = remove_nospace_character(text)
        text = hide_inline_code(text)
        text = remove_enum(text)
        return text
    def rework_sentence(self,s):
        tokens_list, pos_list = self.tokenize_text(s)
        s_out = []
        #print(len(tokens_list))
        for sent_index in range(len(tokens_list)):
            tokens = tokens_list[sent_index]
            pos = pos_list[sent_index]
            sent = []
            for i in range(len(tokens)):
                word = tokens[i].lower()
                if word not in self.text_max_words:
                    word = pos[i][1].upper()
                sent.append(word)
            s_out.append(['START'] + sent + ['END'])


        return s_out
    def tokenize_text(self, t):
        tokens = []
        pos = []
        if self.isselftext:
            text = self.clean_text(t)
            lines = text.split('\n')
            sents = []
            for s in lines:
                sents += nltk.sent_tokenize(s)
        elif self.istitle:
            sents = nltk.sent_tokenize(t)
        for sent in sents:
            if len(sent.strip()) > 0:
                token_sent = nltk.word_tokenize(sent)
                part_of_speech = nltk.pos_tag(token_sent)
                if self.case_insensative:
                    token_sent = [t.lower() for t in token_sent]
                tokens.append(token_sent)
                pos.append(part_of_speech)
           
                        
        return tokens, pos
        
    def build(self, texts):
        self.text_word_count = {}
        if self.isselftext:
            self.n_added_key_words += 3
        for text in texts:
            tokens, pos = self.tokenize_text(text)
            sent_count = len(tokens)
            for i in range(sent_count):
                for token in tokens[i]:
                    if token in self.text_word_count:
                        self.text_word_count[token] += 1
                    else:
                        self.text_word_count[token] = 1
        
        
        counts = list(self.text_word_count.values())
        words = list(self.text_word_count.keys())
        n_max_words = self.n_common_words + self.n_added_key_words
        self.text_max_words = [words[i] for i in \
                               np.array(counts).argsort()[-n_max_words:][::-1] \
                              ]

        
    def save(self):
        pass
    def load(self):
        pass
    def process(self, text):
        text = self.rework_sentence(text)
        return text
        
        
def reddit_link_simplifications(url):
    
    link_type = ""
    if 'i.redd.it' in url:
        link_type = 'image'
    elif 'https://www.reddit.com/r/Python/' in url:
        link_type = 'selftext'
    elif '/r/' in url and '/comments/' in url:
        link_type = 'xpost'
    elif 'v.redd.it' in url:
        link_type = 'video'
    else:
        link_type = 'link'
        
    return link_type
    
    

class reddit_submission_class_fields_naivebayes(object):
    '''
    Breaks down and simplifies a class of submissions and builds the  
    features for 
    '''
    def __init__(self, p_of_class, title_preprocessor, selftext_preprocessor):
        self.p_of_class = p_of_class
        self.s =1
        text_ngram = 2
        self.title_word_feat = Word_Usage_Feature(title_preprocessor,ngram_size=text_ngram)
        self.resting_karma = simple_feature(2)
        self.resting_kratio = simple_feature(2)
        self.link_type = simple_feature({'selftext':'selftext', 'link':'link', 'image':'image', 'xpost':'xpost', 'video':'video'})
        self.selftext_word_feat = Word_Usage_Feature(selftext_preprocessor, ngram_size=text_ngram)
        
        
        self.features = {'title':self.title_word_feat,
                         'selftext':self.selftext_word_feat,
                         'linktype':self.link_type}

        
        
    def extract_features(self, submission):
        title = submission.title
        linktype = reddit_link_simplifications(submission.url)
        selftext = submission.selftext
        
        feats = {'title':title,
                 'selftext':selftext,
                 'linktype':linktype}
        return feats 
            
        
    def build_features(self, submissions):
        for submission in submissions:
            feats = self.extract_features(submission)
              
            for key in feats:
                self.features[key].add_sample(feats[key])
                
            
    def get_p_of_submission_in_class(self, submission):
        
        log_p = np.log(self.p_of_class)
        feats = self.extract_features(submission)
        for key in feats:
            log_p += self.features[key].get_rolling_p(feats[key])
        
        
        return log_p
    
             
    
class reddit_submission_classifier(object):
    def __init__(self):
        pass
    def split_classes(self, submissions):
        learning_posts = []
        successful_posts = []
        unclassified_posts = []
        for post in submissions:
            if not isinstance(post.link_flair_text, type(None)):
                if 'removed: Learning' == post.link_flair_text:
                    learning_posts.append(post)
            elif post.score >= 6:
                successful_posts.append(post)

            else:
                unclassified_posts.append(post)
        return learning_posts, successful_posts#, unclassified_posts
        
            
    def mung_submission(self, submission):
        '''
        Handle all the feature adjustment that a post
        needs to be simply handled by the classifier
        '''
        # Adjust to handle 'deleted' and 'removed' messages
        if submission.selftext.strip().lower() in ['[deleted]', '[removed]']:
            try:
                text = submission.edit_History[-1]
                if text.strip() != "":
                    submission.selftext = submission.edit_History[-1]
            except:
                submission.selftext = ""
                
        return submission
        
    def build_classifiers(self, submissions):
        self.feature_set = ['common_word_pair_titles',
                            'common_word_pair_selftext',
                            'post_type']
        submissions = [self.mung_submission(x) for x in submissions]
        titles = [x.title for x in submissions]
        selftext = [x.selftext for x in submissions]
        title_preprocessor = text_preprocessor(selftext=False, title=True)
        selftext_preprocessor = text_preprocessor(selftext=True, title=False)
        title_preprocessor.build(titles)
        selftext_preprocessor.build(selftext)
        
        source_classes = self.split_classes(submissions)
        
        self.classes = []
        for aclass in source_classes:
            class_p = len(aclass)/len(submissions)
            rnb_class = reddit_submission_class_fields_naivebayes(p_of_class=class_p, 
                                                                  title_preprocessor=title_preprocessor, 
                                                                  selftext_preprocessor=selftext_preprocessor)
            rnb_class.build_features(aclass)
            self.classes.append(rnb_class)
            
    def classify_submission(self, submission):
        scores = [x.get_p_of_submission_in_class(submission) for x in self.classes]
        classification = scores.index(max(scores))
        self._scores = scores[:]
        self._score = scores[classification]

        
        # Get top two classes, and see their sepperation 
        s_score = max(scores)
        del(scores[classification])
        second_score = max(scores)
        score_diff = s_score - second_score
        if score_diff != 0:
            s_confidence = (np.log(np.abs(score_diff)))/(-s_score)
        else:
            s_confidence = -1000
        self._confidence = s_confidence

        
        
        return classification
        


def build_reddit_submission_classifier():
    
    handle = redditData.Reddit_Submission_Dataset_Interactions()
    reddit_submissions = dataSetTools.DSIterator(handle)
    train, test = mod_judged_posts(reddit_submissions)
    rsc = reddit_submission_classifier()

    rsc.build_classifiers(train+test)
    return rsc

    
