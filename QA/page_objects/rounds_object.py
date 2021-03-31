"""
This class models the form on the Selenium tutorial page
The form consists of some input fields, a dropdown, a checkbox and a button
"""

from .Base_Page import Base_Page
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Rounds_Object:
    "Page object for the Rounds"

    #locators
    specific_round_add = locators.specific_round_add
    add_rounds_button = locators.add_rounds_button
    round_name = locators.round_name
    round_duration = locators.round_duration
    round_duration_select = locators.round_duration_select
    round_description = locators.round_description
    round_requirements = locators.round_requirements
    add_button = locators.add_button
    cancel_rounds_button = locators.cancel_rounds_button

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def round_to_job(self):
        "Click on Add Rounds button"
        result_flag = self.click_element(self.specific_round_add)
        self.conditional_write(result_flag,
            positive='Clicked on the Add Rounds button',
            negative='Failed to click on Add Rounds button',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_rounds(self):
        "Click on Add Rounds button"
        result_flag = self.click_element(self.add_rounds_button)
        self.conditional_write(result_flag,
            positive='Clicked on the Add Rounds button',
            negative='Failed to click on Add Rounds button',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_name(self,round_name):
        "Set the name for round"
        result_flag = self.set_text(self.round_name,round_name)
        self.conditional_write(result_flag,
            positive='Set the round name to: %s'% round_name,
            negative='Failed to set the name',
            level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_duration(self,round_duration_select,wait_seconds=1):
        "Set the duration of round"
        result_flag = self.click_element(self.round_duration)
        self.wait(wait_seconds)
        result_flag = self.click_element(self.round_duration_select%round_duration_select)
        self.conditional_write(result_flag,
            positive='Set the round duration to: %s'%round_duration_select,
            negative='Failed to set the round duration',
            level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_description(self,round_description):
        "Set the description"
        result_flag = self.set_text(self.round_description,round_description)
        self.conditional_write(result_flag,
            positive='Set the email to: %s'%round_description,
            negative='Failed to set the email in the form',
            level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_requirements(self,round_requirements):
        "Set the requirements"
        result_flag = self.set_text(self.round_requirements,round_requirements)
        self.conditional_write(result_flag,
            positive='Set the comments to: %s'%round_requirements,
            negative='Failed to set comments',
            level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_add_button(self):
        "Click on Add button"
        result_flag = self.click_element(self.add_button)
        self.conditional_write(result_flag,
            positive='Clicked on the Add button',
            negative='Failed to click on Add button',
            level='debug')
        result_flag = self.alert_accept()

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
    def add_round_details(self,round_name,round_duration_select,round_description,round_requirements):
        "Add round details"
        result_flag = self.add_name(round_name)
        result_flag &= self.add_duration(round_duration_select)
        result_flag &= self.add_description(round_description)
        result_flag &= self.add_requirements(round_requirements)
        result_flag &= self.click_add_button()

        return result_flag
