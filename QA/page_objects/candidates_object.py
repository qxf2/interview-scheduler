"""
This class models the form on candidates page
The form consists of some input fields, a dropdown, a checkbox and a button to submit candidate details
"""
import os
import sys
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
import conf.login_conf as login
from .Base_Page import Base_Page
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#Fetching conf details from the conf file
email = login.email_candidates

class Candidates_Object:
    "Page object for the Candidates"

    #locators
    add_candidates_button = locators.add_candidates_button
    name_candidates = locators.name_candidates
    email_candidates = locators.email_candidates
    job_applied = locators.job_applied
    job_applied_select = locators.job_applied_select
    comment_candidates = locators.comment_candidates
    submit_candidates_button = locators.submit_candidates_button
    delete_candidates_button = locators.delete_candidates_button
    remove_candidates_button = locators.remove_candidates_button
    select_candidate_button = locators.select_candidate_button
    search_option_candidate = locators.search_option
    thumbs_up_button = locators.thumbs_up_button
    thumbs_down_button = locators.thumbs_down_button
    select_round_level_scroll = locators.select_round_level_scroll
    send_email_button = locators.send_email_button
    edit_candidate_button = locators.edit_candidate_button
    edit_candidate_page_save_button = locators.edit_candidate_page_save_button


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_candidates(self):
        "Click on Add Candidates button"
        result_flag = self.click_element(self.add_candidates_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the Add Candidates button',
                               negative='Failed to click on Add Candidates button',
                               level='debug')

        return result_flag

   

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_name(self, name_candidates):
        "Set the name for candidate"
        result_flag = self.set_text(self.name_candidates, name_candidates)
        self.conditional_write(result_flag,
                               positive='Set the  candidates name to: %s'% name_candidates,
                               negative='Failed to set the name',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_email(self, email_candidates):
        "Set the email for the candidate"
        result_flag = self.set_text(self.email_candidates, email_candidates)
        self.conditional_write(result_flag,
                               positive='Set the email to: %s'%email_candidates,
                               negative='Failed to set the email in the form',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_job_applied(self, job_applied_select, wait_seconds=1):
        "Set the email on the form"
        result_flag = self.click_element(self.job_applied)
        self.wait(wait_seconds)
        result_flag = self.click_element(self.job_applied_select%job_applied_select)
        self.conditional_write(result_flag,
                               positive='Set the email to: %s'%job_applied_select,
                               negative='Failed to set the email in the form',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_comments(self, comment_candidates):
        "Set the email on the form"
        result_flag = self.set_text(self.comment_candidates, comment_candidates)
        self.conditional_write(result_flag,
                               positive='Set the comments to: %s'%comment_candidates,
                               negative='Failed to set comments',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit(self):
        "Click on 'Submit' button"
        result_flag = self.click_element(self.submit_candidates_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the Submit button',
                               negative='Failed to click on Submit button',
                               level='debug')
        result_flag = self.alert_accept()

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_candidate_details(self, name_candidates, email_candidates, job_applied_select, comment_candidates):
        "Add all candidate details"
        result_flag = self.add_name(name_candidates)
        result_flag &= self.add_email(email_candidates)
        result_flag &= self.add_job_applied(job_applied_select)
        result_flag &= self.add_comments(comment_candidates)
        result_flag &= self.submit()

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def search_candidate(self, search_option_candidate):
        "Click on 'Search' button"
        result_flag = self.set_text(self.search_option_candidate, search_option_candidate)
        self.conditional_write(result_flag,
                               positive='Search for Candidate name: %s'%search_option_candidate,
                               negative='Failed to Search for Candidate name',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def delete_candidates(self):
        "Click on Delete Candidates button"
        result_flag = self.click_element(self.delete_candidates_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the Delete Candidates button',
                               negative='Failed to click on Delete Candidates button',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def remove_candidates(self, search_option_candidate):
        "Click on Remove Candidates button"
        self.search_candidate(search_option_candidate)
        self.delete_candidates()
        result_flag = self.click_element(self.remove_candidates_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the Remove Candidates button',
                               negative='Failed to click on Remove Candidates button',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def select_candidates(self):
        "Click on Select Candidates button"
        result_flag = self.click_element(self.select_candidate_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the Select Candidates button',
                               negative='Failed to click on Select Candidates button',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def thumbs_up(self):
        "Click on thumbs up button"
        result_flag = self.click_element(self.thumbs_up_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the thumbs up button',
                               negative='Failed to click on thumbs up button',
                               level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def thumbs_down(self):
        "Click on thumbs up button"
        result_flag = self.click_element(self.thumbs_down_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the thumbs down button',
                               negative='Failed to click on thumbs down button',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def select_round(self, select_round_level):
        "Set the name for round"
        result_flag = self.set_text(self.select_round_level_scroll, select_round_level)
        self.conditional_write(result_flag,
                               positive='Set the round to: %s'% select_round_level,
                               negative='Failed to set the round',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def send_email(self):
        "Click on send email button"
        result_flag = self.click_element(self.send_email_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the send email button',
                               negative='Failed to click on send email button',
                               level='debug')
        result_flag = self.alert_accept()

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def send_email_candidate(self, search_option_candidate, select_round_level):
        "Search candidate,select, thumbs up, select round level, send email to candidate "
        result_flag = self.search_candidate(search_option_candidate)
        result_flag &= self.select_candidates()
        result_flag &= self.thumbs_up()
        result_flag &= self.select_round(select_round_level)
        result_flag &= self.send_email()

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
    def edit_candidates(self):
        "Click on edit button of Candidates page"
        result_flag = self.click_element(self.edit_candidate_button)
        self.conditional_write(result_flag,
                                positive= 'Clicked on Edit Candidates link',
                                negative= 'Failed to click on Edit Candidates link',
                                level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def edit_candidate_comment(self, comment_candidates):
        "Edit the comments of Candidate"
        result_flag = self.set_text(self.comment_candidates, comment_candidates, clear_flag=False)
        self.conditional_write(result_flag,
                               positive='Edit the comments to: %s'%comment_candidates,
                               negative='Failed to edit comments',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def save_edited_candidate(self):
        "Click the Save button to save changes applied for te candidate"
        result_flag = self.click_element(self.edit_candidate_page_save_button)
        self.conditional_write(result_flag,
                                positive= 'Click save button after editing candidate',
                                negative='Failed to click on save button after editing candidate',
                                level='debug')
        result_flag = self.alert_accept()
        return result_flag