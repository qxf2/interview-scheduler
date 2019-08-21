"""
    Fetches the API response from the interview scheduler application
"""
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import fetch_api_interviewscheduler_conf as conf
from utils.Option_Parser import Option_Parser
import requests
import urllib
import json



url=conf.url
emailid=conf.emailid
date=conf.date

class fetch_api_response():
    """
    Class contains methods to connect to the Interview scheduler website and fetch the free time slots from the api response
    """
    def connect_to_website(self):
        #method to for api call to fetch response from webpage
        self.config_details={'email':emailid,'date':date}
        self.api_call=requests.post(url,data=self.config_details)
        self.free_timeslot_list=self.api_call.json()['free_slots_in_chunks']
        return self.free_timeslot_list
        
    def get_free_slots(self,free_timeslot_list): 
        #method to seperate out only the start and end times of the events from the API response
        self.start_time_list=[]
        self.end_time_list=[]

        #iterate through the dictionaries in the list and store the values of the key 'start' and 'end' into separate lists
        for each_time_dict in free_timeslot_list:

            self.start_time_list.append(str(each_time_dict['start']))
            self.end_time_list.append(str(each_time_dict['end']))

        #Join the end time and start times in the list
        self.final_time_list=[self.start_time_list[i]+"-"+self.end_time_list[i] for i in range(0,len(self.start_time_list)-1)]
        return self.final_time_list
 