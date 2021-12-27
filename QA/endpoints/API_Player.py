"""
API_Player class does the following:
a) serves as an interface between the test and API_Interface
b) contains several useful wrappers around commonly used combination of actions
c) maintains the test context/state
"""
import logging
import json
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
        new_job_added = job_data.get("role")
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.new_job_added = new_job_added+''.join(timestr)
        new_job_data = {'role':self.new_job_added}
        job_data.update(new_job_data)
        response = self.api_obj.add_jobs(data=job_data)
        result_flag = bool(response['response'] == 200)
        self.new_job_added = job_data.get("role")
        response = (json.loads(response['text']))
        self.job_id = response['job_id']
        self.jobrole = response['jobrole']

        return result_flag


    def add_candidates(self, candidate_data):
        "add new candidate"
        new_candidate_data = {'jobApplied':self.new_job_added}
        candidate_data.update(new_candidate_data)
        response = self.api_obj.add_candidates(data=candidate_data)
        result_flag = bool(response['response'] == 200)
        self.new_candidate_added = candidate_data.get("candidateName")
        response = (json.loads(response['text']))
        self.candidate_id = response['data']['candidate_id']
        self.candidate_name = response['data']['candidate_name']

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
        self.new_interviewer_added = interviewer_data.get("name")
        response = (json.loads(response['text']))
        self.interviewer_id = response['data']['interviewer_id']
        self.interviewer_name = response['data']['interviewer_name']

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
        self.new_job_added = str(self.new_job_added).strip()
        self.jobrole = str(self.jobrole).strip()
        if (self.new_job_added == self.jobrole):
            response = self.api_obj.delete_jobs(data={'job-id': self.job_id})
            result_flag = bool(response['response'] == 200)
            return result_flag
        else:
            print("new job is not matching to added job, so not deleting the job")
            result_flag = 'False'

        return result_flag


    def delete_candidates(self):
        "delete candidate"
        self.new_candidate_added = str(self.new_candidate_added).strip()
        self.candidate_name = str(self.candidate_name).strip()
        if (self.new_candidate_added == self.candidate_name):
            response = self.api_obj.delete_candidates(candidate_id=self.candidate_id, \
            data={'candidateId':self.candidate_id, 'jobId':self.job_id})
            result_flag = bool(response['response'] == 200)
            return result_flag
        else:
            print("latest candidate is not matching to added candidate so not deleting")
            result_flag = 'False'
            return result_flag


    def delete_interviewers(self):
        "delete interviewers"
        self.new_interviewer_added = str(self.new_interviewer_added).strip()
        self.interviewer_name = str(self.interviewer_name).strip()
        if (self.new_interviewer_added == self.interviewer_name):
                response = self.api_obj.delete_interviewers(interviewer_id=self.interviewer_id,\
                data={'interviewer-id':self.interviewer_id})
                result_flag = bool(response['response'] == 200)
                return result_flag
        else:
                print("Not Matching Interviewer added to Interviewer name")
                result_flag = 'False'
                return result_flag