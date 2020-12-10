"""
This module contains business logic that wraps around the Google calendar module
We use this extensively in the routes.py of the qxf2_scheduler application
"""

import qxf2_scheduler.base_gcal as gcal
#import base_gcal as gcal
from googleapiclient.errors import HttpError
import datetime
from datetime import timedelta
import random,sys
from qxf2_scheduler import db
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd

TIMEZONE_STRING = '+05:30'
FMT='%H:%M'
#CHUNK_DURATION = '60'
LOCATION =  'Google Hangout or Office',
ATTENDEE = 'annapoorani@qxf2.com'
DATE_TIME_FORMAT = "%m/%d/%Y%H:%M"
NEW_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S+05:30"

from pytz import timezone

from qxf2_scheduler.models import Jobcandidate,Updatetable,Interviewers,Candidates,Candidateround, Interviewcount


def convert_to_timezone(date_and_time):
    "convert the time into current timezone"
    # Current time in UTC
    format = "%Y-%m-%d %H:%M:%S %Z%z"
    # Convert to Asia/Kolkata time zone
    now_asia = date_and_time.astimezone(timezone('Asia/Kolkata'))
    now_asia = now_asia.strftime(format)
    return now_asia


def scheduler_job():
    "Runs this job in the background"
    last_inserted_id = db.session.query(Updatetable).order_by(Updatetable.table_id.desc()).first()
    fetch_interview_time = Jobcandidate.query.all()
    for each_interview_time in fetch_interview_time:
        if each_interview_time.interview_start_time == None:
            pass
        else:
            interview_start_time = datetime.datetime.strptime(each_interview_time.interview_start_time,'%Y-%m-%dT%H:%M:%S+05:30')
            # Current time in UTC
            now_utc = datetime.datetime.now(timezone('UTC'))
            current_date_and_time = convert_to_timezone(now_utc)
            current_date_and_time = datetime.datetime.strptime(current_date_and_time,"%Y-%m-%d %H:%M:%S IST+0530")
            candidate_status = each_interview_time.candidate_status
            if interview_start_time <= current_date_and_time and int(candidate_status) == 3:
                    update_candidate_status = Jobcandidate.query.filter(each_interview_time.candidate_id==Jobcandidate.candidate_id).update({'candidate_status':1})
                    db.session.commit()
                    #update_round_status = Candidateround.query.filter()

#Running the task in the background to update the jobcandidate table
sched = BackgroundScheduler(daemon=True)
#sched.add_job(scheduler_job,'cron', minute='*')
sched.add_job(scheduler_job,'cron',day_of_week='mon-fri', hour='*', minute='1,31')
sched.start()


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


def append_the_create_event_info(create_event,interviewer_email_id):
    "Appends the created event information into list"
    created_event_info = []
    created_event_info.append({'start':create_event['start']})
    created_event_info.append({'end':create_event['end']})
    created_event_info.append({'Link':create_event['htmlLink']})
    created_event_info.append({'interviewer_email':interviewer_email_id})

    return created_event_info


def convert_interviewer_time_into_string(interviewer_time):
    "Convert the integer into string format"
    interviewer_actual_time = datetime.datetime.strptime(str(interviewer_time),"%H")
    interviewer_actual_time = interviewer_actual_time.strftime("%H") + ":" + interviewer_actual_time.strftime("%M")
    return interviewer_actual_time


def convert_string_into_time_new(conversion_time):
    "convert string into time"

    return datetime.datetime.strptime(conversion_time, NEW_DATE_TIME_FORMAT)


def calculate_difference_in_time(start, end):
    "Calculate the difference between start and end busy slots"
    converted_start_time = convert_string_into_time_new(start)
    converted_end_time = convert_string_into_time_new(end)
    diff_time = converted_end_time-converted_start_time

    return diff_time


def total_busy_slot_for_interviewer(busy_slots):
    "Calculates the total busy duration for the interviewer"
    t='00:00:00'
    total_busy_time = datetime.datetime.strptime(t,'%H:%M:%S')
    for each_slot in busy_slots:
        start_time = each_slot['start']
        end_time = each_slot['end']
        diff_time = calculate_difference_in_time(start_time,end_time)
        total_busy_time = total_busy_time + diff_time
        print(total_busy_time)
    return total_busy_time


def get_busy_slots_for_fetched_email_id(email_id,fetch_date,debug=False):
    "Get the busy slots for a given date"
    service = gcal.base_gcal()
    busy_slots = []
    event_organizer_list = []
    if service:
        all_events = gcal.get_events_for_date(service,email_id,fetch_date)
        if all_events:
            for event in all_events:
                event_organizer = event['organizer']['email']
                event_organizer_list.append(event_organizer)
            busy_slots = gcal.get_busy_slots_for_date(service,email_id,fetch_date,timeZone=gcal.TIMEZONE,debug=debug)

    return busy_slots


def total_busy_slots(attendee_email_id, date):
    "Find the total busy slots for all interviewers"
    total_busy_time_list = []
    for each_attendee in attendee_email_id:
        busy_slots = get_busy_slots_for_fetched_email_id(each_attendee,date)
        total_time = total_busy_slot_for_interviewer(busy_slots)
        total_busy_time_list.append(total_time)

    print(total_busy_time_list,attendee_email_id)
    return total_busy_time_list


def total_count_list(attendee_email_id):
    "Find the total interview count for the interviewer"
    total_interview_count_list = []
    for new_attendee in attendee_email_id:
        attendee_id = Interviewers.query.filter(Interviewers.interviewer_email == new_attendee).value(Interviewers.interviewer_id)
        print("Iam attendee id",attendee_id)
        #fetch the interview count for the interviewer
        interview_count = Interviewcount.query.filter(Interviewcount.interviewer_id == attendee_id).value(Interviewcount.interview_count)
        print("interview count",interview_count)
        if interview_count is None:
            print("interview count none",interview_count)
            total_interview_count_list.append(0)
        else:
            total_interview_count_list.append(interview_count)
    print(total_interview_count_list,attendee_email_id)
    return total_interview_count_list


def pick_interviewer(attendee_email_id,date):
    "Pick the interviewer based on busy time"
    #Find the total busy slots for the interviewers
    busy_time_list = total_busy_slots(attendee_email_id, date)
    print("line no 219",busy_time_list)
    #Find the interview count for the interviewer
    interview_count_list = total_count_list(attendee_email_id)
    #Scoring algorithm to pick the interviewer
    busy_slots_rank = pd.DataFrame(busy_time_list, attendee_email_id).rank()
    print(busy_slots_rank)
    interview_count_rank = pd.DataFrame(interview_count_list, attendee_email_id).rank(ascending=False)
    print(interview_count_rank)
    average_busy_interview_count = (busy_slots_rank + interview_count_rank).rank()
    print(average_busy_interview_count,"line no 226")
    df_rank_to_dict = average_busy_interview_count.to_dict()[0]
    print(df_rank_to_dict)
    picked_attendee_email_id = min(df_rank_to_dict, key=df_rank_to_dict.get)
    print("picked",picked_attendee_email_id)
    return picked_attendee_email_id


def create_event_for_fetched_date_and_time(date,interviewer_emails,candidate_email,selected_slot,round_name,round_description):
    "Create an event for fetched date and time"
    service = gcal.base_gcal()
    interviewer_candidate_email = []
    if ',' in interviewer_emails:
        attendee_email_id = interviewer_emails.split(',')
        picked_email_id = pick_interviewer(attendee_email_id,date)
    else:
        attendee_email_id = interviewer_emails
    interviewer_candidate_email.append(picked_email_id)
    interviewer_candidate_email.append(candidate_email)
    #Fetch interviewers name from the email
    fetch_interviewer_name = Interviewers.query.filter(Interviewers.interviewer_email==picked_email_id).values(Interviewers.interviewer_name)
    for interviewer_name in fetch_interviewer_name:
        chosen_interviewer_name = interviewer_name.interviewer_name
    #Fetch candidate info
    fetch_candidate_name = Candidates.query.filter(Candidates.candidate_email==candidate_email).values(Candidates.candidate_name,Candidates.job_applied)
    for candidate_details in fetch_candidate_name:
        candidate_name = candidate_details.candidate_name
        candidate_job = candidate_details.job_applied
    SUMMARY = candidate_name + '/' + chosen_interviewer_name + '-' + candidate_job
    description = "Round name : "+round_name+'\n\n'+ 'Round description : '+round_description
    create_event_start_time,create_event_end_time = combine_date_and_time(date,selected_slot)
    create_event = gcal.create_event_for_fetched_date_and_time(service,create_event_start_time,create_event_end_time,
    SUMMARY,LOCATION,description,interviewer_candidate_email)
    created_event_info = append_the_create_event_info(create_event,picked_email_id)

    return created_event_info


def get_modified_free_slot_start(free_slot_start,marker):
    "Modifiying the free slot start to 00 or 30"
    if marker == '60' or marker == '90':
        if free_slot_start[-2:]=='00' or free_slot_start[-2:]=='30' or free_slot_start[-2:]=='45':
            modified_free_slot_start = free_slot_start
        elif free_slot_start[-2:] <= '30' and free_slot_start[-2] != '00':
            modified_free_slot_start = '{}:{}'.format(free_slot_start.split(':')[0], '30')
        else:
            free_slot_start = '{}:{}'.format(free_slot_start.split(':')[0], '00')
            modified_free_slot_start = convert_string_into_time(free_slot_start) + timedelta(hours=1)
            modified_free_slot_start = get_datetime_in_time_format(modified_free_slot_start)

    if marker == '45':
        if free_slot_start[-2:]=='00' or free_slot_start[-2:]=='30' or free_slot_start[-2:]=='45':
            modified_free_slot_start = free_slot_start
        elif free_slot_start[-2:] <= '30' and free_slot_start[-2] != '00':
            modified_free_slot_start = '{}:{}'.format(free_slot_start.split(':')[0], '30')
        elif free_slot_start[-2:] > '30'or free_slot_start[-2:] < '45':
            modified_free_slot_start = '{}:{}'.format(free_slot_start.split(':')[0], marker)
        else:
            free_slot_start = '{}:{}'.format(free_slot_start.split(':')[0], '00')
            modified_free_slot_start = convert_string_into_time(free_slot_start) + timedelta(hours=1)
            modified_free_slot_start = get_datetime_in_time_format(modified_free_slot_start)

    if marker == '30':
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
    if marker == '45':
        if free_slot_end[-2:]=='00' or free_slot_end[-2:]==marker :
            modified_free_slot_end = free_slot_end
        elif free_slot_end[-2:] < '30' and free_slot_end[-2] != '00':
            modified_free_slot_end = '{}:{}'.format(free_slot_end.split(':')[0], '00')
        elif free_slot_end[-2:] >= '30'or free_slot_end[-2:] < '45':
            modified_free_slot_end = '{}:{}'.format(free_slot_end.split(':')[0], 30)
        elif free_slot_end[-2:] > marker:
            modified_free_slot_end = '{}:{}'.format(free_slot_end.split(':')[0], marker)

    if marker == '60' or marker == '90':
        if free_slot_end[-2:]=='00' or free_slot_end[-2:]=='30' or free_slot_end[-2]=='45':
            modified_free_slot_end = free_slot_end
        elif free_slot_end[-2:] <'30' and free_slot_end[-2] != '00':
            modified_free_slot_end = '{}:{}'.format(free_slot_end.split(':')[0], '00')
        elif free_slot_end[-2:] > '30':
            free_slot_end = '{}:{}'.format(free_slot_end.split(':')[0], '00')
            modified_free_slot_end = convert_string_into_time(free_slot_end) + timedelta(hours=1)
            modified_free_slot_end = get_datetime_in_time_format(modified_free_slot_end)

    if marker == '30':
        if free_slot_end[-2:]=='00' or free_slot_end[-2:]==marker :
            modified_free_slot_end = free_slot_end
        elif free_slot_end[-2:] < marker:
            modified_free_slot_end = '{}:{}'.format(free_slot_end.split(':')[0], '00')
        elif free_slot_end[-2:] > marker:
            modified_free_slot_end = '{}:{}'.format(free_slot_end.split(':')[0], marker)

    return modified_free_slot_end


def get_chunks_in_slot(modified_free_slot_start,modified_free_slot_end,diff_between_slots_after_modified,interviewer_email_id,CHUNK_DURATION):
    "Divides the free slots into chunks"
    chunk_slots = modified_free_slot_start
    result_flag = True
    idx=0
    time_delta=timedelta(minutes=int(CHUNK_DURATION))
    chunk_slot_list = []
    chunk_time_interval = []
    if diff_between_slots_after_modified == timedelta(minutes=int(CHUNK_DURATION)):
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
            diff_between_slot_start_and_end = convert_string_into_time(modified_free_slot_end) - convert_string_into_time(modified_free_slot_start)
            #While loop should stop if both time become equal
            if modified_free_slot_end == modified_free_slot_start or modified_free_slot_end <= modified_free_slot_start or diff_between_slot_start_and_end < timedelta(minutes=int(CHUNK_DURATION)):
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


def get_free_slots_in_chunks(free_slots,CHUNK_DURATION):
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
                divided_chunk_slots += get_chunks_in_slot(modified_free_slot_start,modified_free_slot_end,diff_between_slots_after_modified,interviewer_email_id,CHUNK_DURATION)
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
    busy_slots = []
    pto_flag = False
    event_organizer_list = []
    if service:
        all_events = gcal.get_events_for_date(service,email_id,fetch_date)
        if all_events:
            for event in all_events:
                event_organizer = event['organizer']['email']
                event_organizer_list.append(event_organizer)
                if 'summary' in event.keys():
                    event_name = event['summary'].split(':')[-1].strip()
                    event_name = event_name.split()[0]
                    if 'PTO'.lower() == event_name.lower():
                        pto_flag = True
                        break
        else:
            pto_flag = True
        if pto_flag:
            busy_slots = gcal.make_day_busy(fetch_date)

        else:
            busy_slots = gcal.get_busy_slots_for_date(service,email_id,fetch_date,timeZone=gcal.TIMEZONE,debug=debug)

    return busy_slots,pto_flag

def get_interviewer_email_id(interviewer_work_time_slots):
    "Parse the email id from the list"
    interviewers_email_id = []
    for each_interviewer_in_row in interviewer_work_time_slots:
        interviewers_email_id.append(each_interviewer_in_row['interviewer_email'])

    return interviewers_email_id


def process_free_slot(fetch_date,day_start_hour,day_end_hour,individual_interviewer_email_id,busy_slots):
    "Process the time"
    processed_free_slots = []
    day_start = process_time_to_gcal(fetch_date,day_start_hour)
    day_end = process_time_to_gcal(fetch_date,day_end_hour)
    free_slots = get_free_slots(busy_slots,day_start,day_end)
    for i in range(0,len(free_slots),2):
        processed_free_slots.append({'start':process_only_time_from_str(free_slots[i]),'end':process_only_time_from_str(free_slots[i+1]),'email_id':individual_interviewer_email_id})

    return processed_free_slots


def get_free_slots_for_date(fetch_date,interviewer_work_time_slots,debug=False):
    "Return a list of free slots for a given date and email"
    final_processed_free_slots = []
    for each_slot in interviewer_work_time_slots:
        individual_interviewer_email_id = each_slot['interviewer_email']
        day_start_hour = each_slot['interviewer_start_time']
        day_end_hour = each_slot['interviewer_end_time']
        busy_slots,pto_flag = get_busy_slots_for_date(individual_interviewer_email_id,fetch_date,debug=debug)
        len_of_busy_slots= len(busy_slots)
        #If the calendar is empty and no pto
        if len_of_busy_slots == 0 and pto_flag == False:
            final_processed_free_slots += process_free_slot(fetch_date,day_start_hour,day_end_hour,individual_interviewer_email_id,busy_slots)
        if len_of_busy_slots >=1:
            final_processed_free_slots += process_free_slot(fetch_date,day_start_hour,day_end_hour,individual_interviewer_email_id,busy_slots)

    return final_processed_free_slots


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
    candidate_email = 'annapoorani@qxf2.com'
    chunk_duration = '30'
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
    free_slots_in_chunks = get_free_slots_in_chunks(free_slots,chunk_duration)
    print("\n======CREATE AN EVENT FOR FETCHED DATE AND TIME=====")
    event_created_slot = create_event_for_fetched_date_and_time(date,emails,candidate_email,selected_slot,round_name,round_description)
    print("The event created,The details are",event_created_slot)