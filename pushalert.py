# A script to test the push notification API

import os
import http.client, urllib
from datetime import datetime

APP_TOKEN = os.environ.get('APP_TOKEN')
USER_KEY = os.environ.get('USER_KEY')

conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": APP_TOKEN,
    "user": USER_KEY,
    "timestamp": datetime.now(),
    "message": "It's been a while since we detected any activity!",
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()
print("Sending push notification at {timenow}".format(timenow=datetime.now()))