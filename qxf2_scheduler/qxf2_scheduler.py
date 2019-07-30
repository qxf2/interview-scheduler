"""
This module contains business logic that wraps around the Google calendar module
We use this extensively in the routes.py of the qxf2_scheduler application
"""

import qxf2_scheduler.base_gcal as gcal
import datetime
from datetime import timedelta

TIMEZONE_STRING = '+05:30'
DAY_START_HOUR = 9
DAY_END_HOUR = 17

def is_past_date(date):
    "Is this date in the past?"
    result_flag = True
    date = gcal.process_date_string(date)
    today = gcal.get_today()
    if date >= today:
        result_flag = False
    
    return result_flag

def get_free_slots(busy_slots, day_start, day_end):
    "Return the free slots"
    """
    Logic:
    1. If busy slots are empty ... set (day_start, day_end) as the interval

    2. There are 6 types of busy slots for us:
    a) A busy slot that ends before day start
        - we ignore
    b) A busy slot that starts after the day end
        - we ignore
    c) A busy slot that starts before the day start and ends after day end
        - we say there are no free slots in that day
    d) A busy slot that starts before day start but ends before day end
        - we set the start of the first free slot to the end of this busy slot 
    e) A busy slot that starts (after day start, before day end) but ends after day end
        - we set the end of the last free slot to be the start of this busy slot
    f) A busy slot that starts after day start and ends before day end
        - we accept both ends points of this slot
    """
    free_slots = []
    if len(busy_slots) == 0:
        free_slots.append(day_start)
    for busy_slot in busy_slots:
        if busy_slot['end'] < day_start:
            continue 
        elif busy_slot['start'] > day_end:
            if len(free_slots) == 0:
                free_slots.append(day_start)
        elif busy_slot['start'] <= day_start and busy_slot['end'] >= day_end:
            break 
        elif busy_slot['start'] < day_start and busy_slot['end'] < day_end:
            free_slots.append(busy_slot['end'])
        elif busy_slot['start'] > day_start and busy_slot['end'] > day_end:
            free_slots.append(busy_slot['start'])
        else:
            #If we make it this far and free_slots is still empty
            #It means the start of the free slot is the start of the day
            if len(free_slots) == 0:
                free_slots.append(day_start)
            free_slots.append(busy_slot['start'])
            free_slots.append(busy_slot['end'])
    #If we have an odd number of values in free_slots
    #It means that we need to close one interval with end of day
    if len(free_slots)%2 == 1:
        if free_slots[-1]==day_end:
            free_slots = free_slots[:-1]
        else:
            free_slots.append(day_end)
    
    return free_slots

def get_busy_slots_for_date(email_id,fetch_date,debug=False):
    "Get the busy slots for a given date"
    service = gcal.base_gcal()
    all_events = gcal.get_events_for_date(service,email_id,fetch_date)
    pto_flag = False
    for event in all_events:
        if 'summary' in event.keys():
            if 'PTO' in event['summary']:
                pto_flag = True 
                break
    if pto_flag:
        busy_slots = gcal.make_day_busy(fetch_date)
    else:
        busy_slots = gcal.get_busy_slots_for_date(service,email_id,fetch_date,timeZone=gcal.TIMEZONE,debug=debug)

    return busy_slots

def get_free_slots_for_date(email_id,fetch_date,debug=False):
    "Return a list of free slots for a given date and email"
    service = gcal.base_gcal()
    busy_slots = get_busy_slots_for_date(email_id,fetch_date,debug=debug)
    day_start = process_time_to_gcal(fetch_date,DAY_START_HOUR)
    day_end = process_time_to_gcal(fetch_date,DAY_END_HOUR)
    free_slots = get_free_slots(busy_slots,day_start,day_end)
    processed_free_slots = []
    for i in range(0,len(free_slots),2):
        processed_free_slots.append({'start':process_only_time_from_str(free_slots[i]),'end':process_only_time_from_str(free_slots[i+1])})
        
    return processed_free_slots

def get_events_for_date(email_id, fetch_date, maxResults=240,debug=False):
    "Get all the events for a fetched date"
    service = gcal.base_gcal()
    events = gcal.get_events_for_date(service,email_id,fetch_date,debug=debug)

    return events

def process_time_to_gcal(given_date,hour_offset=None):
    "Process a given string to a gcal like datetime format"
    processed_date = gcal.process_date_string(given_date)
    if hour_offset is not None:
        processed_date = processed_date.replace(hour=hour_offset)
    processed_date = gcal.process_date_isoformat(processed_date)
    processed_date = str(processed_date).replace('Z',TIMEZONE_STRING)

    return processed_date

def process_only_time_from_str(date):
    "Process and return only the time stamp from a given string"
    #Typical date string: 2019-07-29T15:30:00+05:30
    timestamp = datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%S+05:30')
    return timestamp.strftime('%H') + ':' + timestamp.strftime('%M')


#----START OF SCRIPT
if __name__ == '__main__':
    email = 'indira@qxf2.com'
    date = '07/29/2019'
    print("\n=====HOW TO GET ALL EVENTS ON A DAY=====")
    get_events_for_date(email, date, debug=True)
    print("\n=====HOW TO GET BUSY SLOTS=====")
    busy_slots = get_busy_slots_for_date(email,date,debug=True)
    print("\n=====HOW TO GET FREE SLOTS=====")
    free_slots = get_free_slots_for_date(email,date)
    print("Free slots for {email} on {date} are:".format(email=email, date=date))
    for slot in free_slots:
        print(slot['start'],'-',slot['end'])