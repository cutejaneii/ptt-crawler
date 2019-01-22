# -*- coding: utf-8 -*-

remove_words=[]
text_file = open('/app/app2/remove_words.txt', 'r')
line = text_file.readline()

remove_words.append(line.decode('utf-8'))
while line:
    line = text_file.readline()
    remove_words.append(line.rstrip().decode('utf-8'))

def check_any_remove_words(sentence):
    check=False
    print('type sentence=')
    print(type(sentence))

    for i in range(1, len(remove_words), 1):
        if (remove_words[i] in sentence):
            if (len(remove_words[i])>0):
                check=True
                break
                print(sentence)
                print(remove_words[i])
    return check
