#!/usr/bin/python3.6

# Импортируем библиотеки
import pickle
import random
import os
import sys

# Стандартные параметры
mode = "capitalize"
oneline = False
wordCount = 1

### HELP ###
############
helpLine='''Format:
kso [count] -[l|u] -[o]
Aruments:
count (integer): amount of words
-l: lower case
-u: upper case
-o: one line
-h|--help: show this message and exit\n'''
############
### HELP ###

# Проверям аргументы командной строки

for arg in sys.argv[1:]:
    if   arg == "-l":
        mode = "lower"
    elif arg == "-u":
        mode = "upper"
    elif arg == "-o":
        oneline = True
    elif arg in ['-h', '--help', 'help']:
        print(helpLine)
        exit()
    else:
        try:
            wordCount = int(arg)
        except Exception as e:
            print("Invalid arguments!")
            exit()

# Узнаем, где находится скрипт
dirname = os.path.dirname(os.path.realpath(__file__))

# Открываем файл с ругательствами, анпиклим список
with open(dirname + '/stop', 'rb') as file:
    wordList = pickle.load(file)
# Формируем список слов
wordOuputList = []

for i in range(wordCount):
    word = random.choice(wordList).capitalize()
    if mode == "lower":
        word = word.lower()
    elif mode == "upper":
        word = word.upper()
    wordOuputList.append(word)

# Выводим гадости
*words, lastWord = wordOuputList

if oneline == True:
    end = ' '
else:
    end = '\n'

for word in words:
    print(word, end=end)
print(lastWord)
