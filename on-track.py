# on-track.py

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CALENDAR = apiclient.discovery.build('calendar', 'v3', http=creds.authorize(Http()))
GMT_OFF = '-04:00' # EST/GMT-7
EVENT = {
    'summary': 'Dinner with friends',
    'start': {'dateTime': '2019-05-03T19:00:00%s' % GMT_OFF},
    'end':   {'dateTime': '2019-05-03T22:00:00%s' % GMT_OFF},
    'attendees': [],
}
CALENDAR.events().insert(calendarId='primary', body=EVENT).execute()