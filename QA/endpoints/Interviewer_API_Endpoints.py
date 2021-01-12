"""
API endpoints for Candidates
"""
#!/usr/bin/python -tt
from .Base_API import Base_API

class Interviewer_API_Endpoints(Base_API):
    "Class for Interviewer endpoints"

    def login_url(self):
        """Append API end point to base URL"""
        return self.base_url+'login'


    def interviewer_url(self,suffix=''):
        """Append API end point to base URL"""
        return self.base_url+'interviewers'+suffix


    def interviewer_delete_url(self,interviewer_id):
        """Append API end point to base URL"""
        return self.base_url+'interviewer/%s/delete'%(interviewer_id)


    def add_interviewer(self,data):
        "Adds a new job"
        url = self.interviewer_url('/add')
        response = self.post(url,data=data)
        return {
            'url':url,
            'response':response['response']
        }


    def get_interviewer(self):
        "gets list of jobs"
        url = self.interviewer_url()
        response = self.get(url)
        return {
            'url':url,
            'response': response['response'],
            'response_content': response['json_response']
        }


    def delete_interviewers(self,interviewer_id,data):
        "Deletes a new interviewer"
        url = self.interviewer_delete_url(interviewer_id)
        response = self.post(url,data=data)
        return {
            'url':url,
            'response':response['response'],
            'response_content': response['json_response']
        }
