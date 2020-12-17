import unittest
import mock
from dateutil.parser import parse
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qxf2_scheduler.qxf2_scheduler import total_busy_slots

class pick_interviewer(unittest.TestCase):

    date='12/22/2020'

    print("I am in 12")

    @mock.patch.object(total_busy_slots,'attendee_email_id',return_value=['namitha.sathyananda@qxf2.com', 'nilaya@qxf2.com', 'dennis.samson@qxf2.com'],create=True )

    @mock.patch.object(total_busy_slots,'date',return_value='12/22/2020',create=True)

    def test_total_busy_slots(self,mockattendee_email_id,mockdate):

        print("I am in 20")

        total_busy_time_list = [datetime.datetime(1900, 1, 1, 1, 15), datetime.datetime(1900, 1, 1, 2, 10), datetime.datetime(1900, 1, 1, 1, 15), datetime.datetime(1900, 1, 1, 1, 25)]

        assert total_busy_slots(mockattendee_email_id.return_value,mockdate.return_value)== total_busy_time_list

        print("pass")
