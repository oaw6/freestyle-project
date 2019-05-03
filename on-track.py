# on-track.py

from __future__ import print_function
import datetime
from datetime import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from httplib2 import Http
import PySimpleGUI as sg
import pandas
import csv
import os
import requests
import sys


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
#initial_school_list = ''
#initial_job_list = ''
#initial_social_list = ''

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



def writeeventtocsv(event_type, event_id, summary_text, start_time, end_time, attendees):
    #Reads the csv file and converts the data to a list of dictionaries
    if event_type == 'school':
        chosen_file_path = os.path.join(os.path.dirname(__file__), "data", "eventlist.csv")
    elif event_type == 'job':
        chosen_file_path = os.path.join(os.path.dirname(__file__), "data", "applicationlist.csv")
    elif event_type == 'social':
        chosen_file_path = os.path.join(os.path.dirname(__file__), "data", "sociallist.csv")
    event_list = []
    with open(chosen_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            event_list.append(dict(row))
    
    #Adds new event to list of dictionaries, converts back to csv and overwrites data file
    #event_list.append({"id":event_id, "summary":summary_text, "start":start_time, "end":end_time, "attendees":attendees})
    if event_type == 'school':
        event_list.append({"id":event_id, "summary":summary_text, "start":start_time, "end":end_time, "attendees":attendees})
    elif event_type == 'job':
        event_list.append({"id":event_id, "summary":summary_text, "start":start_time, "end":end_time, "url":attendees})
    elif event_type == 'social':
        event_list.append({"id":event_id, "summary":summary_text, "start":start_time, "end":end_time, "attendees":attendees})
    
    event_id_list = []
    event_summary_list = []
    event_start_list = []
    event_end_list = []
    event_attendees_list = []
    event_active_list = []
    for rowitem in event_list:
        event_id_list.append(rowitem["id"])
        event_summary_list.append(rowitem["summary"])
        event_start_list.append(rowitem["start"])
        event_end_list.append(rowitem["end"])
        if event_type == 'job':
            event_attendees_list.append(rowitem["url"])
        else:
            event_attendees_list.append(rowitem["attendees"])
        event_active_list.append('active')
    if event_type == 'job':
        pandas_data = pandas.DataFrame({'id':event_id_list,'summary':event_summary_list, 'start': event_start_list,'end': event_end_list,'url': event_attendees_list, 'active': event_active_list})
        pandas_data.to_csv('./data/applicationlist.csv')
    else:
        pandas_data = pandas.DataFrame({'id':event_id_list,'summary':event_summary_list, 'start': event_start_list,'end': event_end_list,'attendees': event_attendees_list, 'active': event_active_list})
        if event_type == 'school':
            pandas_data.to_csv('./data/eventlist.csv')
        else:
            pandas_data.to_csv('./data/sociallist.csv')



def createeventid(type, end_time, summary_ten):
    new_event_id = ''
    if type == 'school':
        new_event_id = new_event_id + 'sc'
    new_event_id = new_event_id + end_time[:4] + end_time[5:7] + end_time[8:10] + end_time[11:13] + end_time[14:16] + end_time[17:19]
    unrefined_summary = summary_ten.lower()
    summ_ten = unrefined_summary.replace('w', '11')
    summ_ten = summ_ten.replace('x', '12')
    summ_ten = summ_ten.replace('y', '13')
    summ_ten = summ_ten.replace('z', '14')
    summ_ten = summ_ten.replace(' ', '15')
    new_event_id = new_event_id + summ_ten
    return new_event_id



GMT_OFF = '-04:00'

summary_test = 'Dinner with friends'
start_time_test = {'dateTime': '2019-05-03T15:30:00%s' % GMT_OFF}
end_time_test = {'dateTime': '2019-05-03T16:00:00%s' % GMT_OFF}
attendees_test = []
event_id_test = 'so20190503153000dinner1511it'

update_summary_test = 'Dinner with some friends'
update_start_time_test = {'dateTime': '2019-05-03T12:00:00%s' % GMT_OFF}
update_end_time_test = {'dateTime': '2019-05-03T13:00:00%s' % GMT_OFF}
update_attendees_test = []
update_event_id_test = 'so20190503120000dinner1511it'

#addnewevent(summary_test, start_time_test, end_time_test, attendees_test, event_id_test)
#deleteevent(event_id_test)
#getevent(event_id_test)

#updateevent(event_id_test, update_summary_test, update_start_time_test, update_end_time_test, update_attendees_test)
#writeeventtocsv(event_id_test, summary_test, start_time_test, end_time_test, attendees_test)


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
    
    #Reads next 15 calendar events, then filters/feeds them into lists
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=15, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    page_type = 'initial'
    if page_type == 'initial':
        #Runs this for the initial window
        school_list = ''
        job_list = ''
        social_list = ''
        if not events:
            school_list = 'No upcoming events'
            job_list = 'No upcoming events'
            school_list = 'No upcoming events'
        for event in events:
            if event['id'].startswith('sc'):
                school_list = school_list + "\n" + event['summary'] + "\n" + event['start'].get('dateTime', event['start'].get('date'))
            elif event['id'].startswith('jo'):
                job_list = job_list + "\n" + event['summary'] + "\n" + event['start'].get('dateTime', event['start'].get('date'))
            elif event['id'].startswith('so'):
                social_list = social_list + "\n" + event['summary'] + "\n" + event['start'].get('dateTime', event['start'].get('date'))
        if school_list == '':
            school_list = 'No upcoming events'
        if job_list == '':
            job_list = 'No upcoming events'
        if social_list == '':
            social_list = 'No upcoming events'
        initial_school_list = school_list
        initial_job_list = job_list
        initial_social_list = social_list
    
    sg.ChangeLookAndFeel('GreenTan')

    form = sg.FlexForm('On Track', default_element_size=(10, 3))

    column1 = [
        [sg.Text('School', size=(5, 1), font=("Helvetica", 25))],
        [sg.Multiline(default_text=initial_school_list, disabled=True, size=(30, 10))],
        [sg.Button('Add New Assignment', key='add_assignment', button_color=('white', '#001480'))],
        [sg.Button('Manage Current Assignments', key='manage_assignments', button_color=('white', '#001480'))]
    ]
    column2 = [
        [sg.Text('Jobs', size=(5, 1), font=("Helvetica", 25))],
        [sg.Multiline(default_text=initial_job_list, disabled=True, size=(30, 10))],
        [sg.Button('Add New Job Application', key='add_job', button_color=('white', '#001480'))],
        [sg.Button('Manage Current Job Applications', key='manage_applications', button_color=('white', '#001480'))]
    ]
    column3 = [
        [sg.Text('Social', size=(5, 1), font=("Helvetica", 25))],
        [sg.Multiline(default_text=initial_social_list, disabled=True, size=(30, 10))],
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
    #sg.Popup(button, values)

    if button == 'add_assignment':
        add_assignment()



def add_assignment():
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
    
    # Creates input window for the new event
    
    sg.ChangeLookAndFeel('GreenTan')

    form = sg.FlexForm('On Track', default_element_size=(10, 3))

    layout = [
        [sg.Button('Notification Settings', key='notifications', button_color=('white', '#001480'))],
        [sg.Text('Input New Assignment Information', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Assignment Title')],
        [sg.InputText('', size=(30, 2))],
        [sg.Text('Due Date (yyyy-mm-dd)'), sg.Text('Time Assignment is due (hh:mm:ss)')],
        [sg.InputText('', size=(20, 2)), sg.InputText('', size=(20, 2))],
        [sg.Text('Group Members (emails, separate by commas)')],
        [sg.InputText('', size=(60, 3))],
        [sg.Checkbox('Are there sub-assignments?', default=False)],
        [sg.Submit(), sg.Cancel()]
    ]

    button, values = form.Layout(layout).Read()
    #sg.Popup(button, values)

    if button == 'Submit':
        event_summary = values[0] + " due at " + values[2]
        end_time = values[2]
        if int(end_time[3:5]) >= 15:
            start_adjust = int(end_time[3:5]) - 15
        else:
            start_adjust = int(end_time[3:5]) + 45
            if int(end_time[:2]) >= 1:
                hour_adjust = int(end_time[:2]) - 1
                if hour_adjust <= 9:
                    hour_string = '0' + str(hour_adjust)
                else:
                    hour_string = str(hour_adjust)
            else:
                hour_string = str(23)
        formatted_start_string = values[1] + 'T' + hour_string + ':' + str(start_adjust) + end_time[5:] + '%s'
        event_start = {'dateTime': formatted_start_string % GMT_OFF}
        formatted_end_string = values[1] + 'T' + values[2] + '%s'
        event_end = {'dateTime': formatted_end_string % GMT_OFF}
        event_attendees = values[3]
        if not event_attendees:
            event_attendees = []
        elif event_attendees == '':
            event_attendees = []
        full_summary = values[0]
        if len(full_summary) >= 10:
            summaryten = full_summary[:11]
        else:
            summary_length = int(len(full_summary)) + 1
            summaryten = full_summary[:summary_length]
        event_id = createeventid('school', formatted_end_string, summaryten)
        #print(event_summary, event_start, event_end, event_attendees, event_id)

        addnewevent(event_summary, event_start, event_end, event_attendees, event_id)
        writeeventtocsv('school', event_id, event_summary, event_start, event_end, event_attendees)

        if values[4] == True:
            sub_assignment(event_id)



def sub_assignment(linked_event_id):
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
    
    # Creates input window for the new event
    
    sg.ChangeLookAndFeel('GreenTan')

    form = sg.FlexForm('On Track', default_element_size=(10, 3))

    layout = [
        [sg.Button('Notification Settings', key='notifications', button_color=('white', '#001480'))],
        [sg.Text('Input Sub-Assignment Information', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Sub-Assignment Title')],
        [sg.InputText('', size=(30, 2))],
        [sg.Text('Due Date (yyyy-mm-dd)'), sg.Text('Time Assignment is due (hh:mm:ss)')],
        [sg.InputText('', size=(20, 2)), sg.InputText('', size=(20, 2))],
        [sg.Text('Group Members (emails, separate by commas)')],
        [sg.InputText('', size=(60, 3))],
        [sg.Checkbox('Are there more sub-assignments?', default=False)],
        [sg.Submit(), sg.Cancel()]
    ]

    button, values = form.Layout(layout).Read()
    #sg.Popup(button, values)

    if button == 'Submit':
        event_summary = values[0] + " due at " + values[2]
        end_time = values[2]
        if int(end_time[3:5]) >= 15:
            start_adjust = int(end_time[3:5]) - 15
        else:
            start_adjust = int(end_time[3:5]) + 45
            if int(end_time[:2]) >= 1:
                hour_adjust = int(end_time[:2]) - 1
                if hour_adjust <= 9:
                    hour_string = '0' + str(hour_adjust)
                else:
                    hour_string = str(hour_adjust)
            else:
                hour_string = str(23)
        formatted_start_string = values[1] + 'T' + hour_string + ':' + str(start_adjust) + end_time[5:] + '%s'
        event_start = {'dateTime': formatted_start_string % GMT_OFF}
        formatted_end_string = values[1] + 'T' + values[2] + '%s'
        event_end = {'dateTime': formatted_end_string % GMT_OFF}
        event_attendees = values[3]
        if not event_attendees:
            event_attendees = []
        elif event_attendees == '':
            event_attendees = []
        full_summary = values[0]
        if len(full_summary) >= 10:
            summaryten = full_summary[:11]
        else:
            summary_length = int(len(full_summary)) + 1
            summaryten = full_summary[:summary_length]
        event_id = createeventid('school', formatted_end_string, summaryten)
        #print(event_summary, event_start, event_end, event_attendees, event_id)
        linked_event = linked_event_id

        addnewevent(event_summary, event_start, event_end, event_attendees, event_id)
        writeeventtocsv('school', event_id, event_summary, event_start, event_end, event_attendees)

        if values[4] == True:
            sub_assignment(linked_event_id)



def add_job_application():
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
    
    # Creates input window for the new event
    
    sg.ChangeLookAndFeel('GreenTan')

    form = sg.FlexForm('On Track', default_element_size=(10, 3))

    layout = [
        [sg.Button('Notification Settings', key='notifications', button_color=('white', '#001480'))],
        [sg.Text('Input New Job Application Information', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Application Title')],
        [sg.InputText('', size=(30, 2))],
        [sg.Text('Due Date (yyyy-mm-dd)'), sg.Text('Time Application is due (hh:mm:ss)')],
        [sg.InputText('', size=(20, 2)), sg.InputText('', size=(20, 2))],
        [sg.Text('Application url (if applicable)')],
        [sg.InputText('', size=(60, 3))],
        [sg.Checkbox('Do you have to do anything before the due date?', default=False)],
        [sg.Submit(), sg.Cancel()]
    ]

    button, values = form.Layout(layout).Read()
    #sg.Popup(button, values)

    if button == 'Submit':
        event_summary = values[0] + " due at " + values[2]
        end_time = values[2]
        if int(end_time[3:5]) >= 15:
            start_adjust = int(end_time[3:5]) - 15
        else:
            start_adjust = int(end_time[3:5]) + 45
            if int(end_time[:2]) >= 1:
                hour_adjust = int(end_time[:2]) - 1
                if hour_adjust <= 9:
                    hour_string = '0' + str(hour_adjust)
                else:
                    hour_string = str(hour_adjust)
            else:
                hour_string = str(23)
        formatted_start_string = values[1] + 'T' + hour_string + ':' + str(start_adjust) + end_time[5:] + '%s'
        event_start = {'dateTime': formatted_start_string % GMT_OFF}
        formatted_end_string = values[1] + 'T' + values[2] + '%s'
        event_end = {'dateTime': formatted_end_string % GMT_OFF}
        event_attendees = values[3]
        if not event_attendees:
            event_attendees = ''
        full_summary = values[0]
        if len(full_summary) >= 10:
            summaryten = full_summary[:11]
        else:
            summary_length = int(len(full_summary)) + 1
            summaryten = full_summary[:summary_length]
        event_id = createeventid('job', formatted_end_string, summaryten)
        #print(event_summary, event_start, event_end, event_attendees, event_id)

        addnewevent(event_summary, event_start, event_end, event_attendees, event_id)
        writeeventtocsv('job', event_id, event_summary, event_start, event_end, event_attendees)

        if values[4] == True:
            job_sub_assignment(event_id)



def job_sub_assignment(linked_event_id):
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
    
    # Creates input window for the new event
    
    sg.ChangeLookAndFeel('GreenTan')

    form = sg.FlexForm('On Track', default_element_size=(10, 3))

    layout = [
        [sg.Button('Notification Settings', key='notifications', button_color=('white', '#001480'))],
        [sg.Text('Input Sub-Assignment Information', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Sub-Assignment Title')],
        [sg.InputText('', size=(30, 2))],
        [sg.Text('Due Date (yyyy-mm-dd)'), sg.Text('Time Sub-Assignment is due (hh:mm:ss)')],
        [sg.InputText('', size=(20, 2)), sg.InputText('', size=(20, 2))],
        [sg.Text('Sub-Assignment url (if applicable)')],
        [sg.InputText('', size=(60, 3))],
        [sg.Checkbox('Do you have to do anything else before the due date?', default=False)],
        [sg.Submit(), sg.Cancel()]
    ]

    button, values = form.Layout(layout).Read()
    #sg.Popup(button, values)

    if button == 'Submit':
        event_summary = values[0] + " due at " + values[2]
        end_time = values[2]
        if int(end_time[3:5]) >= 15:
            start_adjust = int(end_time[3:5]) - 15
        else:
            start_adjust = int(end_time[3:5]) + 45
            if int(end_time[:2]) >= 1:
                hour_adjust = int(end_time[:2]) - 1
                if hour_adjust <= 9:
                    hour_string = '0' + str(hour_adjust)
                else:
                    hour_string = str(hour_adjust)
            else:
                hour_string = str(23)
        formatted_start_string = values[1] + 'T' + hour_string + ':' + str(start_adjust) + end_time[5:] + '%s'
        event_start = {'dateTime': formatted_start_string % GMT_OFF}
        formatted_end_string = values[1] + 'T' + values[2] + '%s'
        event_end = {'dateTime': formatted_end_string % GMT_OFF}
        event_attendees = values[3]
        if not event_attendees:
            event_attendees = ''
        full_summary = values[0]
        if len(full_summary) >= 10:
            summaryten = full_summary[:11]
        else:
            summary_length = int(len(full_summary)) + 1
            summaryten = full_summary[:summary_length]
        event_id = createeventid('job', formatted_end_string, summaryten)
        #print(event_summary, event_start, event_end, event_attendees, event_id)

        addnewevent(event_summary, event_start, event_end, event_attendees, event_id)
        writeeventtocsv('job', event_id, event_summary, event_start, event_end, event_attendees)

        if values[4] == True:
            job_sub_assignment(event_id)



def add_social():
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
    
    # Creates input window for the new event
    
    sg.ChangeLookAndFeel('GreenTan')

    form = sg.FlexForm('On Track', default_element_size=(10, 3))

    layout = [
        [sg.Button('Notification Settings', key='notifications', button_color=('white', '#001480'))],
        [sg.Text('Input New Event Information', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Event Title')],
        [sg.InputText('', size=(30, 2))],
        [sg.Text('Event Date (yyyy-mm-dd)'), sg.Text('Time of Event (hh:mm:ss)')],
        [sg.InputText('', size=(20, 2)), sg.InputText('', size=(20, 2))],
        [sg.Text('Attendees (emails, separate by commas)')],
        [sg.InputText('', size=(60, 3))],
        [sg.Checkbox('Do you have to do anything beforehand?', default=False)],
        [sg.Submit(), sg.Cancel()]
    ]

    button, values = form.Layout(layout).Read()
    #sg.Popup(button, values)

    if button == 'Submit':
        event_summary = values[0] + " at " + values[2]
        end_time = values[2]
        if int(end_time[3:5]) >= 15:
            start_adjust = int(end_time[3:5]) - 15
        else:
            start_adjust = int(end_time[3:5]) + 45
            if int(end_time[:2]) >= 1:
                hour_adjust = int(end_time[:2]) - 1
                if hour_adjust <= 9:
                    hour_string = '0' + str(hour_adjust)
                else:
                    hour_string = str(hour_adjust)
            else:
                hour_string = str(23)
        formatted_start_string = values[1] + 'T' + hour_string + ':' + str(start_adjust) + end_time[5:] + '%s'
        event_start = {'dateTime': formatted_start_string % GMT_OFF}
        formatted_end_string = values[1] + 'T' + values[2] + '%s'
        event_end = {'dateTime': formatted_end_string % GMT_OFF}
        event_attendees = values[3]
        if not event_attendees:
            event_attendees = []
        elif event_attendees == '':
            event_attendees = []
        full_summary = values[0]
        if len(full_summary) >= 10:
            summaryten = full_summary[:11]
        else:
            summary_length = int(len(full_summary)) + 1
            summaryten = full_summary[:summary_length]
        event_id = createeventid('social', formatted_end_string, summaryten)
        #print(event_summary, event_start, event_end, event_attendees, event_id)

        addnewevent(event_summary, event_start, event_end, event_attendees, event_id)
        writeeventtocsv('social', event_id, event_summary, event_start, event_end, event_attendees)

        if values[4] == True:
            sub_social(event_id)



def sub_social(linked_event_id):
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
    
    # Creates input window for the new event
    
    sg.ChangeLookAndFeel('GreenTan')

    form = sg.FlexForm('On Track', default_element_size=(10, 3))

    layout = [
        [sg.Button('Notification Settings', key='notifications', button_color=('white', '#001480'))],
        [sg.Text('Input Errand Information', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Errand Title')],
        [sg.InputText('', size=(30, 2))],
        [sg.Text('Due Date (yyyy-mm-dd)'), sg.Text('Time Errand is due (hh:mm:ss)')],
        [sg.InputText('', size=(20, 2)), sg.InputText('', size=(20, 2))],
        [sg.Text('Attendees (emails, separate by commas)')],
        [sg.InputText('', size=(60, 3))],
        [sg.Checkbox('Are there more things you need to do?', default=False)],
        [sg.Submit(), sg.Cancel()]
    ]

    button, values = form.Layout(layout).Read()
    #sg.Popup(button, values)

    if button == 'Submit':
        event_summary = values[0] + " due by " + values[2]
        end_time = values[2]
        if int(end_time[3:5]) >= 15:
            start_adjust = int(end_time[3:5]) - 15
        else:
            start_adjust = int(end_time[3:5]) + 45
            if int(end_time[:2]) >= 1:
                hour_adjust = int(end_time[:2]) - 1
                if hour_adjust <= 9:
                    hour_string = '0' + str(hour_adjust)
                else:
                    hour_string = str(hour_adjust)
            else:
                hour_string = str(23)
        formatted_start_string = values[1] + 'T' + hour_string + ':' + str(start_adjust) + end_time[5:] + '%s'
        event_start = {'dateTime': formatted_start_string % GMT_OFF}
        formatted_end_string = values[1] + 'T' + values[2] + '%s'
        event_end = {'dateTime': formatted_end_string % GMT_OFF}
        event_attendees = values[3]
        if not event_attendees:
            event_attendees = []
        elif event_attendees == '':
            event_attendees = []
        full_summary = values[0]
        if len(full_summary) >= 10:
            summaryten = full_summary[:11]
        else:
            summary_length = int(len(full_summary)) + 1
            summaryten = full_summary[:summary_length]
        event_id = createeventid('social', formatted_end_string, summaryten)
        #print(event_summary, event_start, event_end, event_attendees, event_id)
        linked_event = linked_event_id

        addnewevent(event_summary, event_start, event_end, event_attendees, event_id)
        writeeventtocsv('social', event_id, event_summary, event_start, event_end, event_attendees)

        if values[4] == True:
            sub_assignment(linked_event_id)



#initial_window_test()
initial_window()