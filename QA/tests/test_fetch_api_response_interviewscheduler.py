"""
    Fetches the API response from the interview scheduler application
"""
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import fetch_api_interviewscheduler_conf as conf
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
import requests
import urllib
import json



url=conf.url
emailid=conf.emailid
date=conf.date
test_obj = PageFactory.get_page_object("main page",base_url=url)

def connect_to_website():
    #method to for api call to fetch response from webpage
    config_details={'email':emailid,'date':date}
    api_call=requests.post(url,data=config_details)
    free_timeslot_list=api_call.json()['free_slots_in_chunks']
    return free_timeslot_list
        
def get_free_slots(free_timeslot_list): 
    #method to seperate out only the start and end times of the events from the API response
    start_time_list=[]
    end_time_list=[]

    #iterate through the dictionaries in the list and store the values of the key 'start' and 'end' into separate lists
    for each_time_dict in free_timeslot_list:
        start_time_list.append(str(each_time_dict['start']))
        end_time_list.append(str(each_time_dict['end']))

    #combine the start time and end times into a single list
    final_freeslot_list=start_time_list
    for time_slot in end_time_list:
        if time_slot not in final_freeslot_list:
            final_freeslot_list.append(time_slot)
    
    #sort the list in right order 
    set_converted_list=sorted(set(final_freeslot_list))
    final_freeslot_list=list(set_converted_list)
    return final_freeslot_list
    
if __name__=="__main__":
    free_time_slot_list=connect_to_website()
    get_free_slots(free_time_slot_list)