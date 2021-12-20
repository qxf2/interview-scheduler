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

    def signup_url(self):
        """Append API end point to base URL"""
        return self.base_url+'registration'

    def jobs_url(self,suffix=''):
        """Append API end point to base URL"""
        return self.base_url+'jobs'+suffix

    def confirm_email_url(self,new_url):
        """Append API end point to base URL"""
        return '%s'%(new_url)

    def confirm_email(self,new_url):
        """confirm email"""
        url = self.confirm_email_url(new_url)
        response = self.get(url)
        return response

    def signup_app(self,data):
        """Login to App"""
        url = self.signup_url()
        response = self.post(url,data=data)
        return response

    def login_app(self,data):
        """Login to App"""
        url = self.login_url()
        response = self.post(url,data=data)
        return response

    def add_jobs(self,data):
        "Adds a new job"
        url = self.jobs_url('/add')
        response = self.post(url,data=data)
        print(response)
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
        "Deletes a new job"
        url = self.jobs_url('/delete')
        response = self.post(url,data=data)
        return {
            'url':url,
            'response':response['response'],
            'response_content': response['json_response']
        }
