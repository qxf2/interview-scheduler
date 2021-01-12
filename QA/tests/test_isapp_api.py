"""
API test for Interview Scheduler Application
1. Login to Interview Scheduler App - POST request(without url_params)
2. Add a new job - POST request(without url_params)
3. Get the list of jobs - Get request
4. Add a new candidate - POST request(without url_params)
5. Get the list of candidates - Get request
6. Add a new interviewer - POST request(without url_params)
7. Get the list of interviewers - Get request
8. Delete added interviewers - POST request
9. Delete added job - POST request
10. Delete added candidate - POST request
"""
import os
import sys
import pytest
from QA.conf import api_example_conf as conf
from QA.endpoints.API_Player import API_Player
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.API
def test_isapi_example(api_url='http://localhost:6464/'):
    "Run api test"
    try:
        # Create test object
        test_obj = API_Player(url=api_url)

        # set authentication details
        username = conf.user_name
        password_details = conf.password
        job_data = conf.job_details
        candidate_data = conf.candidate_details
        interviewer_data = conf.interviewer_details

        auth_details = test_obj.login_details(username, password_details)

        result_flag = test_obj.login_app(auth_details)
        test_obj.log_result(result_flag,
                            positive='Successfully logged in app %s' % username,
                            negative='Could not login to app %s' % username)


        result_flag = test_obj.add_jobs(job_data)
        test_obj.log_result(result_flag,
                            positive='Successfully added new job with details %s' % job_data,
                            negative='Could not add new job with details %s' % job_data)


        result_flag = test_obj.get_jobs()
        test_obj.log_result(result_flag,
                            positive='Successfully got the list of jobs',
                            negative='Could not get the list of jobs')


        result_flag = test_obj.add_candidates(candidate_data)
        test_obj.log_result(result_flag,
                            positive='Successfully added a new candidate with all details %s'\
                                % candidate_data,
                            negative='Could not add the candidate %s' % candidate_data)


        result_flag = test_obj.get_candidates()
        test_obj.log_result(result_flag,
                            positive='Successfully got the list of candidates',
                            negative='Could not get the list of candidates')


        result_flag = test_obj.add_interviewers(interviewer_data)
        test_obj.log_result(result_flag,
                            positive='Successfully added a new interviewer with all details %s'\
                                % interviewer_data,
                            negative='Could not add the interviewer %s' % interviewer_data)


        result_flag = test_obj.get_interviewers()
        test_obj.log_result(result_flag,
                            positive='Successfully got the list of interviewers',
                            negative='Could not get the list of interviewers')


        result_flag = test_obj.delete_candidates()
        test_obj.log_result(result_flag,
                            positive='Successfully deleted the candidate',
                            negative='Could not delete the candidate')


        result_flag = test_obj.delete_jobs()
        test_obj.log_result(result_flag,
                            positive='Successfully deleted the job',
                            negative='Could not delete the job')


        result_flag = test_obj.delete_interviewers()
        test_obj.log_result(result_flag,
                            positive='Successfully deleted the interviewer',
                            negative='Could not delete the interviewer')

        # write out test summary
        expected_pass = test_obj.total
        actual_pass = test_obj.passed
        test_obj.write_test_summary()

    except Exception as e:
        print(e)




if __name__ == '__main__':
    test_isapi_example()
