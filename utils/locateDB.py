
import os
import logging

'''  
Keith Murray 
email: kmurrayis@gmail.com
'''

def check_through_these():
    
    amazonQuestionDBSources = ["D:/TempDownload/jMcAuleyAmazon/", "nowhere", "Also/nowhere"]
    englishLangDBSourcess = ["C:/Users/kmurr/Documents/filesForProgramming/reddit/GutTop100Books/", 
                            'D:/Databases/GutTop100Books',
                             '/home/pi/Documents/filesForProgramming/Reddit/GutTop100Books',
                             '/media/keith/hdd01/Databases/GutTop100Books']
    codeForCodeAndText = ['misc/pyProgramTrainingLines.txt']

    check_here = {
        "amazonQ":amazonQuestionDBSources,
        "englishDB":englishLangDBSourcess,
        "codeText":codeForCodeAndText
    }

    return check_here


def check_for_file(paths):
    '''
    Given a set of possible locations for data and databases:
    check to find one that exists, and adjust the path
    folder dilimiters according to OS needs
    '''
    for path in paths:
        if os.path.isdir(os.path.normpath(path)) or os.path.exists(os.path.normpath(path)):
            return os.path.normpath(path)
    return False



def get_db_file_locations():

    paths = {}
    
    check_here = check_through_these()
    for key in check_here:
        path = check_for_file(check_here[key])
        paths[key] = path
        if not path:
            logging.warning( "Unable to locate files associated with " + str(key))
            logging.warning( "\tSearched in:\n  -" + '\n  - '.join(check_here[key]))

    #amazonQuestionDBSources = ["D:/TempDownload/jMcAuleyAmazon/"]
    #englishLangDBSourcess = ["C:/Users/kmurr/Documents/filesForProgramming/reddit/GutTop100Books/"]

    #paths["amazonQ"] = check_for_file(amazonQuestionDBSources, is_file=False)
    #paths["englishDB"] = check_for_file(englishLangDBSourcess, is_file=False)

    return paths
