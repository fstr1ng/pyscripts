import smtplib
import os
import datetime

host = "sprinthost.ru"
sender = "kiska@server"
to = "m.fedoseev@sprinthost.ru"

def send_email( subject, content ):

    for ill in [ "\n", "\r" ]:
        subject = subject.replace(ill, ' ')

    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Disposition': 'inline',
        'Content-Transfer-Encoding': '8bit',
        'From': sender,
        'To': to,
        'X-Mailer': 'python',
        'Subject': subject
    }

    # create the message
    msg = ''
    for key, value in headers.items():
        msg += "%s: %s\n" % (key, value)

    # add contents
    msg += "\n%s\n"  % (content)

    s = smtplib.SMTP(host)

    print ("sending %s to %s" % (subject, headers['To']))
    s.sendmail(headers['From'], headers['To'], msg.encode("utf8"))
    s.quit()

send_email('error [レッドゾーン]', '<b>外国人バカ</b> SAYONARA')
