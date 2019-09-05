"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json

from qxf2_scheduler.models import Interviewers,Interviewertimeslots
DOMAIN = 'qxf2.com'


@app.route("/get-schedule", methods=['GET', 'POST'])
def date_picker():
    "Dummy page to let you see a schedule"
    if request.method == 'GET':
        return render_template('get-schedule.html')
    if request.method == 'POST':        
        date = request.form.get('date')
        new_slot = Interviewers.query.join(Interviewertimeslots,Interviewers.interviewer_id==Interviewertimeslots.interviewer_id).values(Interviewers.interviewer_email,Interviewertimeslots.interviewer_start_time,Interviewertimeslots.interviewer_end_time)
        interviewer_work_time_slots = []
        for interviewer_email,interviewer_start_time,interviewer_end_time in new_slot:
            interviewer_work_time_slots.append({'interviewer_email':interviewer_email,'interviewer_start_time':interviewer_start_time,
            'interviewer_end_time':interviewer_end_time})             
        
        free_slots = my_scheduler.get_free_slots_for_date(date,interviewer_work_time_slots)
        free_slots_in_chunks = my_scheduler.get_free_slots_in_chunks(
            free_slots)
        api_response = {
            'free_slots_in_chunks': free_slots_in_chunks, 'date': date}

        return jsonify(api_response)


@app.route("/confirmation", methods=['GET','POST'])
def scehdule_and_confirm():
    "Schedule an event and display confirmation"
    if request.method == 'GET':
        return render_template("get-schedule.html")
    else:
        new_slot = Interviewers.query.join(Interviewertimeslots,Interviewers.interviewer_id==Interviewertimeslots.interviewer_id).values(Interviewers.interviewer_email,Interviewertimeslots.interviewer_start_time,Interviewertimeslots.interviewer_end_time)
        interviewer_work_time_slots = []
        for interviewer_email,interviewer_start_time,interviewer_end_time in new_slot:
            interviewer_work_time_slots.append({'interviewer_email':interviewer_email,'interviewer_start_time':interviewer_start_time,
            'interviewer_end_time':interviewer_end_time})
        slot = request.form.get('slot')        
        date = request.form.get('date')
        schedule_event = my_scheduler.create_event_for_fetched_date_and_time(
            date, slot,interviewer_work_time_slots)
        api_response = {'schedule_event': schedule_event,
                        'date': date}

    return redirect(url_for('.confirmation', value=value)) 


@app.route("/")
def index():
    "The index page"
    return "The page is not ready yet!"


@app.route("/interviewers")
def listinterviewer():
    "List the interviewer names,designation"
    interviewers_list = Interviewers.query.all()
    return render_template("list-interviewer.html", result=interviewers_list)
