#!/usr/bin/python3

import subprocess

import rlcompleter, readline
readline.parse_and_bind('tab: complete')

while True:
    request = input('сегодня мы с тобой хуизим: ')
    if request == 'q':
        quit()
    else:
        subprocess.call(["whois", request])

