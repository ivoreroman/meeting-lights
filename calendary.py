from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client.file import Storage

import datetime
from dateutil.parser import parse

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
CALENDAR_ID = 'wizeline.com_3237383836343933383735@resource.calendar.google.com'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

    return credentials


def get_events(num_events=2):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now, maxResults=num_events, singleEvents=True,
        orderBy='startTime').execute()

    return events_result.get('items', [])


def transform_to_local(raw_date, hours=2):
    return (raw_date + datetime.timedelta(hours=hours)).replace(tzinfo=None)


def get_first_times_parsed(events):
    return {'start': transform_to_local(parse(events[0]['start']['dateTime'])),
             'end': transform_to_local(parse(events[0]['end']['dateTime']))}


def get_next_meeting(now, first_meeting, second_meeting):
    return first_meeting if (first_meeting - now).seconds > 0 else second_meeting


def is_event_between(now, end, start):
    return end < now < start

def room_avalability():
    events = get_events()
    event = get_first_times_parsed(events)
    now = datetime.datetime.now()

    return {'nextMeetingIn': event['start'] if is_event_between(now, event['end'], event['start']) else event['end'],
            'isNowAvailable': is_event_between(now, event['end'], event['start'])}
