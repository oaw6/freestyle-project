# freestyle-project/test.py

#Almost every function in the script requires HTTP requests and interacting with the Google Calendar API, and those that do
#also require established calendars, active calendar events, etc. Testing these would overload the server and flood
#my calendar with tested events. Thus, only functions that do not rely on those requests are tested here.

import pytest
import os
import csv
import pandas

#For some reason the file won't let me import functions from on-track.py, so I've copied in the exact functions I'm testing

def createeventid(type, end_time, summary_ten):
    #Whenever a new event is created, this generates a unique bit32 string identifier for the event. This is necessary for the API
    new_event_id = ''
    if type == 'school':
        new_event_id = new_event_id + 'sc'
    elif type == 'job':
        new_event_id = new_event_id + 'jo'
    else:
        new_event_id = new_event_id + 'so'
    new_event_id = new_event_id + end_time[:4] + end_time[5:7] + end_time[8:10] + end_time[11:13] + end_time[14:16] + end_time[17:19]
    unrefined_summary = summary_ten.lower()
    summ_ten = unrefined_summary.replace('w', '11')
    summ_ten = summ_ten.replace('x', '12')
    summ_ten = summ_ten.replace('y', '13')
    summ_ten = summ_ten.replace('z', '14')
    summ_ten = summ_ten.replace(' ', '15')
    new_event_id = new_event_id + summ_ten
    return new_event_id

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

def test_createeventid():
    assert createeventid('school', '2019-05-04T12:00:00%s', 'aaaaaaaaaa') == 'sc20190504120000aaaaaaaaaa'

def test_writeeventtocsv():
    writeeventtocsv('school', 'sc20190504120000aaaaaaaaaa', 'aaaaaaaaaa', '2019-05-04T12:00:00%s', '2019-05-04T12:30:00%s', [])
