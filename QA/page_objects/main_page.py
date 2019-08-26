from .Base_Page import Base_Page
from utils.Wrapit import Wrapit
import conf.locators_conf as locators 
from .fetch_api_response_interview_scheduler import fetch_api_response
from .actual_list_of_events import fetch_actual_list_freetimes

class main_page(fetch_actual_list_freetimes,fetch_api_response,Base_Page):
    "Page Object for the main page"
    
    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'get-schedule'
        self.open(url)

    
