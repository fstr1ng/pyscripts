#/usr/bin/python3

from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from oauth2client.file import Storage

CLIENT_ID = ''
CLIENT_SECRET = ''

flow = OAuth2WebServerFlow(
          client_id = CLIENT_ID,
          client_secret = CLIENT_SECRET,
          scope = 'https://www.googleapis.com/auth/spreadsheets.readonly',
          redirect_uri = 'http://localhost:8080'
       )

storage = Storage('creds.data')
credentials = tools.run_flow(flow, storage)
print("access_token: %s" % credentials.access_token)
