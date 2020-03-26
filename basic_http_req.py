import http.client

HOST = "test38148.ru" 
URI = "/test.php" 
CTYPE = "olo/lololo" 
METHOD = "GET" 
UA = "ololo JDatabaseDriverMysqlip" 

h = http.client.HTTPConnection(HOST)
headers = {"Content-Type": CTYPE,
           "Accept": "text/plain",
           "User-Agent": UA}
h.request(METHOD, URI, {}, headers)
r = h.getresponse()
print(r.read())
