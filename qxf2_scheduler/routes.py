"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app


@app.route("/get-schedule",methods=['GET','POST'])
def date_picker():
    "Dummy page to let you see a schedule"
    if request.method == 'GET':            
            return render_template('get-schedule.html')
    if request.method == 'POST': 
        print("I am coming here",file=sys.stderr)
        email=request.form.get('emailfield')
        date=request.form.get('datefield') 
        if email and date:        
                return render_template('free-available-slot.html')
        

@app.route("/available-free-slot")
def available_free_slot():
    "Returns the available free slot"
    return render_template('free-available-slot.html')
    

@app.route("/")
def index():
    "The index page"
    return "The page is not ready yet"
    