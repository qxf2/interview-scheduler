"""
Script to automated Edit Candidate scenario
#Navigate to Login Page
#Populate the username and password and click on Login Button
#User is directed to Home page.Click on List the Candidates link
#User is directed to List Candidates page
#Search the Candidate
#Select the Candidate
#Click on Edit button of the selected Candidate
#Locate Add Comments text box and insert comments
#Click on Edit button

"""
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
from conf import login_conf as conf

@pytest.mark.GUI
def test_edit_candidate(test_obj):
    "Run the test"

    try:
        #Initialize falgs for test summary
        expected_pass= 0
        actual_pass= 1

        #1. Create test object and fill the Login form
        test_obj= PageFactory.get_page_object("login page")

        #Turn on the highlighting feature
        test_obj.turn_on_highlight


        #2. Get the test details from conf file
        username= conf.user_name
        password= conf.password

        comment_candidates = conf.comment_candidates
        search_option_candidate = conf.search_option_candidate

        #3. Enter Username and Password and login to page
        result_flag = test_obj.login_page(username, password)

        test_obj.log_result(result_flag,
                            positive="Successfully logged in the page\n",
                            negative="Failed to login the page \nOn url: %s" \
                            % test_obj.get_current_url(),
                            level="debug")

        #4. Check for Page Heading
        result_flag = test_obj.check_heading()
        test_obj.log_result(result_flag,
                            positive="Heading on the redirect page checks out!\n",
                            negative="Fail: Heading on the redirect page is incorrect!")


        #Click on Candidates Page
        test_obj= PageFactory.get_page_object("candidates page")

        #Search candidate to edit
        result_flag= test_obj.search_candidate(search_option_candidate)
        test_obj.log_result(result_flag,
                            positive="Successfully searched Candidate name\n",
                            negative="Failed to search Candidate name \nOn url: %s"\
                            % test_obj.get_current_url(),
                            level="debug")
        #Click on edit Candidate button
        result_flag= test_obj.edit_candidates()
        test_obj.log_result(result_flag,
                            positive="Successfully clicked the edit Candidate button\n",
                            negative="Failed to click on the edit Candidate button \nOn url: %s"\
                            % test_obj.get_current_url(),
                            level="debug")

        #Edit Candidate comments
        result_flag= test_obj.edit_candidate_comment(comment_candidates)
        test_obj.log_result(result_flag,
                            positive="Successfully edited Candidate comments\n",
                            negative="Failed to edit Candidate comments \nOn url: %s" \
                            % test_obj.get_current_url(),
                            level="debug")


        #Click on Save button after editing candidate
        result_flag= test_obj.save_edited_candidate()
        test_obj.log_result(result_flag,
                            positive="Clicked on Save button of edit candidate page\n",
                            negative="Failed to click on Save button of edit Candidate\
                            page \nOn url: %s" % test_obj.get_current_url(),
                            level="debug")

        test_obj = PageFactory.get_page_object("candidates page")

        #6.Turn off the highlighting feature
        test_obj.turn_off_highlight()

        #7. Print out the result
        test_obj.write_test_summary()
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

    assert expected_pass == actual_pass, "Test failed: %s"%__file__

    #---START OF SCRIPT
if __name__ == '__main__':
    print("Start of %s"%__file__)
    #Creating an instance of the class
    options_obj = Option_Parser()
    options = options_obj.get_options()

    #Run the test only if the options provided are valid
    if options_obj.check_options(options):
        test_obj = PageFactory.get_page_object("Zero", base_url=options.url)

        #Setup and register a driver
        test_obj.register_driver(options.remote_flag, options.os_name,\
        options.os_version, options.browser, options.browser_version,\
        options.remote_project_name, options.remote_build_name)

        #teardowm
        test_obj.wait(3)
        test_obj.teardown()
    else:
        print('ERROR: Received incorrect comand line input arguments')
        print(options_obj.print_usage())
