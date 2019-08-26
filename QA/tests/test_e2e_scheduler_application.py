"""
This is a test to check for Scheduler application
"""
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
#import conf.data as conf

def test_e2e_scheduler_application(base_url,browser,browser_version,os_version,os_name,remote_flag):

    "Run the test"
    try:
        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #Create a test object and fill the example form.
        test_obj = PageFactory.get_page_object("main page",base_url=base_url)

        #Setup and register a driver
        test_obj.register_driver(remote_flag,os_name,os_version,browser,browser_version)  
        
        
        


        #Print out the results
        test_obj.write_test_summary()

        #Teardown
        test_obj.wait(3)
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter
        test_obj.teardown()
        
    except Exception as e:
        print("Exception when trying to run test:%s"%__file__)
        print("Python says:%s"%repr(e))

    assert expected_pass == actual_pass, "Test failed: %s"%__file__
       
    
#---START OF SCRIPT   
if __name__=='__main__':
    print("Start of %s"%__file__)
    #Creating an instance of the class
    options_obj = Option_Parser()
    options = options_obj.get_options()
                
    #Run the test only if the options provided are valid
    if options_obj.check_options(options):
        test_e2e_scheduler_application(base_url=options.url,
                        browser=options.browser,
                        browser_version=options.browser_version,
                        os_version=options.os_version,
                        os_name=options.os_name,
                        remote_flag=options.remote_flag                        ) 
    else:
        print('ERROR: Received incorrect comand line input arguments')
        print(options_obj.print_usage())