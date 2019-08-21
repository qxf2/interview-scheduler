import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.get_list_of_events_google_api import event_list
from conf import google_api_conf as conf
from datetime import datetime,timedelta
import re
import test_fetch_api_response_interviewscheduler

emailid=conf.email_id
mintime=conf.mintime
maxtime=conf.maxtime
date=conf.date

def get_events():
    """
    This function calls the method to fetch the list of events from the utils/get_list_of_events_google_api file
    """
    test_obj=event_list()
    
    #used to fetch the list of events for given email
    list_of_events=test_obj.fetch_events(emailid,mintime,maxtime)
    
    #used to fetch the list of start times and end times of events
    list_of_event_times=test_obj.get_time_of_events(list_of_events)

    return list_of_event_times

def compute_free_time_lots(list_of_event_times):
    """
    This function is used to compute the free time slots from the obtained busy time slots
    """
    #seperate out the start times and the end times from the set
    start_time_list,end_time_list=list_of_event_times
    
    #Format used for date time
    format="%Y-%m-%dT%H:%M:%S+05:30"

    final_freetime_list=[]
    
    #checks if there are no events for the given date 
    if len(start_time_list)==0:
            time_list=[]

            #assign 9:00:00 as the starting time into the list
            time_slots=datetime.strptime("09:00:00","%H:%M:%S")
            time_list.append(datetime.strftime(time_slots,"%H:%M"))

            for each_time_slot in range(16):
                #increment the time in 30 minute intervals
                time_slots=time_slots+timedelta(minutes=30)

                #extract only the hours and minutes from the time and append it to the list
                time_list.append(datetime.strftime(time_slots,"%H:%M"))
            
            #convert datetime to string
            for each_time in time_list:
                final_freetime_list.append(str(each_time))
    else:
        time_slot_list=[]

        #compute the free slots using busy slots
        for start_time,end_time in zip(start_time_list,end_time_list):
                time_difference=end_time-start_time
                time_slot = time_difference+start_time
                time_slot_list.append(time_slot)
                
                while time_slot not in start_time_list:
                        time_slot = time_slot+timedelta(minutes=30)
                        time_slot_list.append(time_slot)

                        #Stop the iteration when time=17:00:00
                        if time_slot == datetime.strptime("2020-06-12T17:00:00+05:30",format):
                                break
        
        #extract only the hours and minute from the datetime object and convert it to string before storing into list
        for each_time_slot in time_slot_list:
                formatted_time=(datetime.strftime(each_time_slot,"%H:%M"))
                final_freetime_list.append(str(formatted_time))
        
            
    return(final_freetime_list)

def compare_events_to_api_response(final_freetime_list):
    #this method compare the list of events obtained through google calender API with api response from app and checks if it matches
    
    print("The given date is:",date)
    
    #prints the free slots obtained through google calender API
    print("\nThe list of free time slots obtained by fetching through Google calender API is:")
    print(final_freetime_list)

    #prints the free slots obtained through API resonse
    free_time_slot=test_fetch_api_response_interviewscheduler.connect_to_website()
    api_response_freetime_slots=test_fetch_api_response_interviewscheduler.get_free_slots(free_time_slot)
    print("\nThe list of free time slots obtained by fetching API response is:")
    print(api_response_freetime_slots)

    result_flag=True
    
    #check if if API response matches with the actual free time slots
    for timeslot_gcal,timeslot_api in zip(final_freetime_list,api_response_freetime_slots):
        if timeslot_gcal != timeslot_api:
            result_flag=False
            break
    if(result_flag==False):
        print("\nThe API response does not match with the fetched free time slots using Google Calender API")
    else:
        print("\nThe API response matches with the actual free time slots. Therefore test is successfull")


        
if __name__=="__main__":
        list_of_event_times=get_events()
        final_free_time_list=compute_free_time_lots(list_of_event_times)
        compare_events_to_api_response(final_free_time_list)
