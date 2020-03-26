import urllib2
import re

contents = urllib2.urlopen("http://inet.from.sh/").read()
ipregex = (r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[^0-9]")

ipstr = re.findall(ipregex, contents)

print(ipstr[0].strip('<'))
