



'''
TinyFile Bug:
    every new dictionary has a '[' ahead of it instead of a comma

Large File Bug:
    Either
        Multiple ']' at the end of the file
    Or
        Missing trailing ']'
'''

import json


import os

def fix_improper_restart_bug(text):
    '''
    Occasionally the json will append the file
    as if it's a new json file, }[\\n rather than
    },\\n

    So this will simple replace it 
    '''
    text = text.split('}[\n')
    text = '},\n'.join(text)
    return text

def fix_trailing_brackets_bug(text):
    '''
    Some of the files get multiple ']' tacked onto 
    the end of them, when they just need one closing bracket

    So we'll strip them out and try to tack one on
    '''
    while text.rstrip()[-2:] == '\n]':
        text = text[:-2]

    if text.rstrip()[-1] != ']':
        text += '\n]'
    return text


def fix_reddit_json_bug(filepath):
    with open(filepath, 'r') as ifl:
        text = ifl.read()
    text = fix_improper_restart_bug(text)
    text = fix_trailing_brackets_bug(text)
    text_struct = json.loads(text)


    return

    