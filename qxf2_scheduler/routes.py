"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.base_gcal as gcal
import datetime,sys
from datetime import timedelta


def get_all_events(email_id,fetch_date):
    "Get all the events for a fetched date" 
    service = gcal.base_gcal()    
    start_date = datetime.datetime.strptime(fetch_date,'%Y-%m-%d')
    end_date = start_date + timedelta(days=1)
    start_date = start_date.isoformat() + 'Z'
    end_date = end_date.isoformat() + 'Z'
    
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=email_id, timeMin=start_date,
                                        maxResults=10, timeMax=end_date,singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    return events


@app.route("/get-schedule",methods=['GET','POST'])
def date_picker():
    "Dummy page to let you see a schedule"
    if request.method == 'GET':            
            return render_template('get-schedule.html')
    if request.method == 'POST':         
        email=request.form.get('email')
        date=request.form.get('date')        
        all_events = get_all_events(email,date)       
        api_response = {"events":all_events,"email":email}
        return jsonify(api_response)

@app.route("/")
def index():
    "The index page"
    return "The page is not ready yet!"    