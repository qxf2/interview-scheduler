"""
API FACTORIAL TEST

"""
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.get_free_slots_from_api import fetch_api_response
from conf import google_api_conf as conf



def test_api_interview_scheduler():
    "Run api test"
    try:

        expected_pass = 0
        actual_pass = -1
        
        # Create test object
        test_obj = fetch_api_response()

        #fetch the list of actual free time
        actual_freetime_list=conf.actual_free_slots

        #Connect to Interviw scheduler webpage
        api_response=test_obj.connect_to_website()

        #Fetch list of free time slots from API response
        list_freeslots_api_response=test_obj.get_free_slots(api_response)
        
        result_flag=True

        test_obj.write("The actual free slots for the given date are:\n%s"%actual_freetime_list)
        

        test_obj.write("The free slots obtained through API response is:\n%s"%list_freeslots_api_response)
    
        #check if if API response matches with the actual free time slots
        for timeslot_gcal,timeslot_api in zip(actual_freetime_list,list_freeslots_api_response):
            if timeslot_gcal != timeslot_api:
                result_flag=False
                break

        #write the result of test
        test_obj.log_result(result_flag,positive='The API response matches with the actual list of free slots fot the given day',
        negative='The API response does not match with the fetched free time slots using Google Calender API')
       

        # write out test summary
        expected_pass = test_obj.total
        actual_pass = test_obj.passed
        test_obj.write_test_summary()

    except Exception as e:
        test_obj.write("Exception when trying to run test:%s"%__file__)
        test_obj.write("Python says:%s" % str(e))

    # Assertion
    assert expected_pass == actual_pass,"Test failed: %s"%__file__
    

if __name__ == '__main__':
    test_api_interview_scheduler()
   
   
