"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import sys

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
        if '@' + DOMAIN != email[-9:]:
            api_response = {'error':'This application will only work for emails ending in @{domain}'.format(domain=DOMAIN)}
        elif my_scheduler.is_past_date(date):
            api_response = {'error':'You can only get schedules for today or later.'}
        elif my_scheduler.is_qxf2_holiday(date):
            api_response = {'error':'The date you have provided is a Qxf2 holiday. Please pick another day.'}
        elif my_scheduler.is_weekend(date):
            api_response = {'error':'Qxf2 does not work on weekends. Please pick another day.'}
        else:
            free_slots = my_scheduler.get_free_slots_for_date(email, date)            
            free_slots_in_chunks = my_scheduler.get_free_slots_in_chunks(free_slots)            
            api_response = {'free_slots_in_chunks':free_slots_in_chunks,'email': email, 'date': date}
            

        return jsonify(api_response)


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
    

