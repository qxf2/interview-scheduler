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
        response = self.api_obj.add_jobs(data=job_data)
        result_flag = bool(response['response'] == 200)
        return result_flag


    def add_candidates(self, candidate_data):
        "add new candidate"
        response = self.api_obj.add_candidates(data=candidate_data)
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
        self.new_job_id = new_id
        response = self.api_obj.delete_jobs(data={'job-id': self.new_job_id})
        result_flag = bool(response['response'] == 200)

        return result_flag


    def delete_candidates(self):
        "delete candidate"
        response = self.api_obj.get_candidates()
        new_id = self.get_id(response)
        self.new_candidate_id = new_id
        response = self.api_obj.get_jobs()
        new_id = self.get_id(response)
        self.new_job_id = new_id
        response = self.api_obj.delete_candidates(candidate_id=self.new_candidate_id, \
            data={'candidateId':self.new_candidate_id, 'jobId':self.new_job_id})
        result_flag = bool(response['response'] == 200)

        return result_flag


    def delete_interviewers(self):
        "delete interviewers"
        response = self.api_obj.get_interviewer()
        new_id = self.get_id(response)
        self.new_interviewer_id = new_id
        response = self.api_obj.delete_interviewers(interviewer_id=self.new_interviewer_id,\
            data={'interviewer-id':self.new_interviewer_id})
        result_flag = bool(response['response'] == 200)

        return result_flag
