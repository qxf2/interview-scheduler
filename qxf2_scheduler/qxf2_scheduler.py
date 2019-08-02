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
FMT='%H:%M'

def convert_string_into_time(alloted_slots):
    "Converting the given string into time"
    alloted_slots = datetime.datetime.strptime(alloted_slots,FMT)
    return alloted_slots

def get_datetime_in_time_format(time_frame_slots):
    "Split the time into hours and minutes"
    time_frame_slots = time_frame_slots.strftime("%H") + ":" + time_frame_slots.strftime("%M")
    return time_frame_slots

def is_past_date(date):
    "Is this date in the past?"
    result_flag = True
    date = gcal.process_date_string(date)
    today = gcal.get_today()
    if date >= today:
        result_flag = False
    
    return result_flag

def is_qxf2_holiday(date):
    "Is this date a Qxf2 holiday?"
    holidays = ['2019-01-01','2019-01-15','2019-03-04','2019-05-01','2019-08-15','2019-09-02','2019-10-02','2019-10-08','2019-11-01']
    #Holiday date format is different to keep it consistent with the JavaScript
    #That way, you can copy paste the same array between the html and here
    holiday_format = '%Y-%m-%d'
    date = gcal.process_date_string(date,holiday_format)
    date = date.strftime(holiday_format)
    result_flag = True if date in holidays else False

    return result_flag

def is_weekend(date):
    "Is this a weekend?"
    date = gcal.process_date_string(date)
    day = date.weekday()
    print('~~~~',day)
    return True if day==5 or day==6 else False


def get_free_slots_in_chunks(free_slots):
    "Return the free slots in 30 minutes interval"
    #Appending the 30 minutes slot into list
    if free_slots == None:
        print("There are no more free slots available for this user")    
    else:        
        chunk_time_interval = []        
        for i in  range(0,len(free_slots)):
            #Initializing the free slot end            
            free_slot_start = free_slots[i]['start']
            #Intializing the next free slot start        
            free_slot_end = free_slots[i]['end']
            
            #Find the difference between start and end slot
            diff_between_slots = convert_string_into_time(free_slot_end) - convert_string_into_time(free_slot_start)
            
            if diff_between_slots >= timedelta(minutes=30):                
                if free_slot_start[-2:]=='00':
                    modified_free_slot_start = free_slot_start                    

                elif free_slot_start[-2:] <= '30':
                    modified_free_slot_start = '{}:{}'.format(free_slot_start.split(':')[0], '30')
                    
                elif free_slot_start[-2:] > '30':
                    free_slot_start = '{}:{}'.format(free_slot_start.split(':')[0], '00')
                    modified_free_slot_start = convert_string_into_time(free_slot_start) + timedelta(hours=1)
                    modified_free_slot_start = get_datetime_in_time_format(modified_free_slot_start)
                    
                chunk_slots = modified_free_slot_start

                if free_slot_end[-2:]=='00' or free_slot_end[-2:]=='30' :
                    modified_free_slot_end = free_slot_end                    

                elif free_slot_end[-2:] <'30':                    
                    modified_free_slot_end = '{}:{}'.format(free_slot_end.split(':')[0], '00')
                    
                elif free_slot_end[-2:] > '30':
                    modified_free_slot_end = '{}:{}'.format(free_slot_end.split(':')[0], '30')                    
                
                result_flag = True
                idx=0 
                chunk_slot_list = []                 
                diff_between_slots_after_modified =  convert_string_into_time(modified_free_slot_end) - convert_string_into_time(modified_free_slot_start)
                if diff_between_slots_after_modified <= timedelta(minutes=30):
                    chunk_slot_list.append(modified_free_slot_start)
                    chunk_slot_list.append(modified_free_slot_end)
                    chunk_time_interval.append({'start':modified_free_slot_start,'end':modified_free_slot_end}) 
                else:          
                    while result_flag:                        
                        chunk_slots = convert_string_into_time(chunk_slots)
                        chunk_slots = chunk_slots +  timedelta(minutes=30)
                        chunk_slots =  get_datetime_in_time_format(chunk_slots)                
                        if idx==0:                           
                            chunk_slot_list.append(modified_free_slot_start)
                            chunk_slot_list.append(chunk_slots)                               
                            chunk_slot_start = chunk_slot_list[idx]
                            chunk_slot_end = chunk_slot_list[idx+1]
                            chunk_time_interval.append({'start':chunk_slot_start,'end':chunk_slot_end})
                        else:                                              
                            chunk_slot_list.append(chunk_slots)                          
                            chunk_slot_start = chunk_slot_list[idx]
                            chunk_slot_end = chunk_slot_list[idx+1]
                            chunk_time_interval.append({'start':chunk_slot_start,'end':chunk_slot_end})
                        idx = idx+1 
                        modified_free_slot_start = convert_string_into_time(modified_free_slot_start)                       
                        modified_free_slot_start = modified_free_slot_start + timedelta(minutes=30)
                        modified_free_slot_start = get_datetime_in_time_format(modified_free_slot_start)
                        
                        #While loop should stop if both time become equal                                 
                        if modified_free_slot_end == modified_free_slot_start:                    
                            result_flag = False

    return chunk_time_interval               


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
            continue 
        elif busy_slot['start'] < day_start and busy_slot['end'] > day_end:
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
    email = 'mak@qxf2.com'
    date = '08/1/2019'
    print("\n=====HOW TO GET ALL EVENTS ON A DAY=====")
    get_events_for_date(email, date, debug=True)
    print("\n=====HOW TO GET BUSY SLOTS=====")
    busy_slots = get_busy_slots_for_date(email,date,debug=True)
    print("\n=====HOW TO GET FREE SLOTS=====")
    free_slots = get_free_slots_for_date(email,date)    
    print("Free slots for {email} on {date} are:".format(email=email, date=date)) 
    print(free_slots)      
    for slot in free_slots:
        print(slot['start'],'-',slot['end'])
    print("\n=====HOW TO GET FREE SLOTS IN CHUNKS=====")
    #free_slots = [{'start': '09:00', 'end': '12:35'}, {'start': '13:00', 'end': '13:30'},{'start': '15:00', 'end': '16:30'}]
    free_slots_in_chunks = get_free_slots_in_chunks(free_slots)
    print(free_slots_in_chunks)    