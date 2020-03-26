#!/usr/bin/python3
import random
import string
import sys

line = ''

try:
    count = int(sys.argv[1])
except:
    count = 10

for i in range(count):
    line += random.choice(string.printable[:-6])
print(line)
