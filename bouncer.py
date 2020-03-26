#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bounce log parser and notification sender"""

import smtplib
import json
import os, sys
import pwd, grp

from datetime import datetime, timedelta
from base64 import b64decode
from socket import gethostname
from collections import Counter
from logging.handlers import RotatingFileHandler
from argparse import ArgumentParser, RawDescriptionHelpFormatter

local_conf_path = '/etc/local.conf'
bounce_log_path = '/var/log/exim/bounce/log'
bounce_logs_count = 5
log_file_owner = 'exim'
encodings = ['utf-8', 'cp1251']

smtp_host = 'sprinthost.ru'
smtp_recipient = 'm.fedoseev'

bounce_limit = 0

email_to = f'{smtp_recipient}@{smtp_host}'
email_from = f'bounce@{gethostname()}'
email_subject = f'{gethostname().split(".")[0]}: bounce notification'

bounce_time_format = '%d.%m.%Y %H:%M:%S'
header_time_format = '%a, %d %b %Y %H:%M:%S +0300'


def checkMultipleLogs(path, logs_count):
    """Check if previous logs exist and count bounces in them"""
    log_data = {}
    log_paths = [path]
    for log_number in range(1, logs_count + 1):
        log_paths.append(f'{path}.{log_number}')
    for path in log_paths:
        if os.path.exists(path):
            with open(path, 'r') as log_file:
                log_data[path] = len(log_file.readlines())
    return log_data


def readLogs(path):
    """ Read bounce log and return list of strings"""
    with open(path, 'r') as log_file:
        logs = [log.rstrip() for log in log_file.readlines()]
        return logs


def parseLogs(logs):
    """Parse raw log lines into list of dicts"""
    parsed_logs = []
    for log in raw_logs:
        timestamp, login, body = log.split()
        parsed_log = {}
        parsed_log['time'] = datetime.fromtimestamp(int(timestamp)).strftime(bounce_time_format)
        parsed_log['login'] = login
        for charset in encodings:
            try:
                parsed_log['body'] = b64decode(body).decode(charset)
            except:
                parsed_log['body'] = 'EMAIL DECODE FAILED'
            else: break
        parsed_logs.append(parsed_log)
    return parsed_logs


def filterLogs(parsed_logs, logins_to_filter):
    """Return only first log of every login in logins_to_filter"""
    filtered_logs = []
    filtered_logins = []
    for log in parsed_logs:
        if log['login'] in limit_reached_logins and log['login'] not in filtered_logins:
            filtered_logs.append(log)
            filtered_logins.append(log['login'])
    return filtered_logs


def rotateLogs(path, logs_count, owner):
    bounce_log_rotator = RotatingFileHandler(path,
                                             maxBytes=0,
                                             backupCount=logs_count)
    bounce_log_rotator.doRollover()
    uid = pwd.getpwnam(owner).pw_uid
    gid = grp.getgrnam(owner).gr_gid
    os.chown(path, uid, gid)
    os.chmod(path, 0o600)


def isDedicatediHost():
    """ Check if current host is dedic according to local.conf"""
    with open(local_conf_path, 'r') as conf_file:
        local_conf = json.load(conf_file)
    return local_conf['service'] == 'Dedic'


def isTestingHost():
    return gethostname().split(".")[0].endswith('centos')


def generateNotificationText(logs, counter):
    "Message with bounce metadata and bounced mail examples"
    separator = ('*' * 0) + '\n\n'

    bounce_message = ''
    bounce_message += f'Bounce events total count: {sum(counter.values())}\n\n'
    bounce_message += 'Bounce events by user:\n'

    for item in counter.most_common():
        bounce_message += f'{item[1]}\t{item[0]}\n'

    if any(filtered_logs):
        bounce_message += f'\nBounce limit reached on following accounts:\n'
        for log in filtered_logs:
            bounce_message += log['login'] + ' '

        bounce_message += "\n\n"
        bounce_message += separator

    for log in filtered_logs:
        bounce_message += f"[LOGIN] {log['login']}\n"
        bounce_message += f"[FIRST_EVENT] {log['time']}\n"
        bounce_message += f"[EVENTS_COUNT] {bounce_counter[log['login']]}\n\n"
        bounce_message += log['body']
        bounce_message += "\n\n"
        bounce_message += separator
    return bounce_message


def generateNotificationEmail(headers, body):
    bounce_email = ''
    for header, value in headers.items():
        bounce_email += "%s: %s\n" % (header, value)
    bounce_email += "\n%s\n" % (body)
    return bounce_email


def sendNotificationEmail(smtp_host, smtp_from, smtp_to, email):
    smtp_session = smtplib.SMTP(smtp_host)
    smtp_session.sendmail(smtp_from, smtp_to, email.encode("utf8"))
    smtp_session.quit()


logs_meta_text = ''
if os.path.exists(bounce_log_path):
    logs_meta = checkMultipleLogs(bounce_log_path, bounce_logs_count)
    for log in logs_meta:
        logs_meta_text += f'{log} : {logs_meta[log]} bounce(s)\n'

ap = ArgumentParser(
    description=__doc__,
    epilog=logs_meta_text,
    formatter_class=RawDescriptionHelpFormatter)

arguments_data = [
    (['-s', '--send'  ], {'action': 'store_true', 'help': 'send notification email'}),
    (['-f', '--force' ], {'action': 'store_true', 'help': 'required on dedics / test VMs to send email'}),
    (['-p', '--print' ], {'action': 'store_true', 'help': 'print output to stdout'}),
    (['-r', '--rotate'], {'action': 'store_true', 'help': 'rotate log files'}),
    (['-l', '--log'   ], {'type': int, 'choices': range(1, bounce_logs_count+1), 'help': 'show previous log'})
]

for arg in arguments_data:
    ap.add_argument(*arg[0], **arg[1])

args = (ap.parse_args())

if len(sys.argv) <= 1: 
    ap.print_help()

working_log_path = bounce_log_path
if args.log:
    working_log_path += f'.{args.log}'

raw_logs = readLogs(working_log_path) if os.path.exists(bounce_log_path) else []

notification = ''
limit_reached = False

if len(raw_logs) != 0:
    parsed_logs = parseLogs(raw_logs)
    bounce_counter = Counter([log['login'] for log in parsed_logs])
    limit_reached_logins = [
        log['login'] for log in parsed_logs
        if bounce_counter[log['login']] >= bounce_limit]

    filtered_logs = filterLogs(parsed_logs, limit_reached_logins)
    limit_reached = any(filtered_logs)
    notification = generateNotificationText(filtered_logs, bounce_counter)
else: 
    notification = 'Bounce log is empty'

allowed_to_send = not isDedicatediHost() and not isTestingHost()

if args.send and ((allowed_to_send and limit_reached) or args.force):
    current_time_header = datetime.now().strftime(header_time_format)
    headers = {
        'Content-Type': 'text/plain charset=utf-8',
        'Content-Disposition': 'inline',
        'Content-Transfer-Encoding': '8bit',
        'Date': current_time_header,
        'From': email_from,
        'To': email_to,
        'X-Mailer': 'bounce parser',
        'Subject': email_subject
    }
    email = generateNotificationEmail(headers, notification)
    sendNotificationEmail(smtp_host, email_from, email_to, email)

if args.print:
    print(notification)

if args.rotate and len(raw_logs) != 0:
    rotateLogs(bounce_log_path, bounce_logs_count, log_file_owner)
