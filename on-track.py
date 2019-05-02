# on-track.py

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from httplib2 import Http

#SCOPES = 'https://www.googleapis.com/auth/calendar'
#store = file.Storage('storage.json')
#creds = store.get()
#if not creds or creds.invalid:
#    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
#    creds = tools.run_flow(flow, store)
#
#CALENDAR = apiclient.discovery.build('calendar', 'v3', http=creds.authorize(Http()))
#GMT_OFF = '-04:00' # EST/GMT-7
#EVENT = {
#    'summary': 'Dinner with friends',
#    'start': {'dateTime': '2019-05-03T19:00:00%s' % GMT_OFF},
#    'end':   {'dateTime': '2019-05-03T22:00:00%s' % GMT_OFF},
#    'attendees': [],
#}
#CALENDAR.events().insert(calendarId='primary', body=EVENT).execute()

# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SCOPES = ['https://www.googleapis.com/auth/calendar']

#def main():
def tenevents():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                #'credentials.json', SCOPES)
                'client_id.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def addevent1():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    #Adds the event
    GMT_OFF = '-04:00' # EST/GMT-7
    EVENT = {
        'summary': 'Dinner with friends',
        'start': {'dateTime': '2019-05-03T19:00:00%s' % GMT_OFF},
        'end':   {'dateTime': '2019-05-03T22:00:00%s' % GMT_OFF},
        'attendees': [],
    }
    service.events().insert(calendarId='primary', body=EVENT).execute()

#if __name__ == '__main__':
#    main()

tenevents()
# [END calendar_quickstart]

#addevent1()