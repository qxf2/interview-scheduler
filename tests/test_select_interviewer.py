
import unittest
from unittest.mock import patch
import mock
import datetime
from dateutil.parser import parse
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qxf2_scheduler.qxf2_scheduler import pick_interviewer



@patch('qxf2_scheduler.qxf2_scheduler.total_busy_slots',return_value=['datetime.datetime(1900, 1, 1, 1, 15)'])

@patch('qxf2_scheduler.qxf2_scheduler.total_count_list',return_value=[1])

def test_pick_interviewer(mock_total_count_list,mock_total_busy_slots):

    picked_interviewer = pick_interviewer(['rohan.j@qxf2.com'],'abc')
    assert picked_interviewer == 'rohan.j@qxf2.com'


@patch('qxf2_scheduler.qxf2_scheduler.total_busy_slots',return_value=['datetime.datetime(1900, 1, 1, 1, 15)','datetime.datetime(1900, 1, 1, 2, 30)'])

@patch('qxf2_scheduler.qxf2_scheduler.total_count_list',return_value=[1,10])

def test_pick_interviewer_two(mock_total_count_list,mock_total_busy_slots):

    picked_interviewer = pick_interviewer(['rohan.j@qxf2.com','annapoorani@qxf2.com'],'abc')
    assert picked_interviewer == 'rohan.j@qxf2.com'

