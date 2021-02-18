"""
A composed interface for all the API objects
Use the API_Player to talk to this class
"""
import requests
from .Base_API import Base_API
from .Jobs_API_Endpoints import Jobs_API_Endpoints
from .Candidate_API_Endpoints import Candidate_API_Endpoints
from .Interviewer_API_Endpoints import Interviewer_API_Endpoints


class API_Interface(Jobs_API_Endpoints, Candidate_API_Endpoints, Interviewer_API_Endpoints):
	"A composed interface for the API objects"

	def __init__(self, url, session_flag=False):
		"Constructor"
		# make base_url available to all API endpoints
		self.request_obj = requests
		if session_flag:
			self.create_session()
		self.base_url = url

	def create_session(self):
		"Create a session object"
		self.request_obj = requests.Session()

		return self.request_obj
