
import unittest
from unittest.mock import patch
import mock
import datetime
from dateutil.parser import parse
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qxf2_scheduler.qxf2_scheduler import pick_interviewer
from qxf2_scheduler.qxf2_scheduler import total_busy_slots
from qxf2_scheduler.qxf2_scheduler import total_count_list


class pick_interviewer(unittest.TestCase):


    @patch('total_busy_slots')

    @patch('total_count_list')

    def test_pick_interviewer(self,total_count_list,total_busy_slots):

        mock_total_busy_slots.return_value = [2]
        mock_total_count_list.return_value = [datetime.datetime(1900, 1, 1, 1, 15)]
        assert pick_interviewer(['rohan.j@qxf2.com'],'abc')=='rohan.j@qxf2.com'
