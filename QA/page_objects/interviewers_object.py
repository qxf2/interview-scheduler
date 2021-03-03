"""
This class models the form on the Selenium tutorial page
The form consists of some input fields, a dropdown, a checkbox and a button
"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from .Base_Page import Base_Page


class Interviewers_Object:
    "Page object for the Form"

    #locators
    add_interviewers_button = locators.add_interviewers_button
    interviewers_name = locators.interviewers_name
    interviewers_email = locators.interviewers_email
    interviewers_designation = locators.interviewers_designation
    interviewers_starttime = locators.interviewers_starttime
    interviewers_starttime_drop = locators.interviewers_starttime_drop
    interviewers_endtime = locators.interviewers_endtime
    interviewers_endtime_drop = locators.interviewers_endtime_drop
    add_time_button = locators.add_time_button
    save_interviewers_button = locators.save_interviewers_button
    cancel_interviewers_button = locators.cancel_interviewers_button
    close_interviewers_button = locators.close_interviewers_button
    delete_interviewers_button = locators.delete_interviewers_button
    remove_interviewers_button = locators.remove_interviewers_button
    search_option_interviewer = locators.search_option

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_interviewer(self):
        "Click on 'Add Interviewers' button"
        result_flag = self.click_element(self.add_interviewers_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the "Add Interviewers" button',
                               negative='Failed to click on "Add Interviewers" button',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_name(self, interviewers_name):
        "Set the name on the form"
        result_flag = self.set_text(self.interviewers_name, interviewers_name)
        self.conditional_write(result_flag,
                               positive='Set the name to: %s'% interviewers_name,
                               negative='Failed to set the name in the form',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def alert_accept(self):
        "Click on 'Ok' alert"
        result_flag = self.alert_window()
        return result_flag
        self.conditional_write(result_flag,
                               positive='Clicked on the OK',
                               negative='Failed to click on OK',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_email(self, interviewers_email):
        "Set the email"
        result_flag = self.set_text(self.interviewers_email, interviewers_email)
        self.conditional_write(result_flag,
                               positive='Set the email to: %s'% interviewers_email,
                               negative='Failed to set the email in the form',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_designation(self, interviewers_designation):
        "Set the designation"
        result_flag = self.set_text(self.interviewers_designation, interviewers_designation)
        self.conditional_write(result_flag,
                               positive='Set the designation to: %s'% interviewers_designation,
                               negative='Failed to set the designation in the form',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_starttime(self, interviewers_starttime_drop, wait_seconds=1):
        "Set the starttime on the form"
        result_flag = self.click_element(self.interviewers_starttime)
        self.wait(wait_seconds)
        result_flag &= self.click_element(self.interviewers_starttime_drop%interviewers_starttime_drop)
        self.conditional_write(result_flag,
                               positive='Set the start time to: %s'% interviewers_starttime_drop,
                               negative='Failed to set the start time in the form',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_endtime(self, interviewers_endtime_drop, wait_seconds=1):
        "Set the endtime on the form"
        result_flag = self.click_element(self.interviewers_endtime)
        self.wait(wait_seconds)
        result_flag = self.click_element(self.interviewers_endtime_drop%interviewers_endtime_drop)
        self.conditional_write(result_flag,
                               positive='Set the end time to: %s'% interviewers_endtime_drop,
                               negative='Failed to set the end time in the form',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_time(self):
        "Click on 'Add Interviewers' button"
        result_flag = self.click_element(self.add_time_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the "Add time" button',
                               negative='Failed to click on "Add time" button',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def save_interviewer(self):
        "Click on 'Save Interviewers' button"
        result_flag = self.click_element(self.save_interviewers_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the "Save Interviewers" button',
                               negative='Failed to click on "Save Interviewers" button',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def cancel(self):
        "Click on 'Cancel Interviewers' button"
        result_flag = self.click_element(self.cancel_interviewers_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the "Cancel Interviewers" button',
                               negative='Failed to click on "Cancel Interviewers" button',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def close_interviewer(self):
        "Click on 'Close' button"
        result_flag = self.click_element(self.close_interviewers_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the ok button',
                               negative='Failed to click on ok button',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def delete_interviewers(self):
        "Click on 'Delete Interviewers' button"
        result_flag = self.click_element(self.delete_interviewers_button)
        self.conditional_write(result_flag,
                               positive='Clicked on delete interviewers button',
                               negative='Failed to click on button',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def remove_interviewers(self, search_option_interviewer):
        "Click on 'Delete Interviewers' button"
        self.search_interviewer(search_option_interviewer)
        self.delete_interviewers()
        result_flag = self.click_element(self.remove_interviewers_button)
        self.conditional_write(result_flag,
                               positive='Clicked on remove interviewers button',
                               negative='Failed to click on button',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def search_interviewer(self, search_option_interviewer):
        "Click on 'Search' button"
        result_flag = self.set_text(self.search_option_interviewer, search_option_interviewer)
        self.conditional_write(result_flag,
                               positive='Search for Interviewer name: %s'%search_option_interviewer,
                               negative='Failed to Search for Interviewer name',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_interviewers_details(self, interviewers_name, interviewers_email, interviewers_designation, interviewers_starttime_drop, interviewers_endtime_drop):
        result_flag = self.set_name(interviewers_name)
        result_flag &= self.set_email(interviewers_email)
        result_flag &= self.set_designation(interviewers_designation)
        result_flag &= self.set_starttime(interviewers_starttime_drop)
        result_flag &= self.set_endtime(interviewers_endtime_drop)
        result_flag &= self.save_interviewer()
        result_flag &= self.close_interviewer()

        return result_flag
