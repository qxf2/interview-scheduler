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
        email = request.form.get('emails')
        date = request.form.get('date')
        schedule_event = my_scheduler.create_event_for_fetched_date_and_time(
            date, email,slot)
        value = {'schedule_event': schedule_event,'date': date}
        value = json.dumps(value)

        return redirect(url_for('confirm', value=value)) 
    return render_template("get-schedule.html")


@app.route("/")
def index():
    "The index page"
    return "The page is not ready yet!"


@app.route("/interviewers")
def listinterviewer():
    "List the interviewer names,designation"
    interviewer_work_time_slots = []
    new_slot = Interviewers.query.join(Interviewertimeslots,Interviewers.interviewer_id==Interviewertimeslots.interviewer_id).values(Interviewers.interviewer_id,Interviewers.interviewer_email,Interviewertimeslots.interviewer_start_time,Interviewertimeslots.interviewer_end_time)
    
    for interviewer_id,interviewer_email,interviewer_start_time,interviewer_end_time in new_slot:        
        interviewer_details = {'interviewer_id':interviewer_id,'interviewer_email':interviewer_email,'interviewer_start_time':interviewer_start_time,
        'interviewer_end_time':interviewer_end_time}        
        if not interviewer_work_time_slots:            
            interviewer_work_time_slots.append(interviewer_details)
        else:
            append_flag = True
            for each_interviewer in interviewer_work_time_slots:                
                if interviewer_details['interviewer_email'] in each_interviewer.values():
                    append_flag = False
                    if type(each_interviewer['interviewer_start_time'])==list:
                        each_interviewer['interviewer_start_time'].append(interviewer_details['interviewer_start_time'])  
                    else:
                        each_interviewer['interviewer_start_time'] = [each_interviewer['interviewer_start_time'], interviewer_details['interviewer_start_time']]                   
                    if type(each_interviewer['interviewer_end_time'])==list:
                        each_interviewer['interviewer_end_time'].append(interviewer_details['interviewer_end_time'])  
                    else:
                        each_interviewer['interviewer_end_time'] = [each_interviewer['interviewer_end_time'], interviewer_details['interviewer_end_time']]
                     
                    break
             
            if append_flag == True:                
                interviewer_work_time_slots.append(interviewer_details)
               
    return render_template("list-interviewer.html", result=interviewer_work_time_slots)    
    

