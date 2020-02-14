"""
This class models the interviewer page.
"""
from .Base_Page import Base_Page
from .interview_scheduler_object import Interview_Scheduler_Object


class Interview_Scheduler_Page(Base_Page,Interview_Scheduler_Object):
    "Page Object for the temperature main page"    
    def start(self):    
        "Use this method to go to specific URL -- if needed"
        url = 'interviewers'
        self.open(url)
        
