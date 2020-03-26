#!/usr/bin/env python3.7

import smtplib

from email.mime.text import MIMEText
from email.header import Header

subject = 'ação'
payload = 'Body of <b>message</b> КИРИЛЛИЦА ТОЖЕ ТУТ ЕСТЬ, БРО'
msg = MIMEText(payload, 'plain', 'utf-8')
msg['Subject'] = Header(subject, 'utf-8')
print(repr(msg.as_string()))

msg['From'] = 'bounce@hostname'
msg['To'] = 'm.fedoseev@sprinthost.ru'
msg.add_header('Content-Type','text/html')

def send_nudes_please():
    smtpObj = smtplib.SMTP('sprinthost.ru')
    smtpObj.sendmail(msg['From'], [msg['To']], msg.as_string())
    print("Successfully sent email")

for i in range(60):
    send_nudes_please()
    pass
