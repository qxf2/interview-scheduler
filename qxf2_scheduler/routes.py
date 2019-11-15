"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json
import ast

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


@app.route("/jobs/add",methods=["GET","POST"])
def add_job():
    "Add ajob through UI"
    if request.method == 'GET':
        all_interviewers = Interviewers.query.all()
        interviewers_list = []
        for each_interviewer in all_interviewers:           
            interviewers_list.append(each_interviewer.interviewer_name)

        return render_template("add-jobs.html",result=interviewers_list)

    if request.method == 'POST':
        job_role = request.form.get("role")
        data = {'jobrole':job_role}
        #Check the job role exists in database
        check_job_exists = db.session.query(db.exists().where(Jobs.job_role==job_role)).scalar()
       
        #If the job is already in the database send failure
        #If it's not there add the new job role and return success
        if check_job_exists != True:
            interviewers = ast.literal_eval(request.form.get("interviewerlist"))
            job_object = Jobs(job_role=job_role)
            db.session.add(job_object)
            db.session.commit()
            job_id = job_object.job_id
            #Get the id of the user from the interviewers table
            for each_interviewer in interviewers:
                interviewer_id = db.session.query(Interviewers.interviewer_id).filter(Interviewers.interviewer_name==each_interviewer.strip()).scalar()
                print(interviewer_id)        
                job_interviewer_object = Jobinterviewer(job_id=job_id,interviewer_id=interviewer_id)
                db.session.add(job_interviewer_object)
                db.session.commit()
        else:
            return jsonify(message='The job already exists'),500           
                
        return jsonify(data)        


@app.route("/jobs/delete",methods=["POST"]) 
def delete_job():
    "Deletes a job"
    if request.method == 'POST':
        job_id_to_delete = request.form.get('job-id')
        deleted_role = Jobs.query.filter(Jobs.job_id==job_id_to_delete).first()
        data = {'job_role':deleted_role.job_role,'job_id':deleted_role.job_id}       
        db.session.delete(deleted_role)
        db.session.commit()        
        
    return jsonify(data)


@app.route("/interviewers/add",methods=["GET","POST"])
def add_interviewers():
    "Adding the interviewers"
    data={}
    if request.method == 'GET':
        return render_template("add-interviewers.html")
    if request.method == 'POST':              
        try:
            # Adding the name,email,deignation through UI
            interviewer_name = request.form.get('name')
            data = {'interviewer_name':interviewer_name}
            add_interviewers = Interviewers(interviewer_name = request.form.get('name'),interviewer_email = request.form.get('email'),interviewer_designation = request.form.get('designation'))  
            db.session.add(add_interviewers)
            
            # Filtering the interviewer id from the table to use it for interviewertimeslots table
            added_interviewer_id = Interviewers.query.filter(Interviewers.interviewer_name==interviewer_name).first()

            # Adding the time slots in the interviewerstimeslots table                
            interviewer_time_slots = eval(request.form.get('timeObject'))
            interviewer_start_time = interviewer_time_slots['starttime']
            interviewer_end_time = interviewer_time_slots['endtime']            
            len_of_slots=len(interviewer_start_time)
            for i in range(len_of_slots):
                add_time_slots=Interviewertimeslots(interviewer_id=added_interviewer_id.interviewer_id,interviewer_start_time=interviewer_start_time[i],interviewer_end_time=interviewer_end_time[i])
                db.session.add(add_time_slots)

        except Exception as e:
            print(e)               
        
        db.session.commit()
        
        return jsonify(data)    