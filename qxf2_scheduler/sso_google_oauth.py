"""
A Flask app for Google SSO
"""
import os
from  oauthlib import oauth2
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID =  os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")


DATA = {
        'response_type':"code",
        'redirect_uri': redirect_uri ,
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'client_id':CLIENT_ID,
        'prompt':'consent'}

URL_DICT = {
        # Google OAuth URI
        'google_oauth' : 'https://accounts.google.com/o/oauth2/v2/auth',
        # URI to generate token to access Google API
        'token_gen' : 'https://oauth2.googleapis.com/token',
        # URI to get the user info
        'get_user_info' : 'https://www.googleapis.com/oauth2/v3/userinfo'
        }


CLIENT = oauth2.WebApplicationClient(CLIENT_ID)
REQ_URI = CLIENT.prepare_request_uri(
    uri=URL_DICT['google_oauth'],
    redirect_uri=DATA['redirect_uri'],
    scope=DATA['scope'],
    prompt=DATA['prompt'])