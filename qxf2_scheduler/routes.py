"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import utils.verify_gcal_setup as gcal 

@app.route("/get-schedule",methods=['GET','POST'])
def date_picker():
    "Dummy page to let you see a schedule"
    if request.method == 'GET':            
            return render_template('get-schedule.html')
    if request.method == 'POST':         
        email=request.form.get('email')
        date=request.form.get('date') 
        events = gcal.main(email)
        api_response = {"events":events,"email":email}
        return jsonify(api_response)

@app.route("/")
def index():
    "The index page"
    return "The page is not ready yet!"    