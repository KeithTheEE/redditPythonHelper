




import numpy as np
import nltk
import datetime
import logging
import json

'''
An early outline of a naive bayes classifier for learning posts
which relies on word pairs to make the classification.

There are better implementations of this classifier, and in the
future the should be reworked to use them instead. None the less
this was the code that satasified the proof of concept, and so as
to not let perfect be the enemy of good, we're rolling with this.
Below is a detailed explaination of what I'm doing so I can return 
to this much later and remember what on earth I did to get these 
results.

The code is divided into three sections plus one

Build Classifier
Save Classifier
Load Classifier

And Classify as the final 'plus one' section



# About this classifier
---------------------
This classifier was built after an attemped to use LDA as a means
to classify learning/question posts as if learning was a topic.
That didn't function. 

The hypothesis is that topic model failed largely because it 
downweighted the key 
elements of a sentence which identify it as a question. 
These features are common parts of speech and word order. 
From there, it's guessed that word order can be measured by 
word pairs, and to reduce the space of all sentences which can be used
only the top k words will be preserved. This ensures the classifier uses
the key features which get downweighted in LDA and LSA models.

The classifier is fairly custom and will need some work to be more generalizable
but that's more or less ok as this is a proof of concept. It's built to expect
two classes, successful, and learning (This is because the bot exists to id learning
posts, all else are unimportant to it). 
It should be added to other naive bayes classifiers to incoperate things like 
p (learning | link[outsite]/link[i.reddit]/selfpost), and so on and so forth 




## Gathering the data
Since around march 2019, the bot has been archiving most of the reddit submissions
the r/python. 

Over all of the posts recorded, the top 1k words used in the titles were recorded.

To build the classifier, there needs to be a set of posts identified as learning, 
and a set of posts identified as 'successful': a hand wavey way to say, 'things
the bot shouldn't interact with'. 
Because there's a bug in the archive, the model for the confusion matrix
outlined in the ROADMAP is a bit difficult to extract. 
(The comments aren't currently easily associated to the submissions)
But the flair: 'removed: Learning' is still a valid measure.

Going off of the removed posts, it's assumed that all posts made 6 hours before the 
post which was later removed by a mod were veiwed by the mods and allowed to stay.
This 6 hour window generates a weak set to draw priors from that defines what is
and is not a learning post. 
From that weak prior posts set, all posts which were removed for learning 
were placed in a list of learning posts. 
All other posts which were not removed and scored above some threshold of karma
(6 in this version) were deemed successful posts. 
This left a set of 'unclassified' posts. 
In the future when the comments are attached to their parent post, this will be
redone to use comments about posting in r/learnpython as further aid in unsupervized
classification. 
(Does crowd sourcing the labeling process mean that the model is supervized? 
Or is it unsupervized because the 'crowd' doesn't know they're labeling the data, 
and I'm not individually validating the labels?
It feels like it's unsupervized to me, we'll go with that until I'm corrected)


## Building the Model 

The model is a naive bayes classifier which uses word pairs to draw the class.
(Future work should look at extending this past word pairs using an LZ dictionary
design or sequitor like structure)
For two reasons, this model restricts the words to the top 1k words used in reddit
submission titles over the past year
(This 1k word list is taken before the learning class list is build, and includes 
posts outside of either the learning post list or the successful post list)
The first reason is to reduce the space of the model: 
    $1k^{2}$ is a lot less than $13k^{2}$
The second reason is to help the model focus on the structure of the sentence over
the content of the sentence, much of which may be unseen previously (new library name) 
while maintaining the possibility of having keywords which help define a post be caught

If a word isn't in the 1k most used set, it's part of speech tag is substitued into
the string in its place (using tokenization by nltk.word_tokenize or space characters). 
The part of speech is determined by the default nltk.pos_tagger, which uses the
penn_treebank pos values. This sets the state space to $1036^{2}$ possible word pairs.

The priors for `learning` and `successful` posts were taken as the size of their lists
over the total number of posts in the weak prior posts list. 
Because both are a subset of the generated weak prior post list, there's a solid 
amount of 'undefined' space (around 70% depending on what the karma threshold is 
set to for the succesfull posts)

The count of word pairs is taken over each class, and the total number of pairs is 
also recorded so the $P(w_{a},w_{b}|Class_{\\alpha})$ can be calculated on demand,
and more easily updated.

## Running the model
With the class' priors known, and the $P(w_{a},w_{b}|Class_{\\alpha})$ being ready to
calculate on demand, a string $S$ is classified by:

Calculating $log(P(Class_{\\alpha}|S))$ for each class by:

 1. Tokenizing the text, (or spliting by spacecharacters if the tokenization runs 
     into an error)
 2. Replacing all tokens not in the approved 'common words' list with their part of
     speech (using `nltk.pos_tag`)
 3. Begin a rolling sum by taking the negative log likelyhood of the class prior
 4. For Each pair of words `a`, `b`, in the sentence:
     Calculate the probability of the word pair in the class by checking:
      * If that pair is in the class model: return the $P(w_{a},w_{b}|Class_{\\alpha})$
      * else: return $\\frac{1}{wordCount^{2}*Modifier}$ Where `wordCount` comes from 
      the total number of common words the model uses plus the part of speech tags, and
     the modifier is used to downweight that word pair to less than random
     but still non-zero probability
    Take the natural log of that value (`np.log()`) to generate the negative log 
    likelyhood and add it to a rolling sum
 5. Return the final sum of the negative log likelyhood

When all (in this case both) classes have had their negative log likelyhood calculated,
return the max of the classes. 

A 'confidence' score is also calculated, though it's fairly hand wavey. 
The score is the natural log of the difference between the two classes 
which can be accessed by `Naive_Bayes_Title_word_pair_classifier.s_confidence`.
The negative log likelyhood score can also be accessed in a similar fashion,
`Naive_Bayes_Title_word_pair_classifier.s_score`. 
These values can be used to guage how confident the classifier is that the
string `S` belongs to one class over another and they will be retained until
the next string is classified. 


'''

def get_k_most_used_words(posts, k=1000):
    '''
    Grab k most used words in the dataset
    Anticipates posts to be a custom class
    with the title feature present

    '''
    word_c = {}
    for post in posts:
        words = nltk.word_tokenize(post.title.lower())
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

def mod_judged_posts(reddit_submissions):

    '''
    If a post has been removed by a mod,
    all posts for the previous 6 hours are
    dumped into out_posts on the assumption
    that the mod is active, and has allowed the 
    previous posts to stay up.

    This creates a weak set of posts to build 
    priors off of.
    '''
    out_posts = []
    posts_buffer = []
    age_limit_hours = 6
    age_limit = datetime.timedelta(hours=age_limit_hours)
    learning_post_count = 0
    high_vote_post_count = 0

    for post in reddit_submissions:
        # Add it to the buffer
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
    return out_posts
        
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

def build_model():
    '''
    Must be run on a computer with aziraphale installed
    and the training data present. Since this is custom code
    it's not expected to work on other machines, but the 
    results of this build are saved under 'misc/title_classifier.json'
    and the load function should work. 
    '''
    from aziraphale.data_handlers import redditData 
    from aziraphale.utils import dataSetTools

    handle = redditData.Reddit_Submission_Dataset_Interactions()
    reddit_submissions = dataSetTools.DSIterator(handle)

    # Get common words to keep bot from treating a post
    #  with language it's never seen before as if it were as
    #  common as can be
    max_words = get_k_most_used_words(reddit_submissions, k=1000)

    # Grab only posts which were made while a mod was active
    weak_prior_posts = mod_judged_posts(reddit_submissions)

    # From weak prior posts organize it into successful,
    #  learning, and other--unclassified
    learning_posts = []
    successful_posts = []
    unclassified_posts = []
    for post in weak_prior_posts:
        if not isinstance(post.link_flair_text, type(None)):
            if 'removed: Learning' == post.link_flair_text:
                learning_posts.append(post)
        elif post.score >= 6:
            successful_posts.append(post)
            
        else:
            unclassified_posts.append(post)
    
    learning_prior = len(learning_posts)/len(weak_prior_posts)
    successful_prior = len(successful_posts)/len(weak_prior_posts)

    learning_S = [post.title for post in learning_posts]
    successful_S = [post.title for post in successful_posts]

    learning_word_pairs, learning_pair_count = \
        get_word_pair_probability(learning_S, max_words)
    successful_word_pairs, successful_pair_count = \
        get_word_pair_probability(successful_S, max_words)


    return max_words, learning_prior, successful_prior, \
            learning_word_pairs, learning_pair_count, \
            successful_word_pairs, successful_pair_count


def build_selftext_model():
    '''
    Must be run on a computer with aziraphale installed
    and the training data present. Since this is custom code
    it's not expected to work on other machines, but the 
    results of this build are saved under 'misc/title_classifier.json'
    and the load function should work. 
    '''
    from aziraphale.data_handlers import redditData 
    from aziraphale.utils import dataSetTools

    handle = redditData.Reddit_Submission_Dataset_Interactions()
    reddit_submissions = dataSetTools.DSIterator(handle)

    # Get common words to keep bot from treating a post
    #  with language it's never seen before as if it were as
    #  common as can be
    max_words = get_k_most_used_words(reddit_submissions, k=1000)

    # Grab only posts which were made while a mod was active
    weak_prior_posts = mod_judged_posts(reddit_submissions)

    # From weak prior posts organize it into successful,
    #  learning, and other--unclassified
    learning_posts = []
    successful_posts = []
    unclassified_posts = []
    for post in weak_prior_posts:
        if not isinstance(post.link_flair_text, type(None)):
            if 'removed: Learning' == post.link_flair_text:
                learning_posts.append(post)
        elif post.score >= 6:
            successful_posts.append(post)
            
        else:
            unclassified_posts.append(post)
    
    learning_prior = len(learning_posts)/len(weak_prior_posts)
    successful_prior = len(successful_posts)/len(weak_prior_posts)

    learning_S = [post.title for post in learning_posts]
    successful_S = [post.title for post in successful_posts]

    learning_word_pairs, learning_pair_count = \
        get_word_pair_probability(learning_S, max_words)
    successful_word_pairs, successful_pair_count = \
        get_word_pair_probability(successful_S, max_words)


    return max_words, learning_prior, successful_prior, \
            learning_word_pairs, learning_pair_count, \
            successful_word_pairs, successful_pair_count


class Neg_Log_likehood_Word_Pairs(object):
    '''
    This classifier is a weak implementation of a naive bayes classifier
    which focuses on the pairs of words used in strings to draw the 
    classification. To help ensure the struture of the strings are what 
    the classifier is using, words which do not appear frequently are 
    replaced with their part of speech. 
    '''
    def __init__(self, class_prior, word_pair_dict, word_pair_count, allowed_words): 
        self._clas_prior = class_prior
        self._word_pair_dict = word_pair_dict
        self._word_pair_count = word_pair_count
        self._allowed_words = allowed_words
        self._allowed_word_count = len(self._allowed_words)
        self._set_missing_word_pair_prob()
    def _set_missing_word_pair_prob(self, pos_tag_count=36, modifier=1000):
        # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        # If it's not in the dataset, it's less than random but not impossible 
        # the modifier helps keep stuff possible
        self._absent_word_pair_prob = (self._allowed_word_count+pos_tag_count)**-2 / modifier

    def neg_log_likelyhood_of_Class_given_words(self, s):
        rolling_p = np.log(self._clas_prior)
        s = rework_sentence(s, self._allowed_words)
        self.any_rep = False # Val indicates if any word pair was in the class database
        for i in range(len(s)-1):
            pre_word = s[i] # prefix
            suf_word = s[i+1] # suffix
            p, pair_present = self._get_word_pair_prob(pre_word, suf_word)
            if pair_present:
                self.any_rep = True
            rolling_p += np.log(p)
    #     if not any_rep:
    #         print("Nothing to go off of")
        #print('-',rolling_p)
        return rolling_p

    def _get_word_pair_prob(self, a,b):
        D = self._word_pair_dict
        pair_count = -1
        rep_present = False
        if a in D:
            if b in D[a]:
                pair_count = D[a][b]
                rep_present = True
                #print(a,b)
        if pair_count == -1:
            p = self._absent_word_pair_prob
            #print(p)
        else:
            p = pair_count/ self._word_pair_count
            #print(p)
            
        #print(p)
        return p, rep_present


class Naive_Bayes_Title_word_pair_classifier(object):
    '''
    This is written to have two classes, hard coded,
    one is a learning post, class 0, and one is a 
    successful post class, class 1
    '''
    def __init__(self):
        flpath = 'misc/title_classifier.json'
        logging.debug("Loading model from "+flpath)
        self.load(flname = flpath)
    def build(self):
        max_words, learning_prior, successful_prior, \
            learning_word_pairs, learning_pair_count, \
            successful_word_pairs, successful_pair_count = build_model()
        self.allowed_words = max_words
        self._classifiers = [Neg_Log_likehood_Word_Pairs(
                class_prior = learning_prior,
                word_pair_dict = learning_word_pairs,
                word_pair_count = learning_pair_count,
                allowed_words = self.allowed_words
            ),
            Neg_Log_likehood_Word_Pairs(
                class_prior = successful_prior,
                word_pair_dict = successful_word_pairs,
                word_pair_count = successful_pair_count,
                allowed_words = self.allowed_words
            )
        ]

    def classify_string(self, s):
        neg_log_likely = [x.neg_log_likelyhood_of_Class_given_words(s) for x in self._classifiers]
        self._s_scores = neg_log_likely[:]
        s_class = neg_log_likely.index(max(neg_log_likely)) # Will choose class a in a tie between [a, b] (left most class)
        s_score = max(neg_log_likely)
        # Grab two highest classes (since there's only two it doesn't matter)
        #  And build confidence value
        del(neg_log_likely[s_class])
        second_score = max(neg_log_likely)
        score_diff = s_score - second_score
        if score_diff != 0:
            s_confidence = np.log(np.abs(score_diff))
        else:
            s_confidence = -1000

        # set string vals to be called on later if needed
        self.s_class = s_class
        self.s_score = s_score
        self.s_confidence = s_confidence
        return s_class




    def export(self, ofl_name = 'misc/title_classifier.json', mode='json'):
        vals = build_model()
        with open(ofl_name, 'w') as f:
            json.dump(vals, f)
        pass

    def load(self, flname = 'misc/title_classifier.json'):
        with open(flname) as json_file:
            
            max_words, learning_prior, successful_prior, \
                learning_word_pairs, learning_pair_count, \
                successful_word_pairs, successful_pair_count  = json.load(json_file)

        self.allowed_words = max_words
        self._classifiers = [Neg_Log_likehood_Word_Pairs(
                class_prior = learning_prior,
                word_pair_dict = learning_word_pairs,
                word_pair_count = learning_pair_count,
                allowed_words = self.allowed_words
            ),
            Neg_Log_likehood_Word_Pairs(
                class_prior = successful_prior,
                word_pair_dict = successful_word_pairs,
                word_pair_count = successful_pair_count,
                allowed_words = self.allowed_words
            )
        ]
