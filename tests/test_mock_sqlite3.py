from unittest.mock import MagicMock,Mock
import unittest
import sqlite3

class MyTests(unittest.TestCase):

    def test_sqlite3_connect_success(self):

        sqlite3.connect = MagicMock(return_value='connection succeeded')

        dbc = DataBaseClass()
        sqlite3.connect.assert_called_with('test_database')
        self.assertEqual(dbc.connection,'connection succeeded')