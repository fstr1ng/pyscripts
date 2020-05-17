import os
from datetime import datetime

from rich import print
from pyzabbix import ZabbixAPI

login = os.getenv('Z_LOGIN')
password = os.getenv('Z_PASS')
api_url = 'http://' + os.getenv('Z_HOST')

zapi = ZabbixAPI(api_url)
zapi.login(login, password)
print("Connected to Zabbix API Version %s" % zapi.api_version())

def get_problems():
    problems = []
    raw_triggers = zapi.trigger.get(only_true=1,
                                    skipDependent=1,
                                    monitored=1,
                                    active=1,
                                    output='extend',
                                    expandDescription=1,
                                    selectHosts=['host'])
    for t in raw_triggers:
        raw_problems = zapi.problem.get(objectids=t['triggerid'])
        if len(raw_problems) == 1:
            problems.append({'host': t['hosts'][0]['host'],
                             'tier': t['priority'],
                             'time': str(datetime.fromtimestamp(int(t['lastchange']))),
                             'name': t['description'],
                             'data': raw_problems[0]['opdata'],
                             'ack' : bool(int(raw_problems[0]['acknowledged']))
                             })
    return problems   
        

for p in get_problems():
    print(p)
