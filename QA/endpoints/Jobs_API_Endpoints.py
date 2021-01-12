"""
API endpoints for Cars
"""
#!/usr/bin/python -tt
from .Base_API import Base_API

class Jobs_API_Endpoints(Base_API):
    "Class for Jobs endpoints"

    def login_url(self):
        """Append API end point to base URL"""
        return self.base_url+'login'


    def jobs_url(self,suffix=''):
        """Append API end point to base URL"""
        return self.base_url+'jobs'+suffix


    def login_app(self,data):
        """Login to App"""
        url = self.login_url()
        response = self.post(url,data=data)
        return response


    def add_jobs(self,data):
        "Adds a new job"
        url = self.jobs_url('/add')
        response = self.post(url,data=data)
        return {
            'url':url,
            'response':response['response'],
            'response_content': response['json_response']
        }


    def get_jobs(self):
        "gets list of jobs"
        url = self.jobs_url()
        response = self.get(url)
        return {
            'url':url,
            'response': response['response'],
            'response_content': response['json_response']
        }


    def delete_jobs(self,data):
        "Adds a new job"
        url = self.jobs_url('/delete')
        response = self.post(url,data=data)
        return {
            'url':url,
            'response':response['response'],
            'response_content': response['json_response']
        }
