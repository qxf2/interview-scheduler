from flask import render_template, url_for, flash, redirect, jsonify, request, Response,session
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
import qxf2_scheduler.candidate_status as status
from qxf2_scheduler import db
import json
import string
import random,sys
from flask_mail import Message, Mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


mail = Mail(app)

from qxf2_scheduler.models import Candidates,Jobs,Jobcandidate,Jobround,Rounds,Candidateround,Candidatestatus
DOMAIN = 'qxf2.com'
base_url = 'http://localhost:6464/'


def url_gen(candidate_id, job_id):
    "generate random url for candidate"
    s = Serializer('WEBSITE_SECRET_KEY', 60*3600) # 60 secs by 30 mins
    urllist = s.dumps({'candidate_id':candidate_id,'job_id': job_id}).decode('utf-8')
    #KEY_LEN = random.randint(8,16)
    #urllist = [random.choice((string.ascii_letters+string.digits)) for i in range(KEY_LEN)]
    return (f'{candidate_id}/{job_id}/{"".join(urllist)}')


@app.route("/candidates",methods=["GET"])
def read_candidates():
    "Read the candidates"      
    display_candidates = db.session.query(Candidates, Jobs, Jobcandidate).filter(Jobcandidate.job_id == Jobs.job_id, Jobcandidate.candidate_id == Candidates.candidate_id).values(Candidates.candidate_id,Candidates.candidate_name,Candidates.candidate_email,Jobs.job_id,Jobs.job_role)
    
    my_candidates_list = []
    for each_candidate in display_candidates:
        my_candidates_list.append({'candidate_id':each_candidate.candidate_id,'candidate_name':each_candidate.candidate_name,'candidate_email':each_candidate.candidate_email,'job_id':each_candidate.job_id,'job_role':each_candidate.job_role})
    
    return render_template("read-candidates.html",result=my_candidates_list)


@app.route("/candidate/<candidate_id>/delete",methods=["POST"]) 
def delete_candidate(candidate_id):
    "Deletes a candidate"
    if request.method == 'POST':
        candidate_id_to_delete = request.form.get('candidateId')
        job_id_to_delete = request.form.get('jobId')
        #Delete the candidates from candidate table
        candidate_to_delete = Candidates.query.filter(Candidates.candidate_id==candidate_id_to_delete).first()
        data = {'candidate_name':candidate_to_delete.candidate_name,'candidate_id':candidate_to_delete.candidate_id}       
        db.session.delete(candidate_to_delete)
        db.session.commit() 
        #Delete candidate from Jobcandidate table
        job_candidate_to_delete = Jobcandidate.query.filter(Jobcandidate.candidate_id==candidate_id_to_delete, Jobcandidate.job_id==job_id_to_delete).first()
        db.session.delete(job_candidate_to_delete)
        db.session.commit() 
        #Delete candidate from candidateround table
        round_candidate_to_delete = Candidateround.query.filter(Candidateround.candidate_id==candidate_id_to_delete, Candidateround.job_id==job_id_to_delete).first()
        db.session.delete(round_candidate_to_delete)
        db.session.commit()     
        
    return jsonify(data)

    
#Passing the optional parameter through URL
@app.route('/candidate/<job_role>/add')
@app.route("/candidate/add",defaults={'job_role': None},methods=["GET","POST"])
def add_candidate(job_role):
    "Add a candidate"
    data,error = [],None
    job_available = Jobs.query.all()
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
        candidate_email = request.form.get('candidateEmail').lower()
        candidate_job_applied = request.form.get('jobApplied')  
        job_id = Jobs.query.filter(Jobs.job_role == candidate_job_applied).value(Jobs.job_id) 
        data = {'candidate_name':candidate_name}
        #Check the candidate has been already added or not
        check_candidate_exists = db.session.query(db.exists().where(Candidates.candidate_email==candidate_email)).scalar()        
        if check_candidate_exists == True:
            error = "Failed"            
        else:
            add_candidate_object = Candidates(candidate_name=candidate_name,candidate_email=candidate_email)
            db.session.add(add_candidate_object)
            db.session.commit()
            #getting the unique candidate id for new candidate
            candidate_id = Candidates.query.filter(Candidates.candidate_email==candidate_email).value(Candidates.candidate_id)
            # Fetch the id for the candidate status 'Waiting on Qxf2'
            #Fetch the candidate status from status.py file also. Here we have to do the comparison so fetching from the status file
            candidate_status_id = db.session.query(Candidatestatus).filter(Candidatestatus.status_name==status.CANDIDTATE_STATUS[0]).scalar()
           
            #storing the candidate id and job id in jobcandidate table
            add_job_candidate_object = Jobcandidate(candidate_id=candidate_id,job_id=job_id,url='',candidate_status= candidate_status_id.status_id)
            db.session.add(add_job_candidate_object)
            db.session.commit()
            #Store the candidateid,jobid,roundid and round status in candidateround table
            add_round_candidate_object = Candidateround(candidate_id=candidate_id,job_id=job_id,round_id='',round_status='')
            db.session.add(add_round_candidate_object)
            db.session.commit()
            error = "Success"
        api_response = {'data':data,'error':error}

        return jsonify(api_response)


@app.route("/candidate/url",methods=["GET","POST"])
def generate_unique_url():
    candidate_id = request.form.get('candidateId')
    job_id = request.form.get('jobId')
    url_exists = Jobcandidate.query.filter(Jobcandidate.candidate_id==candidate_id,Jobcandidate.job_id==job_id).value(Jobcandidate.url)
    if (url_exists != ''):
        url=url_exists
    else:
        url=url_gen(candidate_id,job_id)
        edit_url = Jobcandidate.query.filter(Jobcandidate.candidate_id==candidate_id,Jobcandidate.job_id==job_id).update({'url': url})
        db.session.commit()
    api_response = {'url': url}
    return jsonify(api_response)


def get_pending_round_id(job_id,candidate_id):
    "Get the pending round id for the candidate"
    pending_round_ids = [] 
    #Fetch all the round details for a job
    round_ids_for_job = Jobround.query.filter(Jobround.job_id==job_id).all()
    for each_round_id in round_ids_for_job:
        #Fetch the round id and round status from candidateround table
        round_status = db.session.query(Candidateround).filter(Candidateround.candidate_id == candidate_id,Candidateround.job_id == job_id).values(Candidateround.round_status,Candidateround.round_id)
        #Check the round has been completed or not
        for each_round_status in round_status:
            if(each_round_status.round_id==each_round_id.round_id and each_round_status.round_status=='Completed'):
                break
            else:
                pending_round_ids.append(each_round_id.round_id)
    
    return pending_round_ids
    
        
@app.route("/candidate/<candidate_id>/job/<job_id>") 
def show_candidate_job(job_id,candidate_id):
    "Show candidate name and job role"
    round_names_list = []
    round_details = {}     
    candidate_job_data = db.session.query(Jobs, Candidates, Jobcandidate).filter(Candidates.candidate_id == candidate_id,Jobs.job_id == job_id,Jobcandidate.candidate_id == candidate_id,Jobcandidate.job_id == job_id).values(Candidates.candidate_name, Candidates.candidate_email,Candidates.date_applied,Jobs.job_role,Jobs.job_id,Candidates.candidate_id,Jobcandidate.url,Jobcandidate.candidate_status,Jobcandidate.interviewer_email)
    for each_data in candidate_job_data:
        data = {'candidate_name':each_data.candidate_name,'job_applied':each_data.job_role,'candidate_id':candidate_id,'job_id':job_id,'url': each_data.url,'candidate_email':each_data.candidate_email,'interviewer_email_id':each_data.interviewer_email,'date_applied':each_data.date_applied}
        candidate_status_id = each_data.candidate_status
        print("I am status id",candidate_status_id)
    #fetch the candidate status name for the status id
    candidate_status_name = db.session.query(Candidatestatus).filter(Candidatestatus.status_id==candidate_status_id).scalar()
    data['candidate_status']=candidate_status_name.status_name
    pending_round_ids = get_pending_round_id(job_id,candidate_id)
    print("data",data)
    #Get the pending round id details from the table
    for each_round_id in pending_round_ids:
        round_detail = db.session.query(Rounds).filter(Rounds.round_id==each_round_id).scalar()
        round_details = {'round_name':round_detail.round_name,'round_id':round_detail.round_id,'round_description':round_detail.round_description,'round_time':round_detail.round_time}
        round_names_list.append(round_details)
    return render_template("candidate-job-status.html",result=data,round_names=round_names_list)


@app.route("/candidate/<candidate_id>/edit",methods=["GET","POST"])
def edit_candidates(candidate_id):
    "Edit the candidtes"    
    #Fetch the candidate details and equal job id    
    if request.method == 'GET':
        jobs_list = []
        candidate_data = {}
        candidate_details = Candidates.query.join(Jobcandidate, Candidates.candidate_id == Jobcandidate.candidate_id) .filter(
                Candidates.candidate_id == candidate_id).values(Candidates.candidate_name, Candidates.candidate_email,Candidates.candidate_id,Jobcandidate.job_id)    
        for each_detail in candidate_details:
            #Fetch the job role of the candidate using job id
            get_job_role = db.session.query(Jobs.job_role).filter(Jobs.job_id==each_detail.job_id).first()        
            candidate_data = {'candidate_name':each_detail.candidate_name,'candidate_email':each_detail.candidate_email,'candidate_id':each_detail.candidate_id,'job_role':get_job_role.job_role,'job_id':each_detail.job_id}
        #Fetch all the Job roles from the Jobs table to edit the job details for the candidate
        job_roles = db.session.query(Jobs.job_role).all()    
        for each_job in job_roles:
            jobs_list.append(each_job.job_role)
        
        candidate_data['job_roles']=jobs_list

        return render_template("edit-candidate.html",result=candidate_data) 

    if request.method == 'POST':
        candidate_name = request.form.get('candidateName')
        candidate_email = request.form.get('candidateEmail')
        candidate_job_applied = request.form.get('jobApplied')
        candidate_old_job = request.form.get('existJob')
        data = {'candidate_name':candidate_name}
        #Check the candidate has been already added or not       
        if (candidate_job_applied == candidate_old_job):
            edit_candidate_object = Candidates.query.filter(Candidates.candidate_id==candidate_id).update({'candidate_name':candidate_name,'candidate_email':candidate_email})            
            db.session.commit()            
        else:
            edit_candidate_object = Candidates.query.filter(Candidates.candidate_id==candidate_id).update({'candidate_name':candidate_name,'candidate_email':candidate_email})            
            db.session.commit()
            edited_job_role = db.session.query(Jobs.job_id).filter(Jobs.job_role==candidate_job_applied).first()
            #storing the candidate id and job id in jobcandidate table
            add_job_candidate_object = Jobcandidate(candidate_id=candidate_id,job_id=edited_job_role.job_id,url='')
            db.session.add(add_job_candidate_object)            
            db.session.commit()            

        api_response = {'data':data}
        return jsonify(api_response)
        

@app.route("/candidates/<candidate_id>/jobs/<job_id>/email")
def send_email(candidate_id,job_id):
    # Fetch the id for the candidate status 'Waiting on Candidate'
    #Fetch the candidate status from status.py file also. Here we have to do the comparison so fetching from the status file
    candidate_status_id = db.session.query(Candidatestatus).filter(Candidatestatus.status_name==status.CANDIDTATE_STATUS[1]).scalar()
           
    candidate_status = Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == job_id).update({'candidate_status':candidate_status_id.status_id})
    db.session.commit()
    candidate_name = Candidates.query.filter(Candidates.candidate_id == candidate_id).value(Candidates.candidate_name)
    if candidate_name != None:
        return jsonify(data=candidate_name)
    else:
        return jsonify(error="error"), 500


@app.route("/candidate/<candidate_id>/job/<job_id>/invite", methods=["GET", "POST"])
def send_invite(candidate_id, job_id):
    "Send an invite to schedule an interview"
    if request.method == 'POST':
        candidate_email = request.form.get("candidateemail")
        candidate_id = request.form.get("candidateid")
        candidate_name = request.form.get("candidatename")
        job_id = request.form.get("jobid")
        generated_url = request.form.get("generatedurl")
        round_description = request.form.get("rounddescription")       
        generated_url = base_url + generated_url +'/welcome'
        try:
            msg = Message("Schedule an Interview with Qxf2 Services!",
                          sender="test@qxf2.com", recipients=[candidate_email])
            msg.body = "Hi %s ,We have received your resume and we are using our scheduler application. You can refer the round description here %s.Please use the URL '%s' to schedule an interview with us" % (
                candidate_name, round_description,generated_url)
            mail.send(msg)
            candidate_status = Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == job_id).update({'candidate_status':'Waiting on candidate'})
            db.session.commit()
            error = 'Success'        
           
        except Exception as e:
            error = "Failed"
            return(str(e))
        
        data = {'candidate_name': candidate_name, 'error': error}

    return jsonify(data)       
