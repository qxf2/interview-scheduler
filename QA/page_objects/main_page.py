from .Base_Page import Base_Page
from utils.Wrapit import Wrapit
import conf.locators_conf as locators 

class main_page(Base_Page):
    "Page Object for the main page"
    
    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'get-schedule'
        self.open(url)