"""
This class models the main Selenium tutorial page.
URL: selenium-tutorial-main
The page consists of a header, footer, form and table objects
"""
from .Base_Page import Base_Page
from .form_object import Form_Object
from .index_object import Index_Object
from .candidates_object import Candidates_Object
from .interview_schedule_object import Interview_Schedule_Object


class Candidates_Page(Base_Page, Form_Object, Index_Object, Candidates_Object, Interview_Schedule_Object):
    "Page Object for the tutorial's main page"

    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = '/candidates'
        self.open(url)
