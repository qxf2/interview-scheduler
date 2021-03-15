"""
This class models the form on the Selenium tutorial page
The form consists of some input fields, a dropdown, a checkbox and a button
"""

from .Base_Page import Base_Page
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Jobs_Object:
    "Page object for the Form"

    #locators
    add_jobs_button = locators.add_jobs_button
    job_role = locators.job_role
    job_interviewers = locators.job_interviewers
    submit_job_button = locators.submit_job_button
    delete_job_button = locators.delete_job_button
    remove_job_button = locators.remove_job_button
    search_option_job = locators.search_option


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_jobs(self):
        "Click on 'Add Jobs' button"
        result_flag = self.click_element(self.add_jobs_button)
        self.conditional_write(result_flag,
            positive='Clicked on the "Add Jobs" button',
            negative='Failed to click on "Add Jobs" button',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_job_role(self,job_role):
        "Set the name on the form"
        result_flag = self.set_text(self.job_role,job_role)
        self.conditional_write(result_flag,
            positive='Set the job role to: %s'% job_role,
            negative='Failed to set the job role',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_job_interviewer(self,job_interviewers):
        "Set the name on the form"
        result_flag = self.set_text(self.job_interviewers,job_interviewers)
        self.conditional_write(result_flag,
            positive='Set the email to: %s'% job_interviewers,
            negative='Failed to set the interviewers',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit_job(self):
        "Click on Submit button"
        result_flag = self.click_element(self.submit_job_button)
        self.conditional_write(result_flag,
            positive='Clicked on the "Submit Job" button',
            negative='Failed to click on "Submit Job" button',
            level='debug')
        result_flag = self.alert_accept()

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def delete_job(self):
        "Click on 'Delete Job' button"
        result_flag = self.click_element(self.delete_job_button)
        self.conditional_write(result_flag,
            positive='Clicked on delete job button',
            negative='Failed to click on button',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def remove_job(self,search_option_job):
        "Click on 'Remove Job' button"
        self.search_job(search_option_job)
        self.delete_job()
        result_flag = self.click_element(self.remove_job_button)
        self.conditional_write(result_flag,
            positive='Clicked on remove job button',
            negative='Failed to click on button',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def search_job(self,search_option_job):
        "Click on 'Search' button"
        result_flag = self.set_text(self.search_option_job,search_option_job)
        self.conditional_write(result_flag,
            positive='Search for Job name: %s'%search_option_job,
            negative='Failed to Search for Job name',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_job_details(self,job_role,job_interviewers):
        "Add Job details"
        result_flag = self.set_job_role(job_role)
        result_flag &= self.set_job_interviewer(job_interviewers)
        result_flag &= self.submit_job()

        return result_flag
