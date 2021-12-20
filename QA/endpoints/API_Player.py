"""
API_Player class does the following:
a) serves as an interface between the test and API_Interface
b) contains several useful wrappers around commonly used combination of actions
c) maintains the test context/state
"""
import logging
from bs4 import BeautifulSoup
from QA.utils.results import Results
from .API_Interface import API_Interface
import time


class API_Player(Results):
    "The class that maintains the test context/state"

    def __init__(self, url, log_file_path=None, session_flag=True):
        "Constructor"
        super(API_Player, self).__init__(
            level=logging.DEBUG, log_file_path=log_file_path)
        self.api_obj = API_Interface(url=url, session_flag=session_flag)


    def login_details(self, username, password):
        "encode auth details"
        user = username
        pass_word = password
        login_data = {'username':user, 'password':pass_word}

        return login_data


    def signup_details(self, username, useremail, userpassword):
        "encode auth details"
        user = username
        pass_word = userpassword
        user_email = useremail
        signup_data = {'username':user, 'useremail':user_email,
        'userpassword':pass_word}

        return signup_data


    def signup_app(self, signup_data):
        "signup user"
        response = self.api_obj.signup_app(data=signup_data)
        result_flag = bool(response['response'] == 200)

        return result_flag


    def accept_signup(self, new_url):
        "accept the email sent after signup"
        response = self.api_obj.confirm_email(new_url)
        result_flag = bool(response['response'] == 200)

        return result_flag


    def login_app(self, login_data):
        "login to app"
        response = self.api_obj.login_app(data=login_data)
        result_flag = bool(response['response'] == 200)

        return result_flag


    def get_list(self, response):
        "to extract list from response"
        ses = response['response_content']
        soup = BeautifulSoup(ses, "html.parser")
        table = soup.find('table', {'class':'table table-striped'})
        table_rows = table.find_all('tr')
        new_list = []
        for t_rows in table_rows:
            cols = t_rows.find_all('td')
            row = [i.text for i in cols]
            new_list.append(row)
        new_list.pop(0)
        new_event_list = []
        for val in new_list:
            new_event_list.append(val[1])
        new_event_list = [element.replace("\n", "") for element in new_event_list]

        return new_event_list


    def get_id(self, response):
        "to extract list from response"
        ses = response['response_content']
        soup = BeautifulSoup(ses, "html.parser")
        table = soup.find('table', {'class':'table table-striped'})
        table_rows = table.find_all('tr')
        for t_rows in table_rows:
            cols = t_rows.find_all('td')
            row = [element.text for element in cols]
        self.new_id = row[0]

        return self.new_id

    def get_new_item(self, response):
        "to extract list from response"
        ses = response['response_content']
        soup = BeautifulSoup(ses, "html.parser")
        table = soup.find('table', {'class':'table table-striped'})
        table_rows = table.find_all('tr')
        for t_rows in table_rows:
            cols = t_rows.find_all('td')
            row = [element.text for element in cols]
        self.new_item = row[1]

        return self.new_item

    def get_jobs(self):
        "get available jobs"
        response = self.api_obj.get_jobs()
        new_event_list = self.get_list(response)
        result_flag = bool(response['response'] == 200)
        self.write(msg="Fetched jobs list:\n %s"%new_event_list)

        self.conditional_write(result_flag,
                               positive="Successfully fetched jobs",
                               negative="Could not fetch jobs")

        return result_flag


    def add_jobs(self, job_data):
        "add new job"
        print(job_data)
        new_job_added = job_data.get("role")
        print(new_job_added)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        print (timestr)
        new_job_added = new_job_added+''.join(timestr)
        print(new_job_added)
        new_job_data = {'role':new_job_added}
        job_data.update(new_job_data)
        print(job_data)
        print("after update dict")
        response = self.api_obj.add_jobs(data=job_data)
        print("inside add jobs")
        result_flag = bool(response['response'] == 200)
        print(job_data)
        new_job_added = job_data.get("role")
        print(new_job_added)
        print("under add jobs")

        return result_flag


    def add_candidates(self, candidate_data):
        "add new candidate"
        response = self.api_obj.add_candidates(data=candidate_data)
        print(response)
        print("under add cand")
        result_flag = bool(response['response'] == 200)

        return result_flag


    def get_candidates(self):
        "get available candidates"
        response = self.api_obj.get_candidates()
        new_event_list = self.get_list(response)

        result_flag = bool(response['response'] == 200)
        self.write(msg="Fetched candidates list:\n %s"%new_event_list)
        self.conditional_write(result_flag,
                               positive="Successfully fetched candidates",
                               negative="Could not fetch candidates")

        return result_flag


    def add_interviewers(self, interviewer_data):
        "add new interviewer"
        response = self.api_obj.add_interviewer(data=interviewer_data)
        result_flag = True if response['response'] == 200 else False

        return result_flag


    def get_interviewers(self):
        "get available interviewers"
        response = self.api_obj.get_interviewer()
        new_event_list = self.get_list(response)

        result_flag = bool(response['response'] == 200)
        self.write(msg="Fetched interviewers list:\n %s"%new_event_list)
        self.conditional_write(result_flag,
                               positive="Successfully fetched interviewers",
                               negative="Could not fetch interviewers")

        return result_flag


    def delete_jobs(self):
        "delete job"
        response = self.api_obj.get_jobs()
        new_id = self.get_id(response)
        new_item = self.get_new_item(response)
        self.new_job_id = new_id
        self.new_job = new_item
        print("inside delete jobs")
        print(self.new_job)
        print(self.new_job_added)
        print("inside delete jobs")
        self.new_job = self.new_job_added
        self.new_job_id = new_id
        self.new_item = str(self.new_item).strip()
        self.new_job = str(self.new_job).strip()
        return_flag = 'True'
        if (self.new_job == self.new_item):
            response = self.api_obj.delete_jobs(data={'job-id': self.new_job_id})
            result_flag = bool(response['response'] == 200)
            return result_flag
        else:
            print("new job is not matching to added job, so not deleting the job")
            result_flag = 'False'

        return result_flag

    def delete_candidates(self):
        "delete candidate"
        response = self.api_obj.get_candidates()
        new_id = self.get_id(response)
        new_item = self.get_new_item(response)
        self.new_candidate_id = new_id
        self.new_candidate = 'test+125'
        response = self.api_obj.get_jobs()
        new_id = self.get_id(response)
        self.new_job_id = new_id
        self.new_item = str(self.new_item).strip()
        self.new_candidate = str(self.new_candidate).strip()
        if (self.new_candidate == self.new_item):
            response = self.api_obj.delete_candidates(candidate_id=self.new_candidate_id, \
            data={'candidateId':self.new_candidate_id, 'jobId':self.new_job_id})
            result_flag = bool(response['response'] == 200)
            return result_flag
        else:
            print("latest candidate is not matching to added candidate so not deleting")
            result_flag = 'False'
            return result_flag


    def delete_interviewers(self):
        "delete interviewers"
        response = self.api_obj.get_interviewer()
        new_id = self.get_id(response)
        new_item = self.get_new_item(response)
        self.new_interviewer = 'nilaya19'
        self.new_interviewer_id = new_id
        self.new_item = str(self.new_item).strip()
        self.new_interviewer = str(self.new_interviewer).strip()
        if (self.new_interviewer == self.new_item):
            response = self.api_obj.delete_interviewers(interviewer_id=self.new_interviewer_id,\
            data={'interviewer-id':self.new_interviewer_id})
            result_flag = bool(response['response'] == 200)
            return result_flag
        else:
            print("Not Matching")
