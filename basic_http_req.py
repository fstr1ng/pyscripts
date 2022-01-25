import http.client

host = "test38148.ru" 
uri = "/test.php" 
content_type = "text/html" 
method = "GET" 
UA = "test script" 

c = http.client.HTTPConnection(host)
headers = {"Content-Type": content_type,
           "Accept": "text/plain",
           "User-Agent": UA}
c.request(method, uri, {}, headers)
r = c.getresponse()
print(r.read())
