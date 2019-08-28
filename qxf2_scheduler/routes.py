"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json

from qxf2_scheduler.models import Addinterviewer
DOMAIN = 'qxf2.com'


@app.route("/get-schedule", methods=['GET', 'POST'])
def date_picker():
    "Dummy page to let you see a schedule"
    if request.method == 'GET':
        return render_template('get-schedule.html')
    if request.method == 'POST':
        email = request.form.get('email')
        date = request.form.get('date')
        if '@' + DOMAIN != email[-9:]:
            api_response = {
                'error': 'This application will only work for emails ending in @{domain}'.format(domain=DOMAIN)}
        elif my_scheduler.is_past_date(date):
            api_response = {
                'error': 'You can only get schedules for today or later.'}
        elif my_scheduler.is_qxf2_holiday(date):
            api_response = {
                'error': 'The date you have provided is a Qxf2 holiday. Please pick another day.'}
        elif my_scheduler.is_weekend(date):
            api_response = {
                'error': 'Qxf2 does not work on weekends. Please pick another day.'}
        else:
            free_slots = my_scheduler.get_free_slots_for_date(email, date)
            free_slots_in_chunks = my_scheduler.get_free_slots_in_chunks(
                free_slots)
            api_response = {
                'free_slots_in_chunks': free_slots_in_chunks, 'email': email, 'date': date}

        return jsonify(api_response)

@app.route("/confirm")
def confirm():
    "Confirming the event message"
    response_value = request.args['value']   
    return render_template("confirmation.html",value=json.loads(response_value))
        

@app.route("/confirmation", methods=['GET','POST'])
def scehdule_and_confirm():
    "Schedule an event and display confirmation"
    if request.method == 'GET':
       return render_template("get-schedule.html")
    if request.method == 'POST':
        slot = request.form.get('slot')
        email = request.form.get('email')
        date = request.form.get('date')
        schedule_event = my_scheduler.create_event_for_fetched_date_and_time(
            email, date, slot)
        value = {'schedule_event': schedule_event,
                        'email': email, 'date': date}
        value = json.dumps(value)

        return redirect(url_for('confirm', value=value)) 
    return render_template("get-schedule.html")


@app.route("/")
def index():
    "The index page"
    return "The page is not ready yet!"


@app.route("/listinterviewer")
def listinterviewer():
    "List the interviewer names,designation"
    interviewers_list = Addinterviewer.query.all()
    return render_template("list-interviewer.html", result=interviewers_list)
