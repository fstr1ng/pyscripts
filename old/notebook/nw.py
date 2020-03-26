#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function # Удобный принт из третьего питона
import sys # Для получения аргументов коммандной строки
import os  # Для получения путей к файлам блокнотов и настроек
import cPickle as rick # Для сериализации блокнотов
from datetime import datetime as dt # Для тaйм-стампа

# Информация о программе

prName = 'Mnote'
ver = '0.1'
author = 'Mikef'
i = '''
#  nw.py
#  
#  Copyright 2017 Mikef <admin@killrot.ru>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
'''


# Узнаем пути
settings = {'lastFile':'book', 'mode':'unpickled'}
#print(os.path.abspath(os.path.dirname(sys.argv[0])))
filePath = sys.path[0] + '/books/' + settings.get('lastFile')
#print(filePath)

# Загрузка настроек
#with open('./config.ini', 'rb') as config:
#	settings = { 
#			'lastFile': config.readlines()[0],
#		     	'mode'    : config.readlines()[1]
#		   }


# Если в sys.argv один аргумент, выводим содержимое (первый аргумент - имя файла скрипта)

if len(sys.argv) == 1:
	with open('books/'+ settings.get('lastFile') , 'rb') as file:
		for line in file.readlines():
			print(line, end='')
		exit()



#######################
### Проверка ключей ###
#######################

# Flush - очистить блокнот
if   sys.argv[1] == '-f':
	with open('books/'+ settings.get('lastFile'), 'wb') as file:
		file.write('')
		print('Notebook flushed!')

# Version - узнать версию программы
elif sys.argv[1] == '-v':
	print('{0} {1} by {2}'.format(prName, ver, author))
	print(i)

# Delete last - удалить последнюю запись
elif sys.argv[1] == '-dl':
	output = ''
	with open ('books/'+ settings.get('lastFile'), 'rb+') as file:
		for line in file.readlines():
			output += ' '.join (line)
		file.write(output[:-1] + '\n')
		print('Line deleted!')

# Ключей нет - добавляем строку
else:	
	output = str(dt.now())[:19] + ' | '
	with open('books/'+ settings.get('lastFile'), 'ab') as file:
		output += ' '.join (sys.argv[1:])
		file.write(output + '\n')
		print('Note added!')

