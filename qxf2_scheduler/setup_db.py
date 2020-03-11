"""
Run this file to setup your database for the first time.
"""
import time
import sys
import sqlite3
import os
import datetime
import csv

CURR_FILEPATH = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURR_FILEPATH)
DATA_DIR = os.path.join(ROOT_DIR,'data')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
DB_FILE = os.path.join(ROOT_DIR,'data','interviewscheduler.db')

STATUS_TABLE = 'Candidatestatus'
STATUS_COL_1 = 'status_id'
STATUS_COL_2 = 'status_name'


def create_connection_obj():
    "Return a connection object"
    return sqlite3.connect(DB_FILE)

def setup_raw_data(db_cursor,csv_file):
    "Setup raw data"
    csv_row_data = get_csv_row_data(csv_file)
    db_cursor.executemany("INSERT INTO {} VALUES (?,?)".format(STATUS_TABLE),csv_row_data)
        
    return db_cursor


def get_csv_row_data(csv_file):
    "Return csv row data in a format suitable for executemany"
    row_data = []
    with open(csv_file,'r') as fp:
        all_rows = csv.DictReader(fp)
        row_data = [(row[STATUS_COL_1], row[STATUS_COL_2]) for row in all_rows]
    
    return row_data

def create_tables(db_cursor):
    "Create the tables"   
    #Status table
    db_cursor.execute("CREATE TABLE IF NOT EXISTS {}({} integer PRIMARY KEY, {} char(256))".format(STATUS_TABLE,STATUS_COL_1,STATUS_COL_2))
    
def create_db(csv_file):
    "Create the database for the first time"
    conn = create_connection_obj()
    db_cursor = conn.cursor()
    create_tables(db_cursor)
    db_cursor = setup_raw_data(db_cursor,csv_file)
    conn.commit()    
    conn.close()
   
def setup_database(csv_file):
    "Setup the database"
    if not os.path.exists(csv_file):
        print("Could not locate the CSV file to load data from: {}".format(csv_file))
        return    
    create_db(csv_file)        
    print("Done")


#----START OF SCRIPT
if __name__=='__main__':
    csv_file = os.path.join(DATA_DIR,'candidatestatus.csv')
    usage = "USAGE:\npython {} <optional: path to csv data>\npython {} ../data/candidatestatus.csv".format(__file__,__file__)
    if len(sys.argv)>1:
        if not os.path.exists(sys.argv[1]):
            print("Could not locate the csv file {}".format(sys.argv[1]))
            print(usage)
        elif not sys.argv[1][-4:]=='.csv':
            print("Please provide a valid CSV file as input")
            print(usage)
        else:
            csv_file = os.path.abspath(sys.argv[1])
    setup_database(csv_file)