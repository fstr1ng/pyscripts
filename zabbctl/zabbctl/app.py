import getpass
import os

import click
from tabulate import tabulate
from pyzabbix import ZabbixAPI

login = os.getenv('Z_LOGIN')
password = os.getenv('Z_PASS')
api_url = 'http://' + os.getenv('Z_HOST')

zapi = ZabbixAPI(api_url)
zapi.login(login, password)
print("Connected to Zabbix API Version %s" % zapi.api_version())

@click.group()
def cli():
    pass

@cli.command()
def hosts():
    for h in zapi.host.get(output="extend"):
        print(h)

@cli.command()
def triggers():
    triggers = zapi.trigger.get(only_true=1,
    skipDependent=1,
    monitored=1,
    active=1,
    output='extend',
    expandDescription=1,
    withUnacknowledgedEvents=1,
    selectHosts=['host'],
    )
    
    triggers_table = []

    for t in triggers:
        host = t['hosts'][0]['host']
        description = t['description']
        value = t['value']
        trigger_row = [host, description, value]
        triggers_table.append(trigger_row)
    
    print(tabulate(triggers_table, tablefmt='simple'))

if __name__ == '__main__':
    cli()

