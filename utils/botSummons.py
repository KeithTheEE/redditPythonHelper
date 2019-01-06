


def summonCommands():
    '''
    Returns a list of accepted commands for bot actions
    Currently just reformat, however should later include "Helpme"
    to trigger bot auto answer 
    '''
    return ['reformat']


def checkForSummons(msg):
    summonID = None
    if msg.subject.strip() == "username mention":
        if (msg.body.strip() == 'u/pythonHelperBot !reformat') or (msg.body.strip() == '/u/pythonHelperBot !reformat'):
            print("SUMMONS")
            print(msg.id)
            summonID = msg.id
        print(msg.body)
    
    return summonID
