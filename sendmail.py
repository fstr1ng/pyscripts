#!/usr/bin/env python3.7

import smtplib
import email.message

msg = email.message.Message()
msg['Subject'] = 'HTML TEST'
msg['From'] = 'bounce@hostname'
msg['To'] = 'm.fedoseev@sprinthost.ru'
msg.add_header('Content-Type','text/html')
msg.set_payload('Body of <b>message</b>')

try:
   smtpObj = smtplib.SMTP('sprinthost.ru')
   smtpObj.sendmail(msg['From'], [msg['To']], msg.as_string())
   print("Successfully sent email")
except:
   print("Error: unable to send email")

