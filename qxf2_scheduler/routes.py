"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db

from qxf2_scheduler.models import Interviewers,Interviewertimeslots
DOMAIN = 'qxf2.com'


@app.route("/get-schedule", methods=['GET', 'POST'])
def date_picker():
    "Dummy page to let you see a schedule"
    if request.method == 'GET':
        return render_template('get-schedule.html')
    if request.method == 'POST':
        email = request.form.get('email')
        date = request.form.get('date')
        new_slot = Interviewers.query.join(Interviewertimeslots,Interviewers.interviewer_id==Interviewertimeslots.interviewer_id).filter(Interviewers.interviewer_email==email).values(Interviewertimeslots.interviewer_start_time,Interviewertimeslots.interviewer_end_time)
        interviewer_work_time_slots = []
        for interviewer_start_time,interviewer_end_time in new_slot:
            interviewer_work_time_slots.append({'interviewer_start_time':interviewer_start_time,
            'interviewer_end_time':interviewer_end_time})             
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
            free_slots = my_scheduler.get_free_slots_for_date(email, date,interviewer_work_time_slots)
            free_slots_in_chunks = my_scheduler.get_free_slots_in_chunks(
                free_slots)
            api_response = {
                'free_slots_in_chunks': free_slots_in_chunks, 'email': email, 'date': date}

        return jsonify(api_response)


@app.route("/confirmation", methods=['GET','POST'])
def scehdule_and_confirm():
    "Schedule an event and display confirmation"
    if request.method == 'GET':
        return render_template("get-schedule.html")
    else:
        slot = request.form.get('slot')
        email = request.form.get('email')
        date = request.form.get('date')
        schedule_event = my_scheduler.create_event_for_fetched_date_and_time(
            email, date, slot)
        api_response = {'schedule_event': schedule_event,
                        'email': email, 'date': date}

    return render_template('confirmation.html', value=api_response)


@app.route("/")
def index():
    "The index page"
    return "The page is not ready yet!"


@app.route("/interviewers")
def listinterviewer():
    "List the interviewer names,designation"
    interviewers_list = Interviewers.query.all()
    return render_template("list-interviewer.html", result=interviewers_list)
