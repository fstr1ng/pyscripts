# Script can executed by any wsgi-server, like so:
# gunicorn -b 0.0.0.0:6534 uwsgi:application

def application(env, start_response):
    with open('testwsgi.txt', 'rb') as content_file:
        content = content_file.read()
    start_response('200 OK', [('Content-Type','text/html')])
    return [content] # content must be a bytes sequence
