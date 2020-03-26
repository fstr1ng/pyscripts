import requests
import textwrap
import shutil 
from shutil import get_terminal_size as terminal_size

from bs4 import BeautifulSoup

bashURL = 'https://bash.im/random'

def downloadHTML():
    html = requests.get(bashURL).text
    soup = BeautifulSoup(html, "html.parser")
    return [tag for tag in soup('div','quote') if len(tag['class'])==1]

def makeQuotes(elements):
    quotes = []
    for element in elements:
        id = element.find(class_='id').get_text()
        date = element.find(class_='date').get_text()
        text = [string for string in element.find(class_='text').strings]
        quotes.append({'id':id,'date':date, 'text':text})
    return quotes

def formatQuote(quote):
    maxLength = terminal_size()[0]-3 if not terminal_size()[0] >= 160 else 160
    info = 'Цитата: {}, {}'.format(quote['id'], quote['date'])
    text = ''
    for line in quote['text']:
        if len(line)>=maxLength:
            line = textwrap.fill(line, maxLength, subsequent_indent = '| ')
        text += ('| ' + line + '\n')
    return ('| ' + info + '\n' + text)

def run():
    print('Скачиваем текст...')
    quotes = makeQuotes(downloadHTML())

    print('Enter для вывода новой цитаты, любой другой символ для выхода.')
    print()

    while True:
        try:
            print(formatQuote(quotes.pop()))
            if input() != '':
                break
        except:
            print('Цитаты закончились, загрузить еще? Enter для еще новой цитаты, любой другой символ для выхода.')
            print()
            if input() != '':
                break
            else:
                print('Скачиваем текст...')
                quotes = makeQuotes(downloadHTML())

run()
exit()
