import unittest
from unittest.mock import patch
import mock
import datetime
from dateutil.parser import parse
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print(sys.path)

from qxf2_scheduler.qxf2_scheduler import pick_interviewer
#import qxf2_scheduler.qxf2_scheduler as pick_interviewer


# 1. Passing one interviewer so it returns that interviewer only
@patch('qxf2_scheduler.qxf2_scheduler.total_busy_slots',return_value=['datetime.datetime(1900, 1, 1, 1, 15)'])

@patch('qxf2_scheduler.qxf2_scheduler.total_count_list',return_value=[1])

def test_pick_interviewer(mock_total_count_list,mock_total_busy_slots):

    picked_interviewer = pick_interviewer(['rohan.j@qxf2.com'],'abc')
    assert picked_interviewer == 'rohan.j@qxf2.com'


# 2. Minimum busy slots,min interview and Max busy slots max interviewer, so picks minimum interviewer
@patch('qxf2_scheduler.qxf2_scheduler.total_busy_slots',return_value=['datetime.datetime(1900, 1, 1, 1, 15)','datetime.datetime(1900, 1, 1, 2, 30)'])

@patch('qxf2_scheduler.qxf2_scheduler.total_count_list',return_value=[1,10])

def test_pick_interviewer_two(mock_total_count_list,mock_total_busy_slots):

    picked_interviewer = pick_interviewer(['rohan.j@qxf2.com','annapoorani@qxf2.com'],'abc')
    assert picked_interviewer == 'rohan.j@qxf2.com'


# 3. Max busy slots, min interview and min busy slots max interviews, so picks max busy slots ,min interviewer
@patch('qxf2_scheduler.qxf2_scheduler.total_busy_slots',return_value=['datetime.datetime(1900, 1, 1, 2, 30)','datetime.datetime(1900, 1, 1, 1, 15)'])

@patch('qxf2_scheduler.qxf2_scheduler.total_count_list',return_value=[1,10])

def test_pick_interviewer_three(mock_total_count_list,mock_total_busy_slots):

    picked_interviewer = pick_interviewer(['rohan.j@qxf2.com','annapoorani@qxf2.com'],'abc')
    assert picked_interviewer == 'rohan.j@qxf2.com'


# 4. Min slot, max slots but same interview count so picks the min slot interviewer
@patch('qxf2_scheduler.qxf2_scheduler.total_busy_slots',return_value=['datetime.datetime(1900, 1, 1, 1, 15)','datetime.datetime(1900, 1, 1, 1, 30)'])

@patch('qxf2_scheduler.qxf2_scheduler.total_count_list',return_value=[10,10])

def test_pick_interviewer_four(mock_total_count_list,mock_total_busy_slots):

    picked_interviewer = pick_interviewer(['rohan.j@qxf2.com','annapoorani@qxf2.com'],'abc')
    assert picked_interviewer == 'annapoorani@qxf2.com'


# 5.Same busy slots but different interview count so it picks the minimum interview count
@patch('qxf2_scheduler.qxf2_scheduler.total_busy_slots',return_value=['datetime.datetime(1900, 1, 1, 1, 30)','datetime.datetime(1900, 1, 1, 1, 30)'])

@patch('qxf2_scheduler.qxf2_scheduler.total_count_list',return_value=[20,10])

def test_pick_interviewer_six(mock_total_count_list,mock_total_busy_slots):

    picked_interviewer = pick_interviewer(['rohan.j@qxf2.com','annapoorani@qxf2.com'],'abc')
    assert picked_interviewer == 'annapoorani@qxf2.com'


# 6. Max busy slots, min interview and max busy slots max interviews, so picks max busy slots ,min interviewer
@patch('qxf2_scheduler.qxf2_scheduler.total_busy_slots',return_value=['datetime.datetime(1900, 1, 1, 2, 30)','datetime.datetime(1900, 1, 1, 4, 15)'])

@patch('qxf2_scheduler.qxf2_scheduler.total_count_list',return_value=[1,10])

def test_pick_interviewer_five(mock_total_count_list,mock_total_busy_slots):

    picked_interviewer = pick_interviewer(['rohan.j@qxf2.com','annapoorani@qxf2.com'],'abc')
    assert picked_interviewer == 'rohan.j@qxf2.com'
