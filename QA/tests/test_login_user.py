"""
This is an example automated test to help you test interview scheduler application
Our automated test will do the following:
    #Open Login Page of Scheduler App.
    #Enter Login details.
    #Login to app.
    #Logout from app.

"""
import os
import sys
import pytest
from QA.page_objects.PageFactory import PageFactory
import QA.conf.login_conf as conf
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.GUI
def test_login_user(test_obj):

    "Run the test"
    try:
        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #1. Create a test object and fill the login form.
        test_obj = PageFactory.get_page_object("login page")

        # Turn on the highlighting feature
        test_obj.turn_on_highlight()

        #2. Get the test details from the conf file
        email = conf.email
        password = conf.password

        #3. Enter Username and Password and login to page
        result_flag = test_obj.login_page(email, password)
        test_obj.log_result(result_flag,
                            positive="Successfully logged in the page\n",
                            negative="Failed to login the page \nOn url: %s" % \
                                test_obj.get_current_url(),
                            level="debug")


        #4. Checkout for Page Heading
        result_flag = test_obj.check_heading()
        test_obj.log_result(result_flag,
                            positive="Heading on the redirect page checks out!\n",
                            negative="Fail: Heading on the redirect page is incorrect!")


        #5. Logout from application
        result_flag = test_obj.logout_page()
        test_obj.log_result(result_flag,
                            positive="Successfully logged out of the page\n",
                            negative="Failed to logout from the page \nOn url: %s" \
                                % test_obj.get_current_url(),
                            level="debug")


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
        test_obj.register_driver(options.remote_flag, options.os_name, options.os_version,\
             options.browser, options.browser_version, options.remote_project_name, \
                 options.remote_build_name)

        #teardowm
        test_obj.wait(3)
        test_obj.teardown()
    else:
        print('ERROR: Received incorrect comand line input arguments')
        print(options_obj.print_usage())
