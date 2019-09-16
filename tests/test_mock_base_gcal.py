"""
This is a unit test to mock the base_gcal method for funtion to check holidays and weekend in qxf2_SCHEDULER
"""
import unittest, mock
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qxf2_scheduler.qxf2_scheduler import is_qxf2_holiday,is_weekend
import datetime
 
class Check_Is_qxf2_holiday(unittest.TestCase):
    """
    This class contains unit test for is_qxf2_holiday method in qxf2_scheduler module
    """
    #date that is a qxf2 holiday
    date='03/04/2019'
    
    #Hardcoding the date in datetime format
    time_mock=datetime.datetime.strptime(date,'%m/%d/%Y')
    
    #mocking gcal.process_date_string method
    @mock.patch('qxf2_scheduler.qxf2_scheduler.gcal.process_date_string',return_value=time_mock)      

    def test_is_qxf2_holiday(self, mockbase_gcal):
        """
        This method tests wether the function displays True if the given date is a qxf2 holiday
        """
        assert is_qxf2_holiday(self.date)==True

    #mocking gcal.process_date_string method   
    @mock.patch('qxf2_scheduler.qxf2_scheduler.gcal.process_date_string',return_value=time_mock) 
    
    def test_parameters(self,mockbase_gcal):
        """
        This method tests wether the funtion is called with the right parameters
        """
        
        is_qxf2_holiday(self.date)
        
        #check if the process_date_string method is called with the specified parameters
        mockbase_gcal.assert_called_once_with(self.date,'%Y-%m-%d')
    
    #date thats not a qxf2 holiday
    date='06/04/2019'
    
    #Hardcoding the date in datetime format
    time_mock=datetime.datetime.strptime(date,'%m/%d/%Y')
    
    #mocking gcal.process_date_string method   
    @mock.patch('qxf2_scheduler.qxf2_scheduler.gcal.process_date_string',return_value=time_mock) 
    
    def test_if_not_qxf2_holiday(self, mockbase_gcal):
        """
        This fuction tests wether the Function diplays false if the given date is not a qxf2 holiday
        """

        #calling the function with the date thats not a holiday 
        assert is_qxf2_holiday(self.date)==False
    
    
    #mocking gcal.process_date_string method   
    @mock.patch('qxf2_scheduler.qxf2_scheduler.gcal.process_date_string',return_value=time_mock) 

    def test_if_date_is_weekend(self,mockbase_gcal):
        """
        This function tests wether the function displays False if given date is not a weekend 
        """

        #Passing a date that is not a weekend to the function
        assert is_weekend(self.date)==False

    #date thats not a qxf2 holiday
    date='11/16/2019'
    
    #Hardcoding the date in datetime format
    time_mock=datetime.datetime.strptime(date,'%m/%d/%Y')

    #mocking gcal.process_date_string method   
    @mock.patch('qxf2_scheduler.qxf2_scheduler.gcal.process_date_string',return_value=time_mock) 

    def test_if_date_is_not_weekend(self,mockbase_gcal):
        """
        This function tests wether the function displays true if given date is a weekend 
        """

        #Passing a date that is a weekend to the function
        assert is_weekend(self.date)==True
        
    
        
        
if __name__=="__main__":
    unittest.main()