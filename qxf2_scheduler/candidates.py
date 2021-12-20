import datetime
from flask import render_template, jsonify, request, session
from flask_mail import Message, Mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from qxf2_scheduler import app
import qxf2_scheduler.candidate_status as status
from qxf2_scheduler.authentication_required import Authentication_Required
from qxf2_scheduler import db
from sqlalchemy import or_
import os

mail = Mail(app)

from qxf2_scheduler.models import Candidates, Jobs, Jobcandidate, Jobround, Rounds, Candidateround, Candidatestatus, Candidateinterviewer
DOMAIN = 'qxf2.com'
base_url = 'https://staging-interview-scheduler.qxf2.com/'

def get_end_business_day(add_days, from_date):
    "calcuate the five business days"
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5: # sunday = 6
            continue
        business_days_to_add -= 1

    return current_date

def get_hours_between(end_date, current_date):
    "calculate the hours between two dates"
    diff_between_dates = end_date - current_date
    days, seconds = diff_between_dates.days, diff_between_dates.seconds
    hours_between_dates = days * 24 + seconds // 3600

    return hours_between_dates


def url_gen(candidate_id, job_id):
    "generate random url for candidate"
    num_business_days = 5
    current_date = datetime.datetime.now()
    end_business_day = get_end_business_day(num_business_days, current_date)
    num_hours = get_hours_between(end_business_day, current_date)
    s = Serializer('WEBSITE_SECRET_KEY', num_hours*3600) # 60 secs by 30 mins
    urllist = s.dumps({'candidate_id':candidate_id, 'job_id': job_id}).decode('utf-8')
    return f'{candidate_id}/{job_id}/{"".join(urllist)}',end_business_day


@app.route("/regenerate/url", methods=["GET", "POST"])
def regenerate_url():
    "Regenerate URL"
    if request.method == 'POST':
        try:
            candidate_id = request.form.get("candidateid")
            job_id = request.form.get("jobid")
            Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == job_id).update({'url':'','candidate_status':'1'})
            db.session.commit()
            get_round_id = Candidateround.query.filter(Candidateround.candidate_id == candidate_id, Candidateround.job_id == job_id, Candidateround.round_status == 'Invitation Sent').values(Candidateround.round_id)
            for unique_round_id in get_round_id:
                sent_round_id = unique_round_id.round_id
            db.session.query(Candidateround).filter(Candidateround.candidate_id == candidate_id,Candidateround.job_id == job_id, Candidateround.round_id == sent_round_id).delete()
            db.session.commit()
            error = 'Success'
        except Exception as e:
            print(e)
            error = "error"

    data = {'candidate_id':candidate_id, 'job_id':job_id, 'error':error}

    return jsonify(data)

def fetch_candidate_list(candidate_list_object):
    "Fetch the candidate list"
    my_candidates_list = []
    for each_candidate in candidate_list_object:
        candidate_status_object = Candidatestatus.query.filter(Candidatestatus.status_id == each_candidate.candidate_status).values(Candidatestatus.status_name)
        for candidate_status in candidate_status_object:
            candidate_status = candidate_status.status_name

        my_candidates_list.append({'candidate_id':each_candidate.candidate_id, 'candidate_name':each_candidate.candidate_name, 'candidate_email':each_candidate.candidate_email, 'job_id':each_candidate.job_id, 'job_role':each_candidate.job_role, 'candidate_status':candidate_status,'last_updated_date':each_candidate.last_updated_date})


    return my_candidates_list


@app.route("/candidates", methods=["GET"])
@Authentication_Required.requires_auth
def read_candidates():
    "Read the candidates"
    candidates_list = []
    display_candidates = db.session.query(Candidates, Jobs, Jobcandidate).filter(Jobcandidate.job_id == Jobs.job_id, Jobcandidate.candidate_id == Candidates.candidate_id, Jobs.job_status != 'Close').values(Candidates.candidate_id, Candidates.candidate_name, Candidates.candidate_email, Jobs.job_id, Jobs.job_role, Jobcandidate.candidate_status,Candidates.last_updated_date)

    candidates_list = fetch_candidate_list(display_candidates)

    return render_template("read-candidates.html", result=candidates_list)


@app.route("/candidate/<candidate_id>/delete", methods=["POST"])
@Authentication_Required.requires_auth
def delete_candidate(candidate_id):
    "Deletes a candidate"
    if request.method == 'POST':
        candidate_id_to_delete = request.form.get('candidateId')
        job_id_to_delete = request.form.get('jobId')
        #Delete the candidates from candidate table
        candidate_to_delete = Candidates.query.filter(Candidates.candidate_id == candidate_id_to_delete).first()
        data = {'candidate_name':candidate_to_delete.candidate_name, 'candidate_id':candidate_to_delete.candidate_id}
        db.session.delete(candidate_to_delete)
        db.session.commit()
        #Delete candidate from Jobcandidate table
        job_candidate_to_delete = Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id_to_delete, Jobcandidate.job_id == job_id_to_delete).first()
        db.session.delete(job_candidate_to_delete)
        db.session.commit()
        #Delete candidate from candidateround table
        db.session.query(Candidateround).filter(Candidateround.candidate_id == candidate_id_to_delete).delete()
        db.session.commit()
        #Delete candidate from Candidateinterviewer table
        exists = db.session.query(db.exists().where(Candidateinterviewer.candidate_id == candidate_id_to_delete)).scalar()
        if exists == False:
            pass
        else:
            db.session.query(Candidateinterviewer).filter(Candidateinterviewer.candidate_id == candidate_id_to_delete).delete()
            db.session.commit()

    return jsonify(data)


def candidate_diff_job(candidate_name, candidate_email, candidate_job_applied, job_id, comments):
    "Adding the candidates with different job"
    result_flag = False
    try :
        add_candidate_object = Candidates(candidate_name=candidate_name, candidate_email=candidate_email, job_applied=candidate_job_applied, comments=comments)
        db.session.add(add_candidate_object)
        db.session.flush()
        candidate_id = add_candidate_object.candidate_id
        db.session.commit()

        # Fetch the id for the candidate status 'Waiting on Qxf2'
        #Fetch the candidate status from status.py file also. Here we have to do the comparison so fetching from the status file
        candidate_status_id = Candidatestatus.query.filter(Candidatestatus.status_name == status.CANDIDTATE_STATUS[0]).values(Candidatestatus.status_id)
        for each_value in candidate_status_id:
            status_id = each_value.status_id

        #storing the candidate id and job id in jobcandidate table
        add_job_candidate_object = Jobcandidate(candidate_id=candidate_id, job_id=job_id, url='', candidate_status= status_id)
        db.session.add(add_job_candidate_object)
        db.session.commit()
        #Store the candidateid,jobid,roundid and round status in candidateround table

        result_flag = True
    except Exception as e:
        print(e)
        result_flag = False

    return result_flag

#Passing the optional parameter through URL
@app.route('/candidate/<job_role>/add')
@app.route("/candidate/add", defaults={'job_role': None}, methods=["GET", "POST"])
@Authentication_Required.requires_auth
def add_candidate(job_role):
    "Add a candidate"
    data, error = [], None
    job_available = Jobs.query.all()
    if request.method == 'GET':
        available_job_list = []
        if job_role is None:
            #If the parameter is none then fetch the jobs from the database
            job_available = Jobs.query.filter(Jobs.job_status != 'Delete').all()
            for each_job in job_available:
                available_job_list.append(each_job.job_role)
        else:
            #Since we have come through the job page pass the exact job role
            available_job_list.append(job_role)

        return render_template("add-candidates.html", data=available_job_list)

    if request.method == 'POST':
        candidate_name = request.form.get('candidateName')
        candidate_email = request.form.get('candidateEmail').lower()
        candidate_job_applied = request.form.get('jobApplied')
        job_id = Jobs.query.filter(Jobs.job_role == candidate_job_applied).value(Jobs.job_id)
        added_comments = request.form.get('addedcomments')
        candidate_name = candidate_name.strip()
        data = {'candidate_name':candidate_name}
        #Check the candidate has been already added or not
        check_candidate_exists = db.session.query(db.exists().where(Candidates.candidate_email == candidate_email)).scalar()
        if check_candidate_exists == True:
            #check the job of the candidates if the emails are same
            candidate_applied_job = db.session.query(db.exists().where(Candidates.job_applied == candidate_job_applied)).scalar()
            if candidate_applied_job == True:
                error = "Failed"
            else:
                return_object = candidate_diff_job(candidate_name=candidate_name, candidate_email=candidate_email, candidate_job_applied=candidate_job_applied, job_id=job_id, comments=added_comments)
                if return_object == True:
                    error = "Success"
        else:
            add_candidate_object = Candidates(candidate_name=candidate_name, candidate_email=candidate_email, job_applied=candidate_job_applied, comments=added_comments)
            db.session.add(add_candidate_object)
            db.session.flush()
            candidate_id = add_candidate_object.candidate_id
            db.session.commit()

            data['candidate_id'] = candidate_id

            # Fetch the id for the candidate status 'Waiting on Qxf2'
            #Fetch the candidate status from status.py file also. Here we have to do the comparison so fetching from the status file
            candidate_status_id = Candidatestatus.query.filter(Candidatestatus.status_name == status.CANDIDTATE_STATUS[0]).values(Candidatestatus.status_id)
            for each_value in candidate_status_id:
                status_id = each_value.status_id

            #storing the candidate id and job id in jobcandidate table
            add_job_candidate_object = Jobcandidate(candidate_id=candidate_id, job_id=job_id, url='', candidate_status= status_id)
            db.session.add(add_job_candidate_object)
            db.session.commit()


            error = "Success"

        api_response = {'data':data, 'error':error}
        print(api_response)

        return jsonify(api_response)


@app.route("/candidate/url", methods=["GET", "POST"])
@Authentication_Required.requires_auth
def generate_unique_url():
    candidate_id = request.form.get('candidateId')
    job_id = request.form.get('jobId')
    url,link_expiry_date=url_gen(candidate_id, job_id)
    link_expiry_date = link_expiry_date.date()
    edit_url = Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == job_id).update({'url': url})
    db.session.commit()
    api_response = {'url': url,'expiry_date':link_expiry_date}
    return jsonify(api_response)


def compare_rounds(all_round_id, completed_round_id):
    "compare two lists of round and get pending"
    all_round_id = set(all_round_id)
    completed_round_id = set(completed_round_id)
    pending_round_ids = all_round_id.difference(completed_round_id)
    pending_round_ids = list(pending_round_ids)

    return pending_round_ids


def get_pending_round_id(job_id, candidate_id):
    "Get the pending round id for the candidate"
    pending_round_ids = []
    round_ids = []
    completed_round_id = []
    #Check the round is already alloted for the candidates
    exists = db.session.query(db.exists().where(Candidateround.candidate_id == candidate_id)).scalar()
    if exists == True:
        #Fetch all the round details for a job
        round_ids_for_job = Jobround.query.filter(Jobround.job_id == job_id).all()
        for each_round_id in round_ids_for_job:
            round_ids.append(each_round_id.round_id)
        #Check the round id is already existing in the candidateround table
        completed_round_ids = Candidateround.query.filter(Candidateround.candidate_id == candidate_id, Candidateround.job_id == job_id).values(Candidateround.round_id)
        for each_complete_round in completed_round_ids:
            completed_round_id.append(each_complete_round.round_id)

        #Compare two list
        pending_round_ids = compare_rounds(round_ids, completed_round_id)
    else:
        round_ids_for_job = Jobround.query.filter(Jobround.job_id == job_id).all()
        for each_round_id in round_ids_for_job:
            pending_round_ids.append(each_round_id.round_id)

    return pending_round_ids


def get_round_id(candidate_id, job_id):
    "Get the round idlisted for the job"
    rounds_id_object = Jobround.query.filter(Jobround.job_id == job_id).all()
    round_id_list = []
    for each_round_id in rounds_id_object:
        round_id = each_round_id.round_id
        round_id_list.append(round_id)

    return round_id_list


def get_round_names_and_status(candidate_id, job_id, all_round_id):
    "Get the round name and status listed for the job"
    round_name_status_list = []
    all_round_details = {}
    for every_round_id in all_round_id:
        #Get the round status
        get_round_status = Candidateround.query.filter(Candidateround.candidate_id == candidate_id, Candidateround.job_id == job_id, Candidateround.round_id == every_round_id).value(Candidateround.round_status)
        #Get the candidate feedback
        candidate_feedback = Candidateround.query.filter(Candidateround.candidate_id == candidate_id, Candidateround.job_id == job_id, Candidateround.round_id == every_round_id).values(Candidateround.candidate_feedback,Candidateround.thumbs_value)
        for every_candidate_feedback in candidate_feedback:
            candidate_feedback = {'candidate_feedback':every_candidate_feedback.candidate_feedback, 'thumbs_value':every_candidate_feedback.thumbs_value}
        #Get the round name
        get_round_name = Rounds.query.filter(Rounds.round_id==every_round_id).value(Rounds.round_name)
        all_round_details = {'round_name':get_round_name, 'round_status':get_round_status,'candidate_feedback':candidate_feedback,'round_id':every_round_id}
        round_name_status_list.append(all_round_details)

    return round_name_status_list


@app.route("/candidate/<candidate_id>/job/<job_id>")
@Authentication_Required.requires_auth
def show_candidate_job(job_id, candidate_id):
    "Show candidate name and job role"
    try:
        round_names_list = []
        round_details = {}
        candidate_job_data = db.session.query(Jobs, Candidates, Jobcandidate).filter(Candidates.candidate_id == candidate_id, Jobs.job_id == job_id, Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == job_id).values(Candidates.candidate_name,  Candidates.candidate_email, Candidates.date_applied, Jobs.job_role, Jobs.job_id, Candidates.candidate_id, Jobcandidate.url, Jobcandidate.candidate_status, Jobcandidate.interviewer_email, Candidates.comments, Jobcandidate.interview_start_time, Jobcandidate.interview_date)
        for each_data in candidate_job_data:
            if each_data.url== None or each_data.url == '':
                url = None
            else:
                url = base_url + each_data.url + '/welcome'
            if (each_data.interview_date == None or each_data.interview_date == ''):
                interview_date = None
                interview_start_time = None
            else:
                interview_date = each_data.interview_date
                interview_start_time = each_data.interview_start_time
                interview_start_time = datetime.datetime.strptime(interview_start_time, '%Y-%m-%dT%H:%M:%S+05:30')
                interview_start_time = interview_start_time.time()

            data = {'candidate_name':each_data.candidate_name, 'job_applied':each_data.job_role, 'candidate_id':candidate_id, 'job_id':job_id, 'url': each_data.url, 'candidate_email':each_data.candidate_email, 'interviewer_email_id':each_data.interviewer_email, 'date_applied':each_data.date_applied.date(), 'url':url,'comments':each_data.comments, 'interview_date':interview_date, 'interview_start_time':interview_start_time}
            candidate_status_id = each_data.candidate_status
        #fetch the candidate status name for the status id
        candidate_status_name = db.session.query(Candidatestatus).filter(Candidatestatus.status_id == candidate_status_id).scalar()
        data['candidate_status']=candidate_status_name.status_name
        pending_round_ids = get_pending_round_id(job_id, candidate_id)
        #Get all rounds id for the job the candidate applied
        all_round_id = get_round_id(candidate_id, job_id)
        #Get the roundstatus, feedback of the candidate job
        round_name_status_list = get_round_names_and_status(candidate_id, job_id, all_round_id)
        #Get the pending round id details from the table
        for each_round_id in pending_round_ids:
            round_detail = db.session.query(Rounds).filter(Rounds.round_id == each_round_id).scalar()
            round_details = {'round_name':round_detail.round_name, 'round_id':round_detail.round_id, 'round_description':round_detail.round_description, 'round_time':round_detail.round_time}
            round_names_list.append(round_details)

    except Exception as e:
        app.logger.error(e)
        with open('info_error.log','a') as fp:
            fp.write(repr(e))


    return render_template("candidate-job-status.html", result=data, round_names=round_names_list,all_round_details=round_name_status_list)


@app.route("/candidate/<candidate_id>/edit", methods=["GET", "POST"])
@Authentication_Required.requires_auth
def edit_candidates(candidate_id):
    "Edit the candidtes"
    #Fetch the candidate details and equal job id
    if request.method == 'GET':
        jobs_list = []
        candidate_data = {}
        candidate_details = Candidates.query.join(Jobcandidate, Candidates.candidate_id == Jobcandidate.candidate_id) .filter(Candidates.candidate_id == candidate_id).values(Candidates.candidate_name, Candidates.candidate_email,Candidates.candidate_id, Jobcandidate.job_id, Candidates.comments)
        for each_detail in candidate_details:
            #Fetch the job role of the candidate using job id
            get_job_role = db.session.query(Jobs.job_role).filter(Jobs.job_id == each_detail.job_id).first()
            candidate_data = {'candidate_name':each_detail.candidate_name, 'candidate_email':each_detail.candidate_email, 'candidate_id':each_detail.candidate_id, 'job_role':get_job_role.job_role, 'job_id':each_detail.job_id, 'added_comments':each_detail.comments}
        #Fetch all the Job roles from the Jobs table to edit the job details for the candidate
        job_roles = db.session.query(Jobs.job_role).all()
        for each_job in job_roles:
            jobs_list.append(each_job.job_role)

        candidate_data['job_roles']=jobs_list
        return render_template("edit-candidate.html", result=candidate_data)

    if request.method == 'POST':
        candidate_name = request.form.get('candidateName')
        candidate_email = request.form.get('candidateEmail')
        candidate_job_applied = request.form.get('jobApplied')
        candidate_old_job = request.form.get('existJob')
        exist_added_comments = request.form.get('addedcomments')
        data = {'candidate_name':candidate_name}
        #Check the candidate has been already added or not
        if (candidate_job_applied == candidate_old_job):
            Candidates.query.filter(Candidates.candidate_id == candidate_id).update({'candidate_name':candidate_name, 'candidate_email':candidate_email, 'comments':exist_added_comments})
            db.session.commit()
        else:
            Candidates.query.filter(Candidates.candidate_id == candidate_id).update({'candidate_name':candidate_name, 'candidate_email':candidate_email, 'job_applied':candidate_job_applied, 'comments':exist_added_comments})
            db.session.commit()
            edited_job_role = db.session.query(Jobs.job_id).filter(Jobs.job_role == candidate_job_applied).first()
            #storing the candidate id and job id in jobcandidate table
            Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id).update({'candidate_id':candidate_id, 'job_id':edited_job_role.job_id, 'url':'', 'candidate_status':1})

            db.session.commit()

        api_response = {'data':data}
        return jsonify(api_response)


@app.route("/candidates/<candidate_id>/jobs/<job_id>/email")
@Authentication_Required.requires_auth
def send_email(candidate_id, job_id):
    # Fetch the id for the candidate status 'Waiting on Candidate'
    #Fetch the candidate status from status.py file also. Here we have to do the comparison so fetching from the status file
    candidate_status_id = db.session.query(Candidatestatus).filter(Candidatestatus.status_name == status.CANDIDTATE_STATUS[1]).scalar()

    candidate_status = Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == job_id).update({'candidate_status':candidate_status_id.status_id})
    db.session.commit()
    candidate_name = Candidates.query.filter(Candidates.candidate_id == candidate_id).value(Candidates.candidate_name)
    if candidate_name != None:
        return jsonify(data=candidate_name)
    else:
        return jsonify(error="error"), 500


def change_status_to_noopening(candidate_id,candidate_job_applied):
    "Change status to no opening"
    try:
        #Update the candidate status to 'Waiting for new opening'
        candidate_statuses = Candidatestatus.query.all()
        for each_status in candidate_statuses:
            if each_status.status_name == status.CANDIDTATE_STATUS[6]:
                status_id = each_status.status_id
        #Change the candidate status after the invite has been sent
        Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id,  Jobcandidate.job_id == candidate_job_applied).update({'candidate_status':status_id})
        db.session.commit()
        error = 'Success'

    except Exception as e:
        error = "Failed"
        return(str(e))

    return error


@app.route("/noopening/email", methods=["POST"])
@Authentication_Required.requires_auth
def no_opening():
    "Send a no opening email to the candidates"
    candidate_name = request.form.get('candidatename')
    candidate_email = request.form.get('candidateemail')
    candidate_job_applied = request.form.get('candidatejob')
    candidate_id = request.form.get('candidateid')
    logged_email = session['logged_user']

    msg = Message("Career opportunity with Qxf2 Services", sender=("Qxf2 Services", "test@qxf2.com"),  recipients=[candidate_email], cc=[logged_email])
    msg.body = "Hi %s , \n\nThanks for applying to Qxf2 Services. We have received your application. Currently we don't have openings suitable to your background and experience. We will get back to you once we have an opening that fits you better.\n\nThanks, \nQxf2 Services"%(candidate_name)
    mail.send(msg)
    candidate_status = change_status_to_noopening(candidate_id,candidate_job_applied)
    last_updated_date = Candidates.query.filter(Candidates.candidate_id==candidate_id).update({'last_updated_date':datetime.date.today()})
    db.session.commit()
    data = {'candidate_name': candidate_name,  'error': candidate_status}
    return jsonify(data)


@app.route("/noopening/noemail",methods=["GET","POST"])
def noopeining_without_email():
    "Change the status without no opening  email"
    candidate_name = request.form.get('candidatename')
    candidate_email = request.form.get('candidateemail')
    candidate_job_applied = request.form.get('candidatejob')
    candidate_id = request.form.get('candidateid')
    status_change = change_status_to_noopening(candidate_id,candidate_job_applied)

    data = {'candidate_name': candidate_name, 'error': status_change}
    last_updated_date = Candidates.query.filter(Candidates.candidate_id==candidate_id).update({'last_updated_date':datetime.date.today()})
    db.session.commit()
    return jsonify(data)


def change_status_to_reject(candidate_id,candidate_job_applied):
    "Change the status to reject"
    try:
        #Update the candidate status to 'Reject'
        candidate_statuses = Candidatestatus.query.all()
        for each_status in candidate_statuses:
            if each_status.status_name == status.CANDIDTATE_STATUS[4]:
                status_id = each_status.status_id
        #Change the candidate status after the invite has been sent
        Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == candidate_job_applied).update({'candidate_status':status_id})
        db.session.commit()
        error = 'Success'

    except Exception as e:
        error = "Failed"
        print(e)
        return(str(e))

    return error


def fetch_interviewer_email(candidate_id, job_id):
    "Fetch the interviewers email for the candidate"
    email_id = Jobcandidate.query.filter(Jobcandidate.job_id == job_id, Jobcandidate.candidate_id == candidate_id).value(Jobcandidate.interviewer_email)
    if email_id == None:
        print("The interviewer is not yet assigned for the candidate")

    return email_id


@app.route("/reject", methods=["POST"])
@Authentication_Required.requires_auth
def send_reject():
    "Send reject email"
    candidate_name = request.form.get('candidatename')
    candidate_email = request.form.get('candidateemail')
    candidate_job_applied = request.form.get('candidatejob')
    candidate_id = request.form.get('candidateid')
    interviewer_email = fetch_interviewer_email(candidate_id, candidate_job_applied)
    logged_email = session['logged_user']

    if interviewer_email == None:
        cc = [logged_email]
    else:
        cc = interviewer_email.split(',')
        cc.append(logged_email)

    msg = Message("Interview update from Qxf2 Services", sender=("Qxf2 Services", "test@qxf2.com"),  cc=cc, recipients=[candidate_email])
    msg.body = "Hi %s , \n\nI appreciate your interest in a career opportunity with Qxf2 Services. It was a pleasure speaking to you about your background and interests. There are many qualified applicants in the current marketplace and we are searching for those who have the most directly applicable experience to our limited number of openings. I regret we will not be moving forward with your interview process. We wish you all the best in your current search and future endeavors.\n\nThanks, \nQxf2 Services"%(candidate_name)
    mail.send(msg)
    candidate_status = change_status_to_reject(candidate_id,candidate_job_applied)
    last_updated_date = Candidates.query.filter(Candidates.candidate_id==candidate_id).update({'last_updated_date':datetime.date.today()})
    db.session.commit()
    data = {'candidate_name': candidate_name, 'error': candidate_status}
    return jsonify(data)


@app.route("/comments/save", methods=['GET', 'POST'])
def save_comments():
    "Save the comments"
    candidate_comments = request.form.get('comments')
    candidate_id = request.form.get('candidateid')
    job_id = request.form.get('jobid')
    Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == job_id).update({'comments':candidate_comments})
    db.session.commit()
    error = 'Success'

    data = {'candidate_comments':candidate_comments, 'error':error}

    return jsonify(data)


@app.route("/candidatestatus/filter", methods=['GET', 'POST'])
def filter_candidate_status():
    "Filter the candidates based on the status"
    filtered_candidates_list = []
    filtered_status = request.form.get('selectedstatus')
    #Fetch the candidate status id for the filtered status
    status_id = Candidatestatus.query.filter(Candidatestatus.status_name == filtered_status).value(Candidatestatus.status_id)
    #Fetch the candidates who are all in that status
    filtered_candidates = Jobcandidate.query.filter(Jobcandidate.candidate_status == status_id).values(Jobcandidate.candidate_id, Jobcandidate.job_id)
    for all_candidates in filtered_candidates:
        candidate_id = all_candidates.candidate_id
        job_id = all_candidates.job_id
        #Fetch the job name using job id
        job_applied = Jobs.query.filter(Jobs.job_id == job_id).value(Jobs.job_role)
        #Fetch the candidate details from candidate table
        candidate_details = Candidates.query.filter(Candidates.candidate_id == candidate_id).values(Candidates.candidate_name, Candidates.candidate_email)
        for each_data in candidate_details:
            candidate_name=each_data.candidate_name
            candidate_email = each_data.candidate_email
        filtered_candidates_list.append({'candidate_id':candidate_id, 'candidate_name':candidate_name, 'candidate_email':candidate_email, 'job_role':job_applied, 'candidate_status':filtered_status})
    len_of_filtered_candidates_list = len(filtered_candidates_list)

    if len_of_filtered_candidates_list > 0:
        return render_template("read-candidates.html",  result=filtered_candidates_list)

    else:
        result = 'error'
        return result


@app.route("/filter/job", methods=['GET', 'POST'])
def job_filter():
    "Filter the job for the candidates"
    filter_job_list = []
    filtered_job = request.form.get('selectjob')
    candidate_job_filter = Candidates.query.filter(Candidates.job_applied == filtered_job).values(Candidates.candidate_id,Candidates.candidate_name,Candidates.job_applied,Candidates.candidate_email)

    for each_data in candidate_job_filter:
        candidate_name = each_data.candidate_name
        candidate_email = each_data.candidate_email
        candidate_job = each_data.job_applied
        candidate_id = each_data.candidate_id
        candidate_job_status_id = Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id).value(Jobcandidate.candidate_status)
        candidate_job_status = Candidatestatus.query.filter(Candidatestatus.status_id == candidate_job_status_id).value(Candidatestatus.status_name)
        filter_job_list.append({'candidate_id':candidate_id, 'candidate_name':candidate_name, 'candidate_email':candidate_email,'job_role':candidate_job, 'candidate_status':candidate_job_status})

    len_of_filtered_candidates_list = len(filter_job_list)

    if len_of_filtered_candidates_list > 0:
        return render_template("read-candidates.html",  result=filter_job_list)

    else:
        result = 'error'
        return result


@app.route("/noemail/reject",methods=["GET","POST"])
def reject_without_email():
    "Change the status of the candidate without reject email"
    candidate_name = request.form.get('candidatename')
    candidate_email = request.form.get('candidateemail')
    candidate_job_applied = request.form.get('candidatejob')
    candidate_id = request.form.get('candidateid')
    status_change = change_status_to_reject(candidate_id,candidate_job_applied)
    last_updated_date = Candidates.query.filter(Candidates.candidate_id==candidate_id).update({'last_updated_date':datetime.date.today()})
    db.session.commit()
    data = {'candidate_name': candidate_name, 'error': status_change}
    return jsonify(data)


@app.route('/candidate/noresponse',methods=["GET","POST"])
def status_no_response():
    "Change the candidate status to no response if they have not replied"
    if request.method == "POST":
        candidate_id = request.form.get("candidateid")
        #Update the candidate status to no response
        db.session.query(Jobcandidate).filter(Jobcandidate.candidate_id == candidate_id).update({'candidate_status':4})
        db.session.commit()
        last_updated_date = Candidates.query.filter(Candidates.candidate_id==candidate_id).update({'last_updated_date':datetime.date.today()})
        db.session.commit()

    return candidate_id


@app.route('/candidate/hired',methods=["GET","POST"])
def status_to_hired():
    "Change the candidate status to hiried"
    if request.method == "POST":
        candidate_id = request.form.get("candidateid")
        job_id = request.form.get("jobid")
        db.session.query(Jobcandidate).filter(Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == job_id).update({'candidate_status':6})
        db.session.commit()
        last_updated_date = Candidates.query.filter(Candidates.candidate_id==candidate_id).update({'last_updated_date':datetime.date.today()})
        db.session.commit()
    return candidate_id


@app.route("/candidate/<candidate_id>/round/<round_id>/add_feedback",methods=["GET","POST"])
def add_feedback(candidate_id, round_id):
    "Adding the feedback for the candidates by interviewers"
    if request.method == "GET":
        data = {'candidate_id':candidate_id,'round_id':round_id}
        return render_template("add-feedback.html",result=data)
    if request.method == "POST":
        error = "Success"
        added_feedback = request.form.get("addedfeedback")
        thumbs_value = request.form.get("thumbsvalue")
        combined_feed = thumbs_value + ',' + added_feedback
        Candidateround.query.filter(Candidateround.candidate_id==candidate_id,Candidateround.round_id==round_id).update({'candidate_feedback':added_feedback,'thumbs_value':thumbs_value})
        db.session.commit()
        result = {'added_feedback':added_feedback, 'thumbs_value':thumbs_value, 'error': error}
        last_updated_date = Candidates.query.filter(Candidates.candidate_id==candidate_id).update({'last_updated_date':datetime.date.today()})
        db.session.commit()

    return jsonify(result)


@app.route("/candidate/<candidate_id>/round/<round_id>/edit_feedback",methods=["GET","POST"])
def edit_feedback(candidate_id, round_id):
    "Adding the feedback for the candidates by interviewers"
    if request.method == "GET":
        data = {'candidate_id':candidate_id,'round_id':round_id}
        added_candidate_feedback = Candidateround.query.filter(Candidateround.candidate_id == candidate_id, Candidateround.round_id==round_id).values(Candidateround.candidate_feedback,Candidateround.thumbs_value)
        for edit_feedback in added_candidate_feedback:
            if edit_feedback.candidate_feedback == None:
                added_candidate_feedback = None
            else:
                edit_feedback_value = (edit_feedback.thumbs_value.split('s')[0]+'s'+" "+edit_feedback.thumbs_value.split('s')[-1]).title()
                added_candidate_feedback={'candidate_feedback':edit_feedback.candidate_feedback, 'thumbs_value':edit_feedback_value}

        return render_template("edit-feedback.html",result=data,candidate_feedback=added_candidate_feedback,)

    if request.method == "POST":
        error = "Success"
        edited_feedback = request.form.get("editedfeedback")
        thumbs_value = request.form.get("thumbsvalue")
        combined_edit_feed = thumbs_value + ',' + edited_feedback
        Candidateround.query.filter(Candidateround.candidate_id==candidate_id,Candidateround.round_id==round_id).update({'candidate_feedback':edited_feedback, 'thumbs_value':thumbs_value})
        db.session.commit()
        result = {'edited_feedback':edited_feedback, 'thumbs_value':thumbs_value, 'error': error}
        last_updated_date = Candidates.query.filter(Candidates.candidate_id==candidate_id).update({'last_updated_date':datetime.date.today()})
        db.session.commit()


    return jsonify(result)
