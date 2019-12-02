"""
This module contains business logic that wraps around the Google calendar module
We use this extensively in the routes.py of the qxf2_scheduler application
"""

import qxf2_scheduler.base_gcal as gcal
#import base_gcal as gcal
import datetime
from datetime import timedelta
import random

TIMEZONE_STRING = '+05:30'
FMT='%H:%M'
CHUNK_DURATION = '30'
SUMMARY = 'Interview Scheduler'
LOCATION =  'Google Hangout or Office',
DESCRIPTION = 'Scheduling an interview',
ATTENDEE = 'annapoorani@qxf2.com'
DATE_TIME_FORMAT = "%m/%d/%Y%H:%M"

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
    
    return True if day==5 or day==6 else False


def convert_combined_string_into_isoformat(create_event_timings_and_date):
    "Converting the string into iso format"
    converted_create_event_date_and_time = datetime.datetime.strptime(create_event_timings_and_date,DATE_TIME_FORMAT).isoformat()

    return converted_create_event_date_and_time


def combine_date_and_time(date,selected_slot):
    "Combine the date and selected slot into isoformat" 
    start_time = selected_slot.split('-')[0].strip()    
    end_time = selected_slot.split('-')[-1].strip()    
    create_event_start_time =  convert_combined_string_into_isoformat((date + start_time)) 
    create_event_end_time = convert_combined_string_into_isoformat((date + end_time))

    return create_event_start_time,create_event_end_time


def append_the_create_event_info(create_event):
    "Appends the created event information into list"
    created_event_info = [] 
    created_event_info.append({'start':create_event['start']})    
    created_event_info.append({'end':create_event['end']})     
    created_event_info.append({'Link':create_event['htmlLink']})
    
    return created_event_info


def convert_interviewer_time_into_string(interviewer_time):
    "Convert the integer into string format"
    interviewer_actual_time = datetime.datetime.strptime(str(interviewer_time),"%H")
    interviewer_actual_time = interviewer_actual_time.strftime("%H") + ":" + interviewer_actual_time.strftime("%M")
    return interviewer_actual_time

   
def create_event_for_fetched_date_and_time(date,emails,selected_slot):
    "Create an event for fetched date and time"    
    service = gcal.base_gcal()    
    if ',' in emails:        
        attendee_email_id = emails.split(',')       
        attendee_email_id = random.choice(attendee_email_id)        
    else:
        attendee_email_id = emails    
    create_event_start_time,create_event_end_time = combine_date_and_time(date,selected_slot)      
    create_event = gcal.create_event_for_fetched_date_and_time(service,create_event_start_time,create_event_end_time,
    SUMMARY,LOCATION,DESCRIPTION,attendee_email_id)
    created_event_info = append_the_create_event_info(create_event)

    return created_event_info    


def get_modified_free_slot_start(free_slot_start,marker):
    "Modifiying the free slot start to 00 or 30"
    if free_slot_start[-2:]=='00':
        modified_free_slot_start = free_slot_start
    elif free_slot_start[-2:] <= marker:
        modified_free_slot_start = '{}:{}'.format(free_slot_start.split(':')[0], marker)
        
    elif free_slot_start[-2:] > marker:
        free_slot_start = '{}:{}'.format(free_slot_start.split(':')[0], '00')
        modified_free_slot_start = convert_string_into_time(free_slot_start) + timedelta(hours=1)
        modified_free_slot_start = get_datetime_in_time_format(modified_free_slot_start)   

    return modified_free_slot_start


def get_modified_free_slot_end(free_slot_end,marker):
    "Modifiying the free slot start to 00 or 30"
    if free_slot_end[-2:]=='00' or free_slot_end[-2:]==marker :
        modified_free_slot_end = free_slot_end                    

    elif free_slot_end[-2:] < marker:                    
        modified_free_slot_end = '{}:{}'.format(free_slot_end.split(':')[0], '00')
        
    elif free_slot_end[-2:] > marker:
        modified_free_slot_end = '{}:{}'.format(free_slot_end.split(':')[0], marker)

    return modified_free_slot_end


def get_chunks_in_slot(modified_free_slot_start,modified_free_slot_end,diff_between_slots_after_modified,interviewer_email_id):
    "Divides the free slots into chunks"    
    chunk_slots = modified_free_slot_start               
    result_flag = True
    idx=0 
    chunk_slot_list = [] 
    chunk_time_interval = []   
    if diff_between_slots_after_modified <= timedelta(minutes=int(CHUNK_DURATION)):
        chunk_slot_list.append(modified_free_slot_start)
        chunk_slot_list.append(modified_free_slot_end)
        chunk_time_interval.append({'start':modified_free_slot_start,'end':modified_free_slot_end,'email':interviewer_email_id})         
        
    else:          
        while result_flag:                        
            chunk_slots = convert_string_into_time(chunk_slots)
            chunk_slots = chunk_slots +  timedelta(minutes=int(CHUNK_DURATION))
            chunk_slots =  get_datetime_in_time_format(chunk_slots)                
            if idx==0:                           
                chunk_slot_list.append(modified_free_slot_start)
                chunk_slot_list.append(chunk_slots)                               
                chunk_slot_start = chunk_slot_list[idx]
                chunk_slot_end = chunk_slot_list[idx+1]                
                chunk_time_interval.append({'start':chunk_slot_start,'end':chunk_slot_end,'email':interviewer_email_id})
            else:                                              
                chunk_slot_list.append(chunk_slots)                          
                chunk_slot_start = chunk_slot_list[idx]
                chunk_slot_end = chunk_slot_list[idx+1]                
                chunk_time_interval.append({'start':chunk_slot_start,'end':chunk_slot_end,'email':interviewer_email_id})
            idx = idx+1 
            modified_free_slot_start = convert_string_into_time(modified_free_slot_start)                       
            modified_free_slot_start = modified_free_slot_start + timedelta(minutes=int(CHUNK_DURATION))
            modified_free_slot_start = get_datetime_in_time_format(modified_free_slot_start)
            
            #While loop should stop if both time become equal                                 
            if modified_free_slot_end == modified_free_slot_start:                    
                result_flag = False

    return chunk_time_interval

def combine_multiple_chunks(divided_chunk_slots):
    "Combine the multiple chunks into one button"    
    grouped_chunk_slots = {}
    for each_chunk in divided_chunk_slots:
        key = (each_chunk["start"], each_chunk["end"])        
        if key in grouped_chunk_slots:
            grouped_chunk_slots[key]["email"].append(each_chunk["email"])            
        else:
            grouped_chunk_slots[key] = each_chunk
            grouped_chunk_slots[key]["email"] = [each_chunk["email"]]            

    divided_chunk_slots = list(grouped_chunk_slots.values())      

    return divided_chunk_slots


def get_free_slots_in_chunks(free_slots):
    "Return the free slots in 30 minutes interval"
    #Appending the 30 minutes slot into list
    divided_chunk_slots = []
    if free_slots == None:
        print("There are no more free slots available for this user")    
    else: 
        for free_slot in  free_slots:
            #Initializing the free slot start            
            free_slot_start = free_slot['start']
            #Intializing the next free slot end        
            free_slot_end = free_slot['end']
            interviewer_email_id = free_slot['email_id']

            
            #Find the difference between start and end slot
            diff_between_slots = convert_string_into_time(free_slot_end) - convert_string_into_time(free_slot_start)
            
            if diff_between_slots >= timedelta(minutes=int(CHUNK_DURATION)):
                modified_free_slot_start = get_modified_free_slot_start(free_slot_start,marker=CHUNK_DURATION)
                modified_free_slot_end = get_modified_free_slot_end(free_slot_end,marker=CHUNK_DURATION)                                
                diff_between_slots_after_modified =  convert_string_into_time(modified_free_slot_end) - convert_string_into_time(modified_free_slot_start)
                divided_chunk_slots += get_chunks_in_slot(modified_free_slot_start,modified_free_slot_end,diff_between_slots_after_modified,interviewer_email_id)                
                divided_chunk_slots = sorted(divided_chunk_slots, key=lambda k: k['start'])
        divided_chunk_slots = combine_multiple_chunks(divided_chunk_slots)

    return divided_chunk_slots               


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
            if busy_slots[-1]==busy_slot:
                if len(free_slots) == 0:
                    free_slots.append(day_start)
            else:
                continue
        elif busy_slot['start'] > day_end:
            if len(free_slots) == 0:
                free_slots.append(day_start)
        elif busy_slot['start'] <= day_start and busy_slot['end'] >= day_end:
            break 
        elif busy_slot['start'] <= day_start and busy_slot['end'] < day_end:
            free_slots.append(busy_slot['end'])
        elif busy_slot['start'] > day_start and busy_slot['end'] > day_end:
            #At this point the day has started
            if len(free_slots) == 0:
                free_slots.append(day_start)
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
            event_name = event['summary'].split(':')[-1].strip()
            event_name = event_name.split()[0]
            if 'PTO'.lower() == event_name.lower():
                pto_flag = True 
                break
    if pto_flag:
        busy_slots = gcal.make_day_busy(fetch_date)
    else:
        busy_slots = gcal.get_busy_slots_for_date(service,email_id,fetch_date,timeZone=gcal.TIMEZONE,debug=debug)

    return busy_slots


def get_interviewer_email_id(interviewer_work_time_slots):
    "Parse the email id from the list"    
    interviewers_email_id = []    
    for each_interviewer_in_row in interviewer_work_time_slots:
        interviewers_email_id.append(each_interviewer_in_row['interviewer_email'])
        
    return interviewers_email_id


def get_free_slots_for_date(fetch_date,interviewer_work_time_slots,debug=False):
    "Return a list of free slots for a given date and email"    
    processed_free_slots = []
    for each_slot in interviewer_work_time_slots:
        individual_interviewer_email_id = each_slot['interviewer_email']
        busy_slots = get_busy_slots_for_date(individual_interviewer_email_id,fetch_date,debug=debug)        
        day_start_hour = each_slot['interviewer_start_time']
        day_end_hour = each_slot['interviewer_end_time']
        day_start = process_time_to_gcal(fetch_date,day_start_hour)
        day_end = process_time_to_gcal(fetch_date,day_end_hour)
        free_slots = get_free_slots(busy_slots,day_start,day_end)
        for i in range(0,len(free_slots),2):
            processed_free_slots.append({'start':process_only_time_from_str(free_slots[i]),'end':process_only_time_from_str(free_slots[i+1]),'email_id':individual_interviewer_email_id})
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
        time_split = hour_offset.split(":")
        processed_date = processed_date.replace(hour=int(time_split[0]))
        processed_date = processed_date.replace(minute=int(time_split[1]))
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
    email = 'test@qxf2.com'
    date = '8/13/2019'
    selected_slot = '9:30-10:00'
    interviewer_work_time_slots = [{'interviewer_start_time': '14:00', 'interviewer_end_time': '20:00'}, 
    {'interviewer_start_time': '21:00', 'interviewer_end_time': '23:00'}]
    emails='test@qxf2.com'
    print("\n=====HOW TO GET ALL EVENTS ON A DAY=====")
    get_events_for_date(email, date, debug=True)
    print("\n=====HOW TO GET BUSY SLOTS=====")
    busy_slots = get_busy_slots_for_date(email,date,debug=True)
    print("\n=====HOW TO GET FREE SLOTS=====")
    free_slots = get_free_slots_for_date(date,interviewer_work_time_slots)    
    print("Free slots for {email} on {date} are:".format(email=email, date=date)) 
    print(free_slots)      
    for slot in free_slots:
        print(slot['start'],'-',slot['end'])
    print("\n=====HOW TO GET FREE SLOTS IN CHUNKS=====")    
    free_slots_in_chunks = get_free_slots_in_chunks(free_slots)      
    print("\n======CREATE AN EVENT FOR FETCHED DATE AND TIME=====")
    event_created_slot = create_event_for_fetched_date_and_time(date,emails,selected_slot)
    print("The event created,The details are",event_created_slot)  