"""
This class models the form on the index object page
The form consists of some input fields, a dropdown, a checkbox and a button
"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from .Base_Page import Base_Page


class Index_Object:
    "Page object for the Form"

    #locators
    candidates_page = locators.candidates_page
    interviewers_page = locators.interviewers_page
    jobs_page = locators.jobs_page
    heading = locators.heading

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def check_heading(self):
        "Check if the heading exists"
        result_flag = self.check_element_present(self.heading)
        self.conditional_write(result_flag,
                               positive='Correct heading present on index page',
                               negative='Heading on index page is INCORRECT!!',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_ok(self):
        "Accept the terms and conditions"
        alert = self.click_element(self.name)
        alert.accept()
        self.conditional_write(result_flag,
                               positive='Accepted the terms and conditions',
                               negative='Failed to accept the terms and conditions',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def link_to_interviewers_page(self):
        "Open the interviewers page"
        result_flag = self.click_element(self.interviewers_page)
        self.conditional_write(result_flag,
                               positive='Clicked on Interviewers Page',
                               negative='Failed to click on Interviewers Page',
                               level='debug')

        return result_flag