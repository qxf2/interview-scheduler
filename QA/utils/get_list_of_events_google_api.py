"""
    This utility file fetches the list of events for a desired email adress and a particular date
"""
from __future__ import print_function
from datetime import datetime,timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import re
class event_list():
    """
    This class contains method to fetch the list of events on a particular day for a given email id
    """
    TIMEAHEAD = '+05:30'
    TIMEZONE = 'UTC'+TIMEAHEAD

    def fetch_events(self,emailid,mintime,maxtime):
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        # If modifying these scopes, delete the file token.pickle.
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = self.flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)

        #set the email id for which you want to fetch the event
        self.calender_id=emailid

        #get list of events for the given email id and time period
        self.events=self.service.events().list(calendarId=self.calender_id,timeMin=mintime,timeMax=maxtime).execute()
        self.event_items=self.events['items']
        return(self.event_items)
   
    def get_time_of_events(self,list_of_events):
        "method to extract only the time of the events "
        
        start=[]
        end=[]

        for each_time in list_of_events:
            #Appends the start time of all the events to list 'start'
            start.append(each_time['start']['dateTime'])

            #Appends the end time of all the events to list 'end'
            end.append(each_time['end']['dateTime'])

        start_list_date_converted=[]
        end_list_date_converted=[]

        format="%Y-%m-%dT%H:%M:%S+05:30"

        #Converts the start times from string format to date format
        for each_time in reversed(start):
            each_time=datetime.strptime(each_time,format)
            start_list_date_converted.append(each_time)
        
        #Converts the end times from string format to date format
        for each_time in reversed(end):
            each_time=datetime.strptime(each_time,format)
            end_list_date_converted.append(each_time)

        return start_list_date_converted,end_list_date_converted
        
        