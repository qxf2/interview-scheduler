"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json

from qxf2_scheduler.models import Interviewers,Interviewertimeslots,Jobs,Jobinterviewer
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
    

@app.route("/jobs/")
def jobs_page():
    "Displays the jobs page for the interview"    
    display_jobs = Jobs.query.all()
    my_job_list = []
    for each_job in display_jobs:
        my_job_list.append({'job_id':each_job.job_id,'job_role':each_job.job_role})
        
    return render_template("list-jobs.html",result=my_job_list)


@app.route("/<job_id>/interviewers/")
def interviewers_for_roles(job_id):
    "Display the interviewers based on the job id" 
    interviewers_list = []   
    interviewer_list_for_roles = Interviewers.query.join(Jobinterviewer,Interviewers.interviewer_id==Jobinterviewer.interviewer_id).filter(Jobinterviewer.job_id==job_id).values(Interviewers.interviewer_name)
    
    for each_interviewer in  interviewer_list_for_roles:
        interviewers_list.append({'interviewers_name':each_interviewer.interviewer_name})

    return render_template("role-for-interviewers.html",result=interviewers_list)


@app.route("/delete",methods=["POST"]) 
def delete_job():
    "Deletes a job"
    if request.method== 'POST':
        job_id_to_delete = request.form.get('job-id')
        deleted_role = Jobs.query.filter(Jobs.job_id==job_id_to_delete).first()
        data = {'job_role':deleted_role.job_role,'job_id':deleted_role.job_id}       
        db.session.delete(deleted_role)
        db.session.commit()        
        
    return jsonify(data)


@app.route("/interviewers/add",methods=["GET","POST"])
def add_interviewers():
    "Adding the interviewers"
    if request.method == 'GET':
        return render_template("add-interviewers.html")
    if request.method == 'POST':
        """interviewer_id = request.form.get('id')
        interviewer_name = request.form.get('name')
        interviewer_email = request.form.get('email')
        interivewer_designation = request.form.get('designation')"""
        add_interviewers = Interviewers(interviewer_id = request.form.get('id'),interviewer_name = request.form.get('name'),interviewer_email = request.form.get('email'),interivewer_designation = request.form.get('designation'))
        db.session.add(add_interviewers)
        db.session.commit()

        return jsonify(add_interviewers)
    


    