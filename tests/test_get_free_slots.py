import unittest
import mock
from dateutil.parser import parse
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qxf2_scheduler.qxf2_scheduler import get_free_slots

class Get_free_slots(unittest.TestCase):
    """
    This class contains unit test for get_free_slots method in qxf2_scheduler module
    """

       
    #mocking busy_slots between day_start and day_end
    @mock.patch.object(get_free_slots,'busy_slots',return_value=[{'start': parse("2019-08-13T14:00:00+05:30"), 'end': parse("2019-08-13T15:00:00+05:30")}],create=True)
    #mocking day start time
    @mock.patch.object(get_free_slots,'day_start',return_value=parse("2019-08-13T10:00:00+05:30"),create=True)
    #mocking day end time
    @mock.patch.object(get_free_slots,'day_end',return_value=parse("2019-08-13T18:00:00+05:30"),create=True)
    def test_busy_slots_between_daystart_and_dayend(self,mockday_end,mockday_start,mockbusy_slots):       
        #This method tests wether the function displays free slots correctly if the busy slot is between day_start and day_end
        
        #hardcoding the free slots that should be displayed by the fuction
        free_slots=[parse("2019-08-13T10:00:00+05:30"),parse("2019-08-13T14:00:00+05:30"),parse("2019-08-13T15:00:00+05:30"),parse("2019-08-13T18:00:00+05:30")]
        
        #comparing the hardcoded free_slots with the actual free_slots obtained by the function
        assert get_free_slots(mockbusy_slots.return_value,mockday_start.return_value,mockday_end.return_value)==free_slots
    

    #mocking busy_slots  
    @mock.patch.object(get_free_slots,'busy_slots',return_value=[{'start': parse("2019-08-13T08:00:00+05:30"), 'end': parse("2019-08-13T09:00:00+05:30")}],create=True)
    #mocking day start time
    @mock.patch.object(get_free_slots,'day_start',return_value=parse("2019-08-13T10:00:00+05:30"),create=True)
    #mocking day end time
    @mock.patch.object(get_free_slots,'day_end',return_value=parse("2019-08-13T18:00:00+05:30"),create=True)
    def test_busy_slots_before_daystart(self,mockday_end,mockday_start,mockbusy_slots):       
        #This method tests wether the function displays free slots correctly if the busy slot is before day_start
        
        #hardcoding the free slots that should be displayed by the fuction
        free_slots=[parse("2019-08-13T10:00:00+05:30"),parse("2019-08-13T18:00:00+05:30")]
        
        #comparing the hardcoded free_slots with the actual free_slots obtained by the function
        assert get_free_slots(mockbusy_slots.return_value,mockday_start.return_value,mockday_end.return_value)==free_slots

    #mocking busy_slots  after the day_end
    @mock.patch.object(get_free_slots,'busy_slots',return_value=[{'start': parse("2019-08-13T18:00:00+05:30"), 'end': parse("2019-08-13T20:00:00+05:30")}],create=True)
    #mocking day start time
    @mock.patch.object(get_free_slots,'day_start',return_value=parse("2019-08-13T10:00:00+05:30"),create=True)
    #mocking day end time
    @mock.patch.object(get_free_slots,'day_end',return_value=parse("2019-08-13T18:00:00+05:30"),create=True)
    def test_busy_slots_after_dayend(self,mockday_end,mockday_start,mockbusy_slots):       
        #This method tests wether the function displays free slots correctly if the busy slot is after day_end
        
        #hardcoding the free slots that should be displayed by the fuction
        free_slots=[parse("2019-08-13T10:00:00+05:30"),parse("2019-08-13T18:00:00+05:30")]
        
        #comparing the hardcoded free_slots with the actual free_slots obtained by the function
        assert get_free_slots(mockbusy_slots.return_value,mockday_start.return_value,mockday_end.return_value)==free_slots
    
    #mocking busy_slot extended beyond day_end
    @mock.patch.object(get_free_slots,'busy_slots',return_value=[{'start': parse("2019-08-13T15:00:00+05:30"), 'end': parse("2019-08-13T19:00:00+05:30")}],create=True)
    #mocking day start time
    @mock.patch.object(get_free_slots,'day_start',return_value=parse("2019-08-13T10:00:00+05:30"),create=True)
    #mocking day end time
    @mock.patch.object(get_free_slots,'day_end',return_value=parse("2019-08-13T18:00:00+05:30"),create=True)
    def test_busy_slots_extended_beyond_dayend(self,mockday_end,mockday_start,mockbusy_slots):       
        #This method tests wether the function displays free slots correctly if the busy slot is extended after day_end
        
        #hardcoding the free slots that should be displayed by the fuction
        free_slots=[parse("2019-08-13T10:00:00+05:30"),parse("2019-08-13T15:00:00+05:30")]
        
        #comparing the hardcoded free_slots with the actual free_slots obtained by the function
        assert get_free_slots(mockbusy_slots.return_value,mockday_start.return_value,mockday_end.return_value)==free_slots
   
    #mocking busy_slot set for entire day
    @mock.patch.object(get_free_slots,'busy_slots',return_value=[{'start': parse("2019-08-13T08:00:00+05:30"), 'end': parse("2019-08-13T19:00:00+05:30")}],create=True)
    #mocking day start time
    @mock.patch.object(get_free_slots,'day_start',return_value=parse("2019-08-13T10:00:00+05:30"),create=True)
    #mocking day end time
    @mock.patch.object(get_free_slots,'day_end',return_value=parse("2019-08-13T18:00:00+05:30"),create=True)
    def test_busy_slot_set_for_entire_day(self,mockday_end,mockday_start,mockbusy_slots):       
        #This method tests wether the function displays free slots correctly if the busy slot covers the entire day.
        
        #hardcoding the free slots that should be displayed by the fuction
        free_slots=[]
        
        #comparing the hardcoded free_slots with the actual free_slots obtained by the function
        assert get_free_slots(mockbusy_slots.return_value,mockday_start.return_value,mockday_end.return_value)==free_slots
    
    #mocking busy_slot that start before day_start but end before day_end
    @mock.patch.object(get_free_slots,'busy_slots',return_value=[{'start': parse("2019-08-13T08:00:00+05:30"), 'end': parse("2019-08-13T11:00:00+05:30")}],create=True)
    #mocking day start time
    @mock.patch.object(get_free_slots,'day_start',return_value=parse("2019-08-13T10:00:00+05:30"),create=True)
    #mocking day end time
    @mock.patch.object(get_free_slots,'day_end',return_value=parse("2019-08-13T18:00:00+05:30"),create=True)
    def test_busy_slot_that_start_before_daystart(self,mockday_end,mockday_start,mockbusy_slots):       
        #This method tests wether the function displays free slots correctly if the busy slot starts befor day_start but end befor day_end.
        
        #hardcoding the free slots that should be displayed by the fuction
        free_slots=[parse("2019-08-13T11:00:00+05:30"),parse("2019-08-13T18:00:00+05:30")]
        
        #comparing the hardcoded free_slots with the actual free_slots obtained by the function
        assert get_free_slots(mockbusy_slots.return_value,mockday_start.return_value,mockday_end.return_value)==free_slots


if __name__=="__main__":
    unittest.main()