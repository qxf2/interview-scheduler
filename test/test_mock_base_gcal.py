"""
This is a unit test to mock the base_gcal method for funtion to check holidays in qxf2_SCHEDULER
"""
import unittest, mock
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qxf2_scheduler.qxf2_scheduler import is_qxf2_holiday
import datetime
 
class Check_Is_qxf2_holiday(unittest.TestCase):
    """
    This class contains unit test for is_qxf2_holiday method in qxf2_scheduler module
    """
    date='03/04/2019'
    
    #Hardcoding the date
    time_mock=datetime.datetime.strptime(date,'%m/%d/%Y')
    
    #mocking gcal.process_date_string method
    @mock.patch('qxf2_scheduler.qxf2_scheduler.gcal.process_date_string',return_value=time_mock)      

    def test_is_qxf2_holiday(self, mockbase_gcal):

        assert is_qxf2_holiday(self.date)==True

        #check if the process_date_string method is called with the specified parameters
        mockbase_gcal.assert_called_once_with(self.date,'%Y-%m-%d')
        
        
        
if __name__=="__main__":
    unittest.main()