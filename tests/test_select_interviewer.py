'''
import unittest
import mock
import datetime
from dateutil.parser import parse
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qxf2_scheduler.qxf2_scheduler import total_busy_slots
from qxf2_scheduler.qxf2_scheduler import total_count_list
from qxf2_scheduler.qxf2_scheduler import pick_interviewer
'''
''' An example of how to mock the sqlite3.connection method '''

from unittest.mock import MagicMock,Mock
import unittest
import sqlite3

class MyTests(unittest.TestCase):

    def test_sqlite3_connect_success(self):

        sqlite3.connect = MagicMock(return_value='connection succeeded')

        dbc = DataBaseClass()
        sqlite3.connect.assert_called_with('test_database')
        self.assertEqual(dbc.connection,'connection succeeded')
'''
#import os
os.environ ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\Qxf2 Services\AppData\Roaming\gcloud\legacy_credentials\test@qxf2.com\adc.json'
import logging

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)


class Total_Busy_Slots(unittest.TestCase):

    date='1/5/2021'
    print("I am in 11")

    print("I am in 12")

    @mock.patch.object(total_busy_slots,'attendee_email_id',return_value=['nilaya@qxf2.com'],create=True )


    @mock.patch.object(total_busy_slots,'date',return_value='1/5/2021',create=True)

    def test_total_busy_slots(self,mockdate,mockattendee_email_id):

        print("I am in 20",mockdate,mockattendee_email_id)


        total_busy_time_list = [datetime.datetime(1900, 1, 1, 1, 30)]
        print("Failed")

        assert total_busy_slots(mockattendee_email_id.return_value,mockdate.return_value)== total_busy_time_list

        print("pass")

    @mock.patch.object(total_count_list,'attendee_email_id',return_value=['nilaya@qxf2.com'],create=True )

    def test_total_count_list(self,mockattendee_email_id):

        total_interview_count_list = [2]

        assert total_count_list(mockattendee_email_id.return_value)== total_interview_count_list

        print("pass")

    @mock.patch.object(pick_interviewer,'attendee_email_id',return_value=['nilaya@qxf2.com','annpoorani@qxf2.com','rohan.j@qxf2.com','avinash@qxf2.com'],create=True )


    @mock.patch.object(pick_interviewer,'date',return_value='1/5/2021',create=True)

    def test_pick_interviewer(self,mockdate,mockattendee_email_id):

        assert pick_interviewer(mockattendee_email_id.return_value,mockdate.return_value)=='rohan.j@qxf2.com'
'''
