




'''  
Keith Murray 
email: kmurrayis@gmail.com
'''




def get_learning_sub_Names():
    fl = open('learningSubs.txt', 'r')
    subList = []
    for line in fl:
        line = line.strip()
        if 'r/' in line:
            line = line.split('r/')[-1]
        subList.append(line.lower())
    fl.close()
    return subList
