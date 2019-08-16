"""
This is a simple script to test the Google calendar
"""

from __future__ import print_function
import datetime
from datetime import timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.events']
TIMEAHEAD = '+05:30'
TIMEZONE = 'UTC'+TIMEAHEAD
DATETIME_FORMAT = '%m/%d/%Y'

def get_today():
    "Return today in a datetime format consistent with DATETIME_FORMAT"
    today = datetime.datetime.now()
    today = today.strftime(DATETIME_FORMAT)
    today = datetime.datetime.strptime(today,DATETIME_FORMAT)

    return today


def process_date_string(date,format=DATETIME_FORMAT):
    "Return a date time object we want for a given date string format"
    return datetime.datetime.strptime(date,DATETIME_FORMAT)


def process_date_isoformat(date,format=TIMEAHEAD):
    "Convert the date to isoformat"
    return date.isoformat() + format


def base_gcal():
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
            print("Your credentials to access Google Calendar are not setup correctly")
    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events_for_date(service,email_id,fetch_date,maxResults=240,debug=False):
    "Return up to a maximum of maxResults events for a given date and email id"
    start_date = process_date_string(fetch_date)
    end_date = start_date.replace(hour=23,minute=59)
    start_date = process_date_isoformat(start_date)
    end_date = process_date_isoformat(end_date)
    if debug:
        print('Getting the upto a maximum of {maxResults} upcoming events'.format(maxResults=maxResults))
    events_result = service.events().list(calendarId=email_id, timeMin=start_date,
                                          maxResults=maxResults, timeMax=end_date, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if debug:
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    return events


def get_busy_slots_for_date(service,email_id,fetch_date,timeZone=TIMEZONE,debug=False):
    "Return free/busy for a given date"
    start_date = process_date_string(fetch_date) 
    end_date = start_date.replace(hour=23,minute=59)
    start_date = process_date_isoformat(start_date)
    end_date = process_date_isoformat(end_date)
    body = {
        "timeMin": start_date,
        "timeMax": end_date,
        "timeZone": TIMEZONE,
        "items": [{"id": email_id}]
    }
    eventsResult = service.freebusy().query(body=body).execute()
    busy_slots = eventsResult[u'calendars'][email_id]['busy']
    if debug:
        print('Busy slots for {email_id} on {date} are: '.format(email_id=email_id,date=fetch_date))
        for slot in busy_slots:
            print(slot['start'],' - ', slot['end'])

    return busy_slots


def make_day_busy(fetch_date):
    "Return the entire day as busy"
    start_date = process_date_string(fetch_date)
    end_date = start_date.replace(hour=23,minute=59)
    start_date = process_date_isoformat(start_date)
    end_date = process_date_isoformat(end_date)
    busy_slots=[{'start':start_date,'end':end_date}]

    return busy_slots


def create_event_for_fetched_date_and_time(service,email,event_start_time,event_end_time,summary,location,description,attendee):
    "Create an event for a particular date and time"
    event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': event_start_time,
                'timeZone': TIMEZONE,
            },
            'end': {
                'dateTime': event_end_time,
                'timeZone': TIMEZONE,
            },            
            'attendees': [
                {'email': attendee},
                
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
                ],
            },
            "conferenceData": 
            {
                "createRequest": 
                {
                    "conferenceSolutionKey": 
                    {
                    "type": "hangoutsMeet"
                    },
                "requestId": "kdb-atdx-exx"
                }
            }
            }
    event = service.events().insert(calendarId=email, body=event).execute()
    
    return event 