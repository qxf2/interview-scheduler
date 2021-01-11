from qxf2_scheduler import db
import qxf2_scheduler.base_gcal as gcal
import random
import datetime
from datetime import timedelta

from qxf2_scheduler.models import Interviewers, Candidates

TIMEZONE_STRING = '+05:30'
FMT='%H:%M'
#CHUNK_DURATION = '60'
LOCATION =  'Google Hangout or Office',
ATTENDEE = 'annapoorani@qxf2.com'
DATE_TIME_FORMAT = "%m/%d/%Y%H:%M"
from pytz import timezone


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


def create_event_for_fetched_date_and_time(date,interviewer_emails,candidate_email,selected_slot,round_name,round_description):
    "Create an event for fetched date and time"
    service = gcal.base_gcal()
    interviewer_candidate_email = []
    if ',' in interviewer_emails:
        attendee_email_id = interviewer_emails.split(',')
        attendee_email_id = random.choice(attendee_email_id)
    else:
        attendee_email_id = interviewer_emails
    interviewer_candidate_email.append(attendee_email_id)
    interviewer_candidate_email.append(candidate_email)
    #Fetch interviewers name from the email
    fetch_interviewer_name = Interviewers.query.filter(Interviewers.interviewer_email==attendee_email_id).values(Interviewers.interviewer_name)
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
    created_event_info = append_the_create_event_info(create_event,attendee_email_id)

    return created_event_info
