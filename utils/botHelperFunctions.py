




'''  
Keith Murray 
email: kmurrayis@gmail.com
'''




def get_learning_sub_Names():
    fl = open('misc/learningSubs.txt', 'r')
    subList = []
    for line in fl:
        line = line.strip()
        if 'r/' in line:
            line = line.split('r/')[-1]
        subList.append(line.lower())
    fl.close()
    return subList

def load_autoreply_key_phrases(fl_path):
    fl = open('misc/autoreplyKeyPhrases.txt', 'r')
    phrase_set = []
    for line in fl:
        line = line.strip()
        if line != "":
            phrase_set.append(line.lower())
    fl.close()
    return phrase_set

def shortenRedditURL(url):
    url = url[8:]
    return '/'.join(url.split('/')[:-2])+'/'


def coolPlacesToDonate():
    donationList = []
    # Load websites, randomly suggest one as a good place to donate too
    return

def ramCheck():
    # Return used and available ram for logging 
    return