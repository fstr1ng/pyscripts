#!/usr/bin/python3.6
import sys
import string
import random

passLength = 16 if len(sys.argv) == 1 else int(sys.argv[1])
symbols = string.ascii_letters + string.digits

for i in range(15):
    passwd = [random.choice(symbols) for i in range(passLength)]
    print(''.join(passwd))

