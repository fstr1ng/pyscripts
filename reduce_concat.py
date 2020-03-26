#!/usr/bin/python3.8
import functools
import itertools

fruits = 'apple banana kiwi orange peach grape pineapple cherry potato'.split()

# Вспомогательная функция для конкатенации строк
concatenator = lambda x, y: f'{x} + {y}'
# Свертывает список строк ['Abc', 'def', 'ghi'] в 'Abc, def, ghi'
biz = functools.reduce(concatenator, fruits)
# print(biz)

