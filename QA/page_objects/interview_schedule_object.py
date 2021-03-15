"""
This class models the interview schedule on candidate side
The form consists of scheduling an interview,checking google link
"""
import os
import sys
import email
import datetime
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from utils.email_util import Email_Util
import conf.email_conf as conf_file
from conf import login_conf as login
from .Base_Page import Base_Page
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


#Fetching conf details from the conf and login file
imap_host = conf_file.imaphost
username = conf_file.username
password = conf_file.app_password
email = login.email_candidates
date_picker = login.date_picker
date_check = login.date_check
free_slot = login.free_slot
email_on_link = login.email_on_link
password_link = login.password_link

N_DAYS_After = 7


class Interview_Schedule_Object:
    "Page Object for Scheduling an interview"

    #locators
    select_url = locators.select_url
    select_unique_code = locators.select_unique_code
    select_candidate_email = locators.select_candidate_email
    go_for_schedule = locators.go_for_schedule
    date_picker = locators.date_picker
    confirm_interview_date = locators.confirm_interview_date
    select_free_slot = locators.select_free_slot
    schedule_my_interview = locators.schedule_my_interview
    date_on_calendar = locators.date_on_calendar
    calendar_link = locators.calendar_link
    google_meet_link = locators.google_meet_link
    email_on_link = locators.email_on_link
    next_button = locators.next_button
    next_button_after_password = locators.next_button_after_password
    password_link = locators.password_link

    url = "abcd"
    unique_code = 0


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def fetch_email_invite(self):
        "Get email contents and fetch URL and unique code and schedule an interview"
        imap_host = conf_file.imaphost
        username = conf_file.username
        password = conf_file.app_password

        unique_code = 0
        email_obj = Email_Util()

        #Connect to the IMAP host
        email_obj.connect(imap_host)
        result_flag = email_obj.login(username, password)
        self.conditional_write(result_flag,
                               positive='Logged into %s' % imap_host,
                               negative='Could not log into %s to fetch the activation email' % imap_host,
                               level='debug')
        self.wait(30)
        if result_flag is True:
            result_flag = email_obj.select_folder('Inbox')
            self.conditional_write(result_flag,
                                   positive='Selected the folder Inbox',
                                   negative='Could not select the folder Inbox',
                                   level='critical')
        uid = email_obj.get_latest_email_uid(subject="Invitation to schedule an Interview with Qxf2 Services!", sender='careers@qxf2.com', wait_time=20)
        email_body = email_obj.fetch_email_body(uid)
        soup = BeautifulSoup(''.join(email_body), 'html.parser')
        unique_code = soup.b.text
        url = soup.a.get('href')

        result_flag = self.open_invitation_url(url)
        result_flag = self.set_unique_code(unique_code)
        result_flag = self.set_candidate_email(email)
        result_flag = self.click_interview_schedule()
        result_flag = self.get_the_date()
        result_flag = self.set_the_date()
        result_flag = self.confirm_the_date()
        result_flag = self.scroll_down_page()
        result_flag = self.slot_selection()
        result_flag = self.scheduling_interview()
        result_flag = self.checking_interview_meet_link()

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def open_invitation_url(self, url):
        "Open invitation url in new tab"
        print(self.url)
        result_flag = self.open_url_new_tab(self.url)
        self.conditional_write(result_flag,
                               positive='Opened the new tab with link',
                               negative='Failed to open the new tab with link',
                               level='critical')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_unique_code(self, unique_code):
        "Setting unique code on url invitation"
        result_flag = self.set_text(self.select_unique_code, unique_code)
        self.conditional_write(result_flag,
                               positive='Set unique code  to: %s'% unique_code,
                               negative='Failed to set the unique code',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_candidate_email(self, email):
        "Setting email on url invitation"
        result_flag = self.set_text(self.select_candidate_email, email)
        self.conditional_write(result_flag,
                               positive='Set candidate email to: %s'% email,
                               negative='Failed to set the email',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_interview_schedule(self):
        "Click on INterview Schedule button"
        result_flag = self.click_element(self.go_for_schedule)
        self.conditional_write(result_flag,
                               positive='Clicked on Scheduling interview button',
                               negative='Failed to click on Scheduling interview button',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_the_date(self):
        " Getting the date on calendar"
        result_flag = self.click_element(self.date_picker)
        self.conditional_write(result_flag,
                               positive='Get the date',
                               negative='Failed to get the date',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_the_date(self):
        "Setting the date on calendar"
        date = datetime.now()
        date = date + timedelta(days=N_DAYS_After)
        self.date = date.day
        result_flag = self.click_element(self.date_on_calendar%self.date)
        self.conditional_write(result_flag,
                               positive='Set the date',
                               negative='Failed to set the date',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def confirm_the_date(self):
        "Confirm the date"
        result_flag = self.click_element(self.confirm_interview_date)
        self.conditional_write(result_flag,
                               positive='Clicked on confirming interview date',
                               negative='Failed to click on confirming interview date',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def scroll_down_page(self):
        "Scrolling down the page to show all available time slots for an interview"
        result_flag = self.scroll_down(self.confirm_interview_date)
        self.conditional_write(result_flag,
                               positive='Scrolling down the page till Schedule my interview option',
                               negative='Failed to scroll down the page till schedule my interview option',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def slot_selection(self):
        "Select the interview slot"
        result_flag = self.click_element(self.select_free_slot)
        self.conditional_write(result_flag,
                               positive='Selected free interview slot',
                               negative='Failed to select free interview slot',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def scheduling_interview(self):
        "Schedule an interview"
        result_flag = self.click_element(self.schedule_my_interview)
        self.conditional_write(result_flag,
                               positive='Clicked on schedule my interview',
                               negative='Failed to click on schedule my interview',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_calendar_link(self):
        "Click on calendar link on confirmation page"
        self.wait(5)
        result_flag = self.click_element(self.calendar_link)
        self.conditional_write(result_flag,
                               positive='Clicked on calendar link',
                               negative='Failed to click on calendar link',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_the_email(self, email_on_link):
        "set email to check google link"
        self.wait(2)
        self.switch_window()
        result_flag = self.set_text(self.email_on_link, email_on_link)
        self.conditional_write(result_flag,
                               positive='Set email to: %s'% email_on_link,
                               negative='Failed to set the email',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_next_button(self):
        "Click next button"
        result_flag = self.click_element(self.next_button)
        self.conditional_write(result_flag,
                               positive='Clicked on Next',
                               negative='Failed to click on Next',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_the_password_link(self, password_link):
        "Set password on link"
        self.wait(5)
        result_flag = self.set_text(self.password_link, password_link)
        self.conditional_write(result_flag,
                               positive='Set password to: %s'% password_link,
                               negative='Failed to set the password',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_next_after_password(self):
        "Click on next button after password"
        result_flag = self.click_element(self.next_button_after_password)
        self.conditional_write(result_flag,
                               positive='Clicked on Next',
                               negative='Failed to click on Next',
                               level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_google_meet_link(self):
        "Click on google link"
        result_flag = self.click_element(self.google_meet_link)
        self.conditional_write(result_flag,
                               positive='Clicked on Google meet link',
                               negative='Failed to click on Google meet link',
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
    def checking_interview_meet_link(self):
        "Scheduling an interview by candidate"
        result_flag = self.click_calendar_link()
        result_flag = self.set_the_email(email_on_link)
        result_flag = self.click_next_button()
        result_flag = self.set_the_password_link(password_link)
        result_flag = self.click_next_after_password()
        result_flag = self.click_google_meet_link()

        return result_flag
