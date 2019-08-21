"""
Fetch the actual free slots available for the given date
"""
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import google_api_conf as conf
from .Base_Page import Base_Page

date=conf.date
list_of_free_slots=conf.free_slots_for_10_july_2025

class fetch_actual_list_freetimes(Base_Page):
    """
    This class fetches the actual free time slots for the given date from the configuration file
    """
    def get_actual_free_time(self):
        #this method compare the list of freeslots obtained through google calender  with api response from app and checks if it matches
        
        self.write("The given date is:%s"%date)
        
        #Gets the free slots as seen in google calender
        self.actual_free_slots=list_of_free_slots
        return(self.actual_free_slots)

       

            
    
