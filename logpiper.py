#!/usr/bin/env python3
import sys
import operator
from datetime import datetime

logs = []
extra_logs = {}

for line in sys.stdin:
    log = {}
    line_split = line.rstrip().split(maxsplit=3)
    try:
        time = f"{line_split[0].split('[')[1]} {line_split[1][:-1]}"
        log['time'] = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        log['type'] = line_split[2][:-1]
        log['data'] = line_split[3]
        logs.append(log)
    except:
        pass

sorted_logs = sorted(logs, key=lambda log: log['time'])

for i, log in enumerate(sorted_logs):
    print(f"{i} {log['time']} {log['type']} {log['data']}")

