# on-track.py

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from httplib2 import Http
import PySimpleGUI as sg

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

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



def addnewevent(summary_text, start_time, end_time, attendees, custom_event_id):
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

    #Adds the event
    EVENT = {
        'summary': summary_text,
        'start': start_time,
        'end':   end_time,
        'attendees': attendees,
        'id': custom_event_id,
    }
    service.events().insert(calendarId='primary', body=EVENT).execute()



def deleteevent(custom_event_id):
    creds = None
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

    #Deletes the event
    service.events().delete(calendarId='primary', eventId=custom_event_id).execute()



def getevent(custom_event_id):
    creds = None
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

    #Gets and prints the event
    event = service.events().get(calendarId='primary', eventId=custom_event_id).execute()
    print(event['summary'])



def updateevent(custom_event_id, new_summary_text, new_start_time, new_end_time, new_attendees):
    creds = None
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

    #Gets and updates the event parameters
    event = service.events().get(calendarId='primary', eventId=custom_event_id).execute()

    event['summary'] = new_summary_text
    event['start'] = new_start_time
    event['end'] = new_end_time
    event['attendees'] = new_attendees
    #event['id'] = new_event_id

    service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()



GMT_OFF = '-04:00'

summary_test = 'Dinner with friends'
start_time_test = {'dateTime': '2019-05-03T11:00:00%s' % GMT_OFF}
end_time_test = {'dateTime': '2019-05-03T12:00:00%s' % GMT_OFF}
attendees_test = []
event_id_test = 'so20190503110000dinner1511it1'

update_summary_test = 'Dinner with some friends'
update_start_time_test = {'dateTime': '2019-05-03T12:00:00%s' % GMT_OFF}
update_end_time_test = {'dateTime': '2019-05-03T13:00:00%s' % GMT_OFF}
update_attendees_test = []
update_event_id_test = 'so20190503120000dinner1511it'

#addnewevent(summary_test, start_time_test, end_time_test, attendees_test, event_id_test)
#deleteevent(event_id_test)
#getevent(event_id_test)

#updateevent(event_id_test, update_summary_test, update_start_time_test, update_end_time_test, update_attendees_test)



# PySimpleGUI Code
def initial_window_test():

    sg.ChangeLookAndFeel('GreenTan')

    form = sg.FlexForm('On Track', default_element_size=(40, 1))

    column1 = [[sg.Text('Column 1', background_color='#d3dfda', justification='center', size=(10,1))],
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]
    layout = [
        [sg.Text('All graphic widgets in one form!', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Here is some text.... and a place to enter text')],
        [sg.InputText('This is my text')],
        [sg.Checkbox('My first checkbox!'), sg.Checkbox('My second checkbox!', default=True)],
        [sg.Radio('My first Radio!     ', "RADIO1", default=True), sg.Radio('My second Radio!', "RADIO1")],
        [sg.Multiline(default_text='This is the default Text should you decide not to type anything', size=(35, 3)),
         sg.Multiline(default_text='A second multi-line', size=(35, 3))],
        [sg.InputCombo(('Combobox 1', 'Combobox 2'), size=(20, 3)),
         sg.Slider(range=(1, 100), orientation='h', size=(34, 20), default_value=85)],
        [sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3)),
         sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=25),
         sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=75),
         sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=10),
         sg.Column(column1, background_color='#d3dfda')],
        [sg.Text('_'  * 80)],
        [sg.Text('Choose A Folder', size=(35, 1))],
        [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
         sg.InputText('Default Folder'), sg.FolderBrowse()],
        [sg.Submit(), sg.Cancel()]
         ]

    button, values = form.Layout(layout).Read()
    sg.Popup(button, values)

def initial_window():

    sg.ChangeLookAndFeel('GreenTan')

    form = sg.FlexForm('On Track', default_element_size=(10, 3))

    column1 = [
        [sg.Text('School', size=(5, 1), font=("Helvetica", 25))],
        [sg.Multiline(default_text='Test list item\nSecond line', disabled=True, size=(30, 3))],
        [sg.Button('Add New Assignment', key='add_assignment', button_color=('white', '#001480'))],
        [sg.Button('Manage Current Assignments', key='manage_assignments', button_color=('white', '#001480'))]
    ]
    column2 = [
        [sg.Text('Jobs', size=(5, 1), font=("Helvetica", 25))],
        [sg.Multiline(default_text='Test list item\nSecond line', disabled=True, size=(30, 3))],
        [sg.Button('Add New Job Application', key='add_job', button_color=('white', '#001480'))],
        [sg.Button('Manage Current Job Applications', key='manage_applications', button_color=('white', '#001480'))]
    ]
    column3 = [
        [sg.Text('Social', size=(5, 1), font=("Helvetica", 25))],
        [sg.Multiline(default_text='Test list item\nSecond line', disabled=True, size=(30, 3))],
        [sg.Button('Add New Event', key='add_event', button_color=('white', '#001480'))],
        [sg.Button('Manage Current Events', key='manage_events', button_color=('white', '#001480'))]
    ]

    layout = [
        [sg.Button('Notification Settings', key='notifications', button_color=('white', '#001480'))],
        [sg.Column(column1, background_color='#d3dfda'),
        sg.Column(column2, background_color='#d3dfda'),
        sg.Column(column3, background_color='#d3dfda')
        ]
    ]

    button, values = form.Layout(layout).Read()
    sg.Popup(button, values)

#initial_window_test()
initial_window()