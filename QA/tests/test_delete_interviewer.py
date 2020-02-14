"""

"""
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
import conf.locators_conf as locators
import conf.name_conf 
from utils.Option_Parser import Option_Parser

def test_delete_interviewer(base_url,browser,browser_version,os_version,os_name,remote_flag,remote_project_name,remote_build_name):

    "Run the test"
    try:
    
        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1
        print("Base url:",base_url)

        name = conf.name_conf.name
        
        #1. Create a test object 
        test_obj = PageFactory.get_page_object("List of interviewer details",base_url=base_url)
        
        #2. Setup and register a driver
        start_time = int(time.time())	#Set start_time with current time
        test_obj.register_driver(remote_flag,os_name,os_version,browser,browser_version)
        
        #3. Print the table details
        result_flag = test_obj.print_table_text()
        test_obj.log_result(result_flag,
                            positive="Completed printing table text",
                            negative="Unable to print the table text")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        
        #4.Checking for the name before deletion
        result_flag = test_obj.check_name_present(name)
        test_obj.log_result(result_flag,
                            positive="Located the name %s in the table"%name,
                            negative="The name %s is not present under Interviewer Name column"%name)
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
    
        #5. Deleting the Interviewer name
        result_flag = test_obj.remove_interviewer()

        #4.Checking for the name before deletion
        result_flag = test_obj.check_name_present(name)
        test_obj.log_result(not result_flag,
                            positive="Deleted the name %s from the table"%name,
                            negative="The name %s is still present under Interviewer Name column"%name)
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
    
        #Teardown
        test_obj.wait(3)
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter
        test_obj.teardown()
      
    except Exception as e:
        print("Exception when trying to run test:%s"%__file__)
        print("Python says:%s"%str(e))
   

    assert expected_pass == actual_pass, "Test failed: %s"%__file__
       
    
#---START OF SCRIPT   
if __name__=='__main__':
    print("Start of %s"%__file__)
    #Creating an instance of the class
    options_obj = Option_Parser()
    options = options_obj.get_options()
                
    #Run the test only if the options provided are valid
    if options_obj.check_options(options): 
        test_delete_interviewer(base_url=options.url,
                        browser=options.browser,
                        browser_version=options.browser_version,
                        os_version=options.os_version,
                        os_name=options.os_name,
                        remote_flag=options.remote_flag,
                        remote_project_name=options.remote_project_name,
                        remote_build_name=options.remote_build_name) 
    else:
        print('ERROR: Received incorrect comand line input arguments')
        print(options_obj.print_usage())
