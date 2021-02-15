"""
This class models the interview schedule on candidate side
The form consists of scheduling an interview,checking google link
"""
import os
import sys
import email
from bs4 import BeautifulSoup
#from QA.utils.Wrapit import Wrapit
from QA.utils.email_util import Email_Util
import QA.conf.email_conf as conf_file
#from QA.conf import login_conf as login
#from .Base_Page import Base_Page
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


#Fetching conf details from the conf and login file
imap_host = conf_file.imaphost
username = conf_file.username
password = conf_file.app_password

unique_code = 0
url = "abcd"

class Confirm_Email_Object:
    "Page Object for Scheduling an interview"


    def fetch_email_invite(self):
        "Confirm the email address on the link sent on email"
        imap_host = conf_file.imaphost
        username = conf_file.username
        password = conf_file.app_password

        email_obj = Email_Util()

        url = "abcd"
        unique_code = "0"

        #Connect to the IMAP host
        email_obj.connect(imap_host)
        result_flag = email_obj.login(username, password)
        print(result_flag)

        if result_flag is True:
            result_flag = email_obj.select_folder('Inbox')

        uid = email_obj.get_latest_email_uid(subject="Confirm Your Email Address", sender='careers@qxf2.com', wait_time=20)
        email_body = email_obj.fetch_email_body(uid)
        soup = BeautifulSoup(''.join(email_body), 'html.parser')
        url = soup.a.get('href')

        return url