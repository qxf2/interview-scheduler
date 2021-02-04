"""
API endpoints for Candidates
"""
#!/usr/bin/python -tt
from .Base_API import Base_API

class Candidate_API_Endpoints(Base_API):
    "Class for Jobs endpoints"

    def login_url(self):
        """Append API end point to base URL"""
        return self.base_url+'login'


    def candidates_url(self, suffix=''):
        """Append API end point to base URL"""
        return self.base_url+'candidate'+suffix


    def candidate_url(self, suffix=''):
        """Append API end point to base URL"""
        return self.base_url+'candidates'+suffix


    def candidate_delete_url(self, candidate_id):
        """Append API end point to base URL"""
        return self.base_url+'candidate/%s/delete'%(candidate_id)


    def add_candidates(self, data):
        "Adds a new candidate"
        url = self.candidates_url('/add')
        response = self.post(url, data=data)
        return {
            'url':url,
            'response':response['response'],
            'response_content': response['json_response']
        }


    def get_candidates(self):
        "gets list of candidates"
        url = self.candidate_url()
        response = self.get(url)
        return {
            'url':url,
            'response': response['response'],
            'response_content': response['json_response']
        }


    def delete_candidates(self, candidate_id, data):
        "Deletes a new job"
        url = self.candidate_delete_url(candidate_id)
        response = self.post(url, data=data)
        return {
            'url':url,
            'response':response['response'],
            'response_content': response['json_response']
        }
