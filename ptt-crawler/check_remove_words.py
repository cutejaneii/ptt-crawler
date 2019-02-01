# -*- coding: utf-8 -*-

remove_words=[]
text_file = open('remove_words.txt', 'r')
line = text_file.readline()

remove_words.append(line)
while line:
    line = text_file.readline()
    remove_words.append(line.rstrip())

def check_any_remove_words(sentence):
    check=False
    for i in range(1, len(remove_words), 1):
        if (remove_words[i] in sentence):
            if (len(remove_words[i])>0):
                check=True
                break
    return check
