1. Sign up for Google API (if not yet): https://console.developers.google.com/
   1. Create Project & Enable API
   2. Credentials -> Create new Client ID
   3. Type: "Other", authorized/redirect = "http://localhost:8080" (may be ommitted)
```
       client_id = Client ID
       client_secret = Client Secret
```
   4. Credentials -> Create new Service Account
```
       private_p12 = path to downloaded *.p12
```
2. Fill oauth.py with client_id,client_secret. Run in cli, follow instructions.
3. Fill data in data.json (user == Last name).
4. Run calc.py.
