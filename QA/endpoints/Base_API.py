"""
A wrapper around Requests to make Restful API calls
"""
from urllib.error import HTTPError
from urllib.error import URLError
import requests


class Base_API:
    "Main base class for Requests based scripts"
    def __init__(self, url=None):
        pass

    def json_or_text(self, response):
        "Class to define text or json response"
        try:
            json_response = response.json()
        except Exception as e:
            if (response.headers["Content-Type"] == 'application/json' or 'text/html'):
                json_response = response.text
            else:
                json_response = None

        return json_response


    def get(self, url, headers={}):
        "Get request"
        json_response = None
        error = {}

        try:
            response = self.request_obj.get(url=url, headers=headers)
            json_response = self.json_or_text(response)
        except (HTTPError, URLError) as e:
            error = e
            if isinstance(e, HTTPError):
                error_message = e.read()
                print("\n******\nGET Error: %s %s" %
                      (url, error_message))
            elif e.reason.args[0] == 10061:
                print("\033[1;31m\nURL open error: Please check if the API server is \
                    up or there is any other issue accessing the URL\033[1;m")
                raise e
            else:
                print(e.reason.args)
                # bubble error back up after printing relevant details
                raise e

        return {'response': response.status_code, 'text':response.text, \
            'json_response':json_response, 'error': error}


    def post(self, url, params=None, data=None, json=None, headers={}):
        "Post request"
        error = {}
        json_response = None
        try:
            response = self.request_obj.post(url, data=data, json=json, headers=headers)
            self.json_or_text(response)
        except (HTTPError, URLError) as e:
            error = e
            if isinstance(e, HTTPError, URLError):
                error_message = e.read()
                print("\n******\nPOST Error: %s %s %s" %
                      (url, error_message, str(json)))
            elif e.reason.args[0] == 10061:
                print("\033[1;31m\nURL open error: Please check if the API server is up \
                     or there is any other issue accessing the URL\033[1;m")
            else:
                print(e.reason.args)
                # bubble error back up after printing relevant details
            raise e

        return {'response': response.status_code, 'text':response.text,\
             'json_response':json_response, 'error': error}


    def delete(self, url, headers={}):
        "Delete request"
        response = False
        error = {}
        try:
            response = self.request_obj.delete(url, headers=headers)
            try:
                json_response = response.json()
            except Exception as e:
                json_response = None

        except (HTTPError, URLError) as e:
            error = e
            if isinstance(e, HTTPError):
                error_message = e.read()
                print("\n******\nPUT Error: %s %s %s" %
                      (url, error_message, str(data)))
            elif e.reason.args[0] == 10061:
                print("\033[1;31m\nURL open error: Please check if the \
                    API server is up or there is any other issue accessing the URL\033[1;m")
            else:
                print(str(e.reason.args))
            # bubble error back up after printing relevant details
            raise e

        return {'response': response.status_code, 'text':response.text, \
            'json_response':json_response, 'error': error}


    def put(self, url, json=None, headers={}):
        "Put request"
        error = {}
        response = False
        try:
            response = self.request_obj.put(url, json=json, headers=headers)
            try:
                json_response = response.json()
            except Exception as e:
                json_response = None


        except (HTTPError, URLError) as e:
            error = e
            if isinstance(e, HTTPError):
                error_message = e.read()
                print("\n******\nPUT Error: %s %s %s" %
                      (url, error_message, str(data)))
            elif e.reason.args[0] == 10061:
                print("\033[1;31m\nURL open error: Please check if \
                    the API server is up or there is any other issue accessing the URL\033[1;m")
            else:
                print(str(e.reason.args))
            # bubble error back up after printing relevant details
            raise e

        return {'response': response.status_code, 'text':response.text, \
            'json_response':json_response, 'error': error}
