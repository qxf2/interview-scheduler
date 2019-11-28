from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json

from qxf2_scheduler.models import Candidates,Jobs
DOMAIN = 'qxf2.com'

@app.route("/candidates",methods=["GET"])
def read_candidates():
    "Read the candidates"      
    display_candidates = Candidates.query.all()
    my_candidates_list = []
    for each_candidate in display_candidates:
        my_candidates_list.append({'candidate_id':each_candidate.candidate_id,'candidate_name':each_candidate.candidate_name,'candidate_email':each_candidate.candidate_email,'job_applied':each_candidate.job_applied})
        
    return render_template("read-candidates.html",result=my_candidates_list)


@app.route("/candidate/delete",methods=["POST"]) 
def delete_candidate():
    "Deletes a candidate"
    if request.method == 'POST':
        candidate_id_to_delete = request.form.get('candidate-id')
        candidate_to_delete = Candidates.query.filter(Candidates.candidate_id==candidate_id_to_delete).first()
        data = {'candidate_name':candidate_to_delete.candidate_name,'candidate_id':candidate_to_delete.candidate_id}       
        db.session.delete(candidate_to_delete)
        db.session.commit()        
        
    return jsonify(data)
#Passing the optional parameter through URL
@app.route('/candidate/add/<job_role>')
@app.route("/candidate/add",defaults={'job_role': None},methods=["GET","POST"])
def add_candidate(job_role):
    "Add a candidate"
    data,error = [],None
    if request.method == 'GET':
        available_job_list = []        
        if job_role is None:
            #If the parameter is none then fetch the jobs from the database    
            job_available = Jobs.query.all()            
            for each_job in job_available:
                available_job_list.append(each_job.job_role)               
        else: 
            #Since we have come through the job page pass the exact job role          
            available_job_list.append(job_role)
            
        return render_template("add-candidates.html",data=available_job_list)

    if request.method == 'POST':        
        candidate_name = request.form.get('candidateName')
        candidate_email = request.form.get('candidateEmail')
        candidate_job_applied = request.form.get('jobApplied')        
        data = {'candidate_name':candidate_name}
        #Check the candidate has been already added or not
        check_candidate_exists = db.session.query(db.exists().where(Candidates.candidate_email==candidate_email)).scalar()        
        if check_candidate_exists == True:
            error = "The user already exists in the table"            
        else:
            add_candidate_object = Candidates(candidate_name=candidate_name,candidate_email=candidate_email,job_applied=candidate_job_applied)
            db.session.add(add_candidate_object)
            db.session.commit()

        api_response = {'data':data,'error':error}
        return jsonify(api_response)