"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.base_gcal as gcal
import datetime
import sys
import pytz
from datetime import timedelta


"""def get_alloted_free_slots(free_slots):
    "Return the free slots with one hour time interval"
    i = 0
    len_of_slot = (len(free_slots)) / 2
    parsed_free_slot = []
    while len_of_slot:        
        start_free_slot = free_slots[i]
        free_end_slot = free_slots[i + 1]
        current_start = start_free_slot
        while(current_start < free_end_slot):
            start = current_start
            current_start = current_start + 1
            print("Iam current start",current_start,file=sys.stderr)
            mid_value = current_start
            if (mid_value == free_end_slot):
                continue
            else:
                parsed_free_slot.append((start, mid_value))
        i = i + 2
        print(parsed_free_slot)
        len_of_slot = len_of_slot - 1

    return parsed_free_slot"""
    


def get_free_slots(busy_slots, day_start, day_end):
    "Return the free slots"
    free_slots = []
    for i, busy_slot in enumerate(busy_slots):
        # I couldnt use the time object so I tried with this option only
        # I tried to use the format of google calendar time format returns but couldnt compare it because
        # it always goes to second elif statememnt that means it breaks and come out of it
        # I am adding this line for your refernece
        busy_slot[i]['start'] = str(datetime.datetime.strptime(
            busy_slot[i]['start'], "%Y-%m-%dT%H:%M:%S+05:30").time())

        busy_slot[i]['end'] = str(datetime.datetime.strptime(
            busy_slot[i]['end'], "%Y-%m-%dT%H:%M:%S+05:30").time())

        if busy_slot[i]['start'] < day_start and busy_slot[i]['end'] < day_start:

            continue
        elif busy_slot[i]['start'] > day_end:

            continue
        elif busy_slot[i]['start'] < day_start and busy_slot[i]['end'] > day_end:

            break
        elif busy_slot[i]['start'] < day_start and busy_slot[i]['end'] < day_end:

            free_slots.append(busy_slot['end'])
        elif busy_slot[i]['start'] > day_start and busy_slot[i]['end'] > day_end:

            free_slots.append(busy_slot[i]['start'])
        else:
            # If we make it this far and free_slots is still empty
            # It means the start of the free slot is the start of the day

            if len(free_slots) == 0:
                free_slots.append(day_start)

            free_slots.append(busy_slot[i]['start'])
            free_slots.append(busy_slot[i]['end'])
    # If we have an odd number of values in free_slots
    # It means that we need to close one interval with end of day
    if len(free_slots) % 2 == 1:
        free_slots.append(day_end)

    return free_slots


def get_free_events(email_id, fetch_date):
    "Get the free events for a given date"
    service = gcal.base_gcal()
    # tz = pytz.timezone('US/Central')    
    start_date = datetime.datetime.strptime(fetch_date, '%Y-%m-%d')
    end_date = start_date + timedelta(days=1)
    start_date = start_date.isoformat() + 'Z'
    end_date = end_date.isoformat() + 'Z'
    body = {
        "timeMin": start_date,
        "timeMax": end_date,
        "timeZone": 'UTC+5:30',
        "items": [{"id": email_id}]
    }
    eventsResult = service.freebusy().query(body=body).execute()
    cal_dict = eventsResult[u'calendars']
    dictionary_values = cal_dict.values()
    for each_busy_schedule in dictionary_values:
        busy_slots = each_busy_schedule.values()
        print(busy_slots, file=sys.stderr)
    day_start = datetime.time(9, 00, 00)
    day_start = datetime.time.strftime(day_start, '%H:%M:%S')
    day_end = datetime.time(17, 00, 00)
    day_end = datetime.time.strftime(day_end, '%H:%M:%S')

    free_slots = get_free_slots(busy_slots, day_start, day_end)
    num_free = len(free_slots)
    print("Free slots are: ")
    for i in range(0, num_free, 2):
        print(free_slots[i], '-', free_slots[i + 1], file=sys.stderr)

    #divided_free_slots = get_alloted_free_slots(free_slots)

    return free_slots


def get_all_events(email_id, fetch_date):
    "Get all the events for a fetched date"
    service = gcal.base_gcal()
    start_date = datetime.datetime.strptime(fetch_date, '%Y-%m-%d')
    end_date = start_date + timedelta(days=1)
    start_date = start_date.isoformat() + 'Z'
    end_date = end_date.isoformat() + 'Z'

    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=email_id, timeMin=start_date,
                                          maxResults=10, timeMax=end_date, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    return events


@app.route("/get-schedule", methods=['GET', 'POST'])
def date_picker():
    "Dummy page to let you see a schedule"
    if request.method == 'GET':
        return render_template('get-schedule.html')
    if request.method == 'POST':
        email = request.form.get('email')
        date = request.form.get('date')
        all_events = get_all_events(email, date)
        free_events = get_free_events(email, date)
        api_response = {"events": free_events, "email": email}
        return jsonify(api_response)


@app.route("/")
def index():
    "The index page"
    return "The page is not ready yet!"
