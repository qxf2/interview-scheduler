"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response, session
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
import qxf2_scheduler.candidate_status as status
from qxf2_scheduler import db
import json
import ast,re,uuid
import sys,datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message, Mail
from flask_login import current_user, login_user,login_required,logout_user
from pytz import timezone
import flask
import flask_login

mail = Mail(app)

from qxf2_scheduler.models import Interviewers, Interviewertimeslots, Jobs, Jobinterviewer, Rounds, Jobround,Candidates,Jobcandidate,Candidatestatus,Candidateround,Candidateinterviewer,Login
DOMAIN = 'qxf2.com'
base_url = 'https://interview-scheduler.qxf2.com/'

def check_user_exists(user_email):
    "Check the job already exists in the database"
    fetch_existing_user_email = Login.query.all()
    emails_list = []
    # Fetch the job role
    for each_email in fetch_existing_user_email:
        emails_list.append(each_email.email.lower())

    # Compare the job with database job list
    if user_email.lower() in emails_list:
        check_user_exists = True
    else:
        check_user_exists = False

    return check_user_exists

@app.route("/registration",methods=['GET','POST'])
def registration():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        user_name = request.form.get('username')
        user_password = request.form.get('userpassword')
        user_email = request.form.get('useremail')
        check_user_exist = check_user_exists(user_email)
        data = {'user_name':user_name,'user_email':user_email,'user_password':user_password}
        if check_user_exist == True:
            error = 'error'
        else:
            add_new_user_object = Login(username=user_name,email=user_email,password=user_password)
            db.session.add(add_new_user_object)
            db.session.flush()
            user_id = add_new_user_object.id
            db.session.commit()
            error = 'Success'
        api_response = {'data':data,'error':error}

    return jsonify(api_response)


def get_id_for_emails(email_list):
    "Get the id for the interviewers who has interview scheduled already"
    interviewers_id_list = []
    for interviewer_email in email_list:
        interviewer_id = Interviewers.query.filter(Interviewers.interviewer_email == interviewer_email).value(Interviewers.interviewer_id)
        interviewers_id_list.append(interviewer_id)

    return interviewers_id_list


def check_interview_exists(date):
    "Fetch the interviewers wich have an interview already"
    interviewers_email_list = []
    date = datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%B %d, %Y')
    fetch_interviewers_email = db.session.query(Jobcandidate).filter(Jobcandidate.interview_date == date).values(Jobcandidate.interviewer_email)
    for each_interviewer_email in fetch_interviewers_email:
        interviewers_email_list.append(each_interviewer_email.interviewer_email)
    interviewers_id_list = get_id_for_emails(interviewers_email_list)

    return interviewers_id_list


@app.route("/get-schedule", methods=['GET', 'POST'])
def date_picker():
    "Dummy page to let you see a schedule"
    round_duration = request.form.get('roundtime')
    if request.method == 'GET':
        return render_template('get-schedule.html')
    if request.method == 'POST':
        date = request.form.get('date')
        round_duration = request.form.get('roundtime')
        round_id = request.form.get('roundid')
        chunk_duration = round_duration.split(' ')[0]
        job_id = session['candidate_info']['job_id']
        candidate_id = session['candidate_info']['candidate_id']
        #Check the candidate is scheduled an interview already
        check_scheduled_event = Candidateround.query.filter(Candidateround.candidate_id==candidate_id,Candidateround.job_id==job_id,Candidateround.round_id==round_id).values(Candidateround.round_status)
        for check_event in check_scheduled_event:
            candidate_schedule_status = check_event.round_status
        if candidate_schedule_status == 'Invitation Sent':

            #Check who are all the interviewers interviewed the candidate
            alloted_interviewers_id_list = []
            try:
                alloted_interviewers_id = db.session.query(Candidateinterviewer).filter(Candidateinterviewer.candidate_id==candidate_id,Candidateinterviewer.job_id==job_id).values(Candidateinterviewer.interviewer_id)
                alloted_interviewers_id_list = []
                for each_interviewer_id in alloted_interviewers_id:
                    alloted_interviewers_id_list.append(each_interviewer_id.interviewer_id)
            except Exception as e:
                print("The candidate is scheduling an interview for the first time",e)
            #Fetch the interviewers email id which have an interview for the picked date
            scheduled_interviewers_id = check_interview_exists(date)
            #Fetch the interviewers for the candidate job
            job_interviewer_id = db.session.query(Jobinterviewer).filter(Jobinterviewer.job_id==job_id).values(Jobinterviewer.interviewer_id)
            interviewer_id = []
            for each_interviewer_id in job_interviewer_id:
                if each_interviewer_id.interviewer_id in scheduled_interviewers_id:
                    pass
                else:
                    interviewer_id.append(each_interviewer_id.interviewer_id)

            if len(alloted_interviewers_id_list) == 0:
                pass
            else:
                #Compare the alloted and fetched interviewers id
                interviewer_id = list(set(interviewer_id)-set(alloted_interviewers_id_list))

            #Fetch the interviewer emails for the candidate job
            interviewer_work_time_slots = []
            for each_id in interviewer_id:
                new_slot = db.session.query(Interviewers,Interviewertimeslots).filter(each_id==Interviewers.interviewer_id,each_id==Interviewertimeslots.interviewer_id).values(
                Interviewers.interviewer_email, Interviewertimeslots.interviewer_start_time, Interviewertimeslots.interviewer_end_time)

                for interviewer_email, interviewer_start_time, interviewer_end_time in new_slot:
                        interviewer_work_time_slots.append({'interviewer_email': interviewer_email, 'interviewer_start_time': interviewer_start_time,'interviewer_end_time': interviewer_end_time})
            free_slots = my_scheduler.get_free_slots_for_date(
                date, interviewer_work_time_slots)
            free_slots_in_chunks = my_scheduler.get_free_slots_in_chunks(
                free_slots,chunk_duration)
            api_response = {
                'free_slots_in_chunks': free_slots_in_chunks, 'date': date}

            return jsonify(api_response)
        else:
            data = {'error':"Already scheduled",'candidate_id':candidate_id}
            return jsonify(data)


@app.route("/confirm",methods=['GET','POST'])
def confirm():
    "Confirming the event message"
    if request.method == 'GET':
        response_value = request.args['value']

        return render_template("confirmation.html", value=json.loads(response_value))


@app.route("/confirmation", methods=['GET', 'POST'])
def scehdule_and_confirm():
    "Schedule an event and display confirmation"
    if request.method == 'GET':

        return render_template("get-schedule.html")

    if request.method == 'POST':
        slot = request.form.get('slot')
        email = request.form.get('interviewerEmails')
        date = request.form.get('date')
        candidate_id = session['candidate_info']['candidate_id']
        candidate_email = session['candidate_info']['candidate_email']
        job_id = session['candidate_info']['job_id']
        #Fetch the round id
        get_round_id_object = db.session.query(Candidateround).filter(Candidateround.candidate_id==candidate_id,Candidateround.job_id==job_id,Candidateround.round_status=='Invitation Sent').scalar()

        #Fetch the round name and description
        round_name_and_desc = Rounds.query.filter(Rounds.round_id==get_round_id_object.round_id).values(Rounds.round_name,Rounds.round_description)
        for each_round_detail in round_name_and_desc:
            round_name = each_round_detail.round_name
            round_description = each_round_detail.round_description
        schedule_event = my_scheduler.create_event_for_fetched_date_and_time(
            date, email,candidate_email, slot,round_name,round_description)
        date_object = datetime.datetime.strptime(date, '%m/%d/%Y').date()
        date = datetime.datetime.strftime(date_object, '%B %d, %Y')
        value = {'schedule_event': schedule_event,
        'date': date,
        'slot' : slot}
        value = json.dumps(value)
        candidate_status_id = db.session.query(Candidatestatus).filter(Candidatestatus.status_name==status.CANDIDTATE_STATUS[2]).scalar()
        candidate_status = Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == job_id).update({'candidate_status':candidate_status_id.status_id,'interview_start_time':schedule_event[0]['start']['dateTime'],'interview_end_time':schedule_event[1]['end']['dateTime'],'interview_date':date,'interviewer_email':schedule_event[3]['interviewer_email']})
        db.session.commit()
        #Update the round status for the candidate
        update_round_status = Candidateround.query.filter(Candidateround.candidate_id==candidate_id,Candidateround.job_id==job_id).update({'round_status':'Completed'})
        db.session.commit()
        #Get the interviewer email from the form
        alloted_interviewer_email = schedule_event[3]['interviewer_email']
        #Fetch the interviewer id of the interviewer
        fetch_interviewer_id = db.session.query(Interviewers).filter(Interviewers.interviewer_email==alloted_interviewer_email).values(Interviewers.interviewer_id)
        for each_interviewer in fetch_interviewer_id:
            fetch_interviewer_id_value=each_interviewer.interviewer_id

        #Add the interviewer id, candidateid and job id to the table
        add_interviewer_candidate_object = Candidateinterviewer(job_id=job_id,candidate_id=candidate_id,interviewer_id=fetch_interviewer_id_value)
        db.session.add(add_interviewer_candidate_object)
        db.session.commit()

        return redirect(url_for('confirm', value=value))


    return render_template("get-schedule.html")


def validate(username):
    "Validate the username and passowrd"
    exists = db.session.query(db.exists().where(Login.username == username)).scalar()

    return exists


def password_validate(password):
    "Validate the username and passowrd"
    exists = db.session.query(db.exists().where(Login.password == password)).scalar()

    return exists

@app.before_request
def before_request():
    "Session time out method"
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes = 60)
    flask.session.modified = True


@app.route('/login', methods=['GET', 'POST'])
@app.route('/')
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html', error=error)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        data = {'username':username,'password':password}
        #fetch the email id of the user whose logged in
        user_email_id = Login.query.filter(Login.username==username).values(Login.email)
        for logged_user in user_email_id:
            logged_email_id = logged_user.email
        session['logged_user'] = logged_email_id
        completion = validate(username)
        if completion ==False:
            error = 'error.'
        else:
            password_check = password_validate(password)
            if password_check ==False:
                error = 'error.'
            else:
                user = Login()
                user.name=username
                user.password=password
                login_user(user)
                error = 'Success'
        api_response = {'data':data,'error':error}
        return jsonify(api_response)


@app.route("/logout",methods=["GET","POST"])
@login_required
def logout():
    "Logout the current page"
    logout_user()
    return redirect(url_for('login'))


@app.route("/index")
@login_required
def index():
    "The index page"
    return render_template('index.html')


@app.route("/interviewers")
@login_required
def list_interviewers():
    "List all the interviewer names"
    all_interviewers = Interviewers.query.all()
    my_interviewers_list = []
    for each_interviewer in all_interviewers:
        my_interviewers_list.append({'interviewer_id': each_interviewer.interviewer_id,
                                     'interviewer_name': each_interviewer.interviewer_name})

    return render_template("list-interviewers.html", result=my_interviewers_list)


def form_interviewer_timeslot(time_slot):
    "Parse the interviewer detail with start and end time"
    time_dict = {}
    time_dict['starttime'] = time_slot['interviewers_starttime']
    time_dict['endtime'] = time_slot['interviewers_endtime']
    del time_slot['interviewers_starttime']
    del time_slot['interviewers_endtime']
    time_slot['time'] = time_dict

    return time_slot


def form_interviewer_details(interviewer_details):
    "Parsing the interviewer detals we get it from form"
    list_parsed_interviewer_detail = []
    parsed_interviewer_details = []

    for each_detail in interviewer_details:
        interviewer_detail = {
            'interviewer_id': each_detail.interviewer_id,
            'interviewers_name': each_detail.interviewer_name,
            'interviewers_id': each_detail.interviewer_id,
            'interviewers_email': each_detail.interviewer_email,
            'interviewers_designation': each_detail.interviewer_designation,
            'interviewers_starttime': each_detail.interviewer_start_time,
            'interviewers_endtime': each_detail.interviewer_end_time}

        parsed_interviewer_detail = form_interviewer_timeslot(
            time_slot=interviewer_detail)
        list_parsed_interviewer_detail.append(parsed_interviewer_detail)

    for each_dict in list_parsed_interviewer_detail:
        if len(parsed_interviewer_details) == 0:
            parsed_interviewer_details.append(each_dict)
            parsed_interviewer_details[0]["time"] = [
                parsed_interviewer_details[0]["time"]]
        else:
            parsed_interviewer_details[0]['time'].append(each_dict['time'])

    return parsed_interviewer_details


@app.route("/<interviewer_id>/interviewer")
@login_required
def read_interviewer_details(interviewer_id):
    "Displays all the interviewer details"
    # Fetching the Interviewer detail by joining the Interviewertimeslots tables and Interviewer tables
    exists = db.session.query(db.exists().where(
        Interviewertimeslots.interviewer_id == interviewer_id)).scalar()
    if exists:
        interviewer_details = Interviewers.query.join(Interviewertimeslots, Interviewers.interviewer_id == Interviewertimeslots.interviewer_id).filter(
            Interviewers.interviewer_id == interviewer_id).values(Interviewers.interviewer_name, Interviewers.interviewer_email, Interviewers.interviewer_designation, Interviewers.interviewer_id, Interviewertimeslots.interviewer_start_time, Interviewertimeslots.interviewer_end_time)
        parsed_interviewer_details = form_interviewer_details(
            interviewer_details)
    else:
        interviewer_details = Interviewers.query.filter(Interviewers.interviewer_id == interviewer_id).values(
            Interviewers.interviewer_id, Interviewers.interviewer_name, Interviewers.interviewer_email, Interviewers.interviewer_designation)
        for each_detail in interviewer_details:
            parsed_interviewer_details = {
                'interviewers_name': each_detail.interviewer_name,
                'interviewers_id': each_detail.interviewer_id,
                'interviewers_email': each_detail.interviewer_email,
                'interviewers_designation': each_detail.interviewer_designation}

    return render_template("read-interviewers.html", result=parsed_interviewer_details)


def add_edit_interviewers_in_time_slot_table(interviewer_name):
    "Adding the interviewers in the interviewer time slots table"
    added_edited_interviewer_id = Interviewers.query.filter(
        Interviewers.interviewer_name == interviewer_name).first()

    # Adding the new time slots in the interviewerstimeslots table
    interviewer_time_slots = ast.literal_eval(request.form.get('timeObject'))
    interviewer_start_time = interviewer_time_slots['starttime']
    interviewer_end_time = interviewer_time_slots['endtime']
    len_of_slots = len(interviewer_start_time)
    for i in range(len_of_slots):
        add_edit_time_slots = Interviewertimeslots(interviewer_id=added_edited_interviewer_id.interviewer_id,
                                                   interviewer_start_time=interviewer_start_time[i], interviewer_end_time=interviewer_end_time[i])
        db.session.add(add_edit_time_slots)
        db.session.commit()


@app.route("/interviewer/<interviewer_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_interviewer(interviewer_id):
    "Edit the interviewers"
    # This query fetch the interviewer details by joining the time slots table and interviewers table.
    if request.method == "GET":
        exists = db.session.query(db.exists().where(
            Interviewertimeslots.interviewer_id == interviewer_id)).scalar()
        if exists:
            interviewer_details = Interviewers.query.join(Interviewertimeslots, Interviewers.interviewer_id == Interviewertimeslots.interviewer_id).filter(
                Interviewers.interviewer_id == interviewer_id).values(Interviewers.interviewer_name, Interviewers.interviewer_email, Interviewers.interviewer_designation, Interviewers.interviewer_id, Interviewertimeslots.interviewer_start_time, Interviewertimeslots.interviewer_end_time)
            parsed_interviewer_details = form_interviewer_details(
                interviewer_details)
        else:
            interviewer_details = Interviewers.query.filter(Interviewers.interviewer_id == interviewer_id).values(
                Interviewers.interviewer_id, Interviewers.interviewer_name, Interviewers.interviewer_email, Interviewers.interviewer_designation)
            for each_detail in interviewer_details:
                parsed_interviewer_details = {
                    'interviewers_name': each_detail.interviewer_name,
                    'interviewers_id': each_detail.interviewer_id,
                    'interviewers_email': each_detail.interviewer_email,
                    'interviewers_designation': each_detail.interviewer_designation}

    if request.method == "POST":
        # Updating the interviewers table
        interviewer_name = request.form.get('name')
        time_object = request.form.get('timeObject')
        data = {'interviewer_name': interviewer_name}
        edit_interviewers = Interviewers.query.filter(Interviewers.interviewer_id == interviewer_id).update({'interviewer_name': request.form.get(
            'name'), 'interviewer_email': request.form.get('email'), 'interviewer_designation': request.form.get('designation')})
        db.session.commit()

        # Fetching the time ids of interviewer
        total_rows_of_interviewer_in_time_table = Interviewertimeslots.query.filter(
            Interviewertimeslots.interviewer_id == interviewer_id).values(Interviewertimeslots.time_id)

        # Store the timeid in the list for deleting at the end
        list_edited_time_slots = []
        for each_time_id in total_rows_of_interviewer_in_time_table:
            list_edited_time_slots.append(each_time_id.time_id)

        # Filtering the interviewer id from the table to use it for interviewertimeslots table
        add_edit_interviewers_in_time_slot_table(interviewer_name)

        # Deleting the old time slots based on the timeie
        for each_times_id in list_edited_time_slots:
            delete_time_slots = Interviewertimeslots.query.filter(
                Interviewertimeslots.time_id == each_times_id).one()
            db.session.delete(delete_time_slots)
            db.session.commit()

        return jsonify(data)
    return render_template("edit-interviewer.html", result=parsed_interviewer_details)


@app.route("/interviewer/<interviewer_id>/delete", methods=["POST"])
@login_required
def delete_interviewer(interviewer_id):
    "Deletes an interviewer"
    if request.method == 'POST':
        # interviewer_to_delete = request.form.get('interviewer-id')
        deleted_user = Interviewers.query.filter(
            Interviewers.interviewer_id == interviewer_id).first()
        data = {'interviewer_name': deleted_user.interviewer_name,
                'interviewer_id': deleted_user.interviewer_id}
        db.session.delete(deleted_user)
        db.session.commit()
        delete_user_timeslot = Interviewertimeslots.query.filter(
            Interviewertimeslots.interviewer_id == interviewer_id).delete()
        db.session.commit()

    return jsonify(data)


@app.route("/jobs")
@login_required
def jobs_page():
    "Displays the jobs page for the interview"
    display_jobs = Jobs.query.all()
    my_job_list = []
    for each_job in display_jobs:
        if each_job.job_status is None:
            each_job.job_status = 'Open'
        my_job_list.append(
            {'job_id': each_job.job_id, 'job_role': each_job.job_role,'job_status':each_job.job_status})

    return render_template("list-jobs.html", result=my_job_list)

def fetch_candidate_list(candidate_list_object,job_id):
    "Fetch the candidate list"
    my_candidates_list = []
    for each_candidate in candidate_list_object:
        candidate_status_object = Candidatestatus.query.filter(Candidatestatus.status_id == each_candidate.candidate_status).values(Candidatestatus.status_name)
        for candidate_status in candidate_status_object:
            candidate_status = candidate_status.status_name

        my_candidates_list.append({'candidate_id':each_candidate.candidate_id, 'candidate_name':each_candidate.candidate_name, 'candidate_email':each_candidate.candidate_email, 'job_id':job_id, 'candidate_status':candidate_status})

    return my_candidates_list


@app.route("/<job_id>/details/")
@login_required
def interviewers_for_roles(job_id):
    "Display the interviewers based on the job id"
    interviewers_list = []
    rounds_list = []
    candidates_list = []

    # Fetch the interviewers list for the job role
    interviewer_list_for_roles = Interviewers.query.join(Jobinterviewer, Interviewers.interviewer_id == Jobinterviewer.interviewer_id).filter(
        Jobinterviewer.job_id == job_id).values(Interviewers.interviewer_name)

    # Fetch the job list
    db_round_list = db.session.query(Jobs, Jobround, Rounds).filter(Jobround.job_id == job_id, Rounds.round_id == Jobround.round_id).group_by(Rounds.round_id).values(
        Rounds.round_name,Rounds.round_time,Rounds.round_description,Rounds.round_requirement)

    #Fetch the candidate list
    db_candidate_list = Candidates.query.join(Jobcandidate,Candidates.candidate_id == Jobcandidate.candidate_id).filter(Jobcandidate.job_id==job_id).values(Candidates.candidate_id, Candidates.candidate_name, Candidates.candidate_email, Jobcandidate.candidate_status)


    """db_candidate_list = db.session.query(Candidates, Jobs, Jobcandidate).filter(Jobcandidate.job_id == job_id).values(Candidates.candidate_id, Candidates.candidate_name, Candidates.candidate_email, Jobs.job_id, Jobs.job_role, Jobcandidate.candidate_status)"""

    candidates_list = fetch_candidate_list(db_candidate_list,job_id)

    for each_interviewer in interviewer_list_for_roles:
        interviewers_list.append(
            {'interviewers_name': each_interviewer.interviewer_name})

    for each_round in db_round_list:
        rounds_list.append(
            {
            'round_name' : each_round.round_name,
            'round_time' : each_round.round_time,
            'round_description' : each_round.round_description,
            'round_requirement' : each_round.round_requirement
            }
        )
    job_status = Jobs.query.filter(Jobs.job_id==job_id).value(Jobs.job_status)
    rounds_list.append({'job_id':job_id,'job_status':job_status})
    return render_template("role-for-interviewers.html", round=rounds_list, result=interviewers_list,candidates=candidates_list)


def check_jobs_exists(job_role):
    "Check the job already exists in the database"
    fetch_existing_job_role = Jobs.query.all()
    jobs_list = []
    # Fetch the job role
    for each_job in fetch_existing_job_role:
        jobs_list.append(each_job.job_role.lower())

    # Compare the job with database job list
    if job_role.lower() in jobs_list:
        check_job_exists = True
    else:
        check_job_exists = False

    return check_job_exists


def check_not_existing_interviewers(interviewers,actual_interviewers_list):
    "remove the non existing interviewers"
    interviewers = set(interviewers)
    actual_interviewers_list = set(actual_interviewers_list)
    final_interviewers_list = actual_interviewers_list.intersection(interviewers)

    return final_interviewers_list


@app.route("/jobs/add", methods=["GET", "POST"])
@login_required
def add_job():
    "Add ajob through UI"
    if request.method == 'GET':
        all_interviewers = Interviewers.query.all()
        interviewers_list = []
        for each_interviewer in all_interviewers:
            interviewers_list.append(each_interviewer.interviewer_name)

        return render_template("add-jobs.html", result=interviewers_list)

    if request.method == 'POST':
        job_role = request.form.get("role")
        data = {'jobrole': job_role}
        check_job_exists = check_jobs_exists(job_role)
        # If the job is already in the database send failure
        # If it's not there add the new job role and return success
        if check_job_exists != True:
            #new_interviewers_list = []
            interviewers = ast.literal_eval(
                request.form.get("interviewerlist"))
            # I have to remove the duplicates and removing the whitespaces which will be
            # added repeatedly through UI
            interviewers = remove_duplicate_interviewers(interviewers)

            #remove the interviewers if its not in the database
            all_interviewers_list = Interviewers.query.all()
            actual_interviewers_list = []
            for each_interviewer in all_interviewers_list:
                actual_interviewers_list.append(each_interviewer.interviewer_name)
            interviewers = check_not_existing_interviewers(interviewers,actual_interviewers_list)
            job_status = 'Open'
            job_object = Jobs(job_role=job_role, job_status=job_status)
            db.session.add(job_object)
            db.session.commit()
            job_id = job_object.job_id
            # Get the id of the user from the interviewers table
            for each_interviewer in interviewers:
                interviewer_id = db.session.query(Interviewers.interviewer_id).filter(
                    Interviewers.interviewer_name == each_interviewer.strip()).scalar()
                job_interviewer_object = Jobinterviewer(
                    job_id=job_id, interviewer_id=interviewer_id)
                db.session.add(job_interviewer_object)
                db.session.commit()

        else:
            return jsonify(message='The job already exists'), 500
        data = {'jobrole': job_role, 'interviewers': list(interviewers), 'job_status':job_status}
        return jsonify(data)


@app.route("/jobs/delete", methods=["POST"])
@login_required
def delete_job():
    "Deletes a job"
    if request.method == 'POST':
        job_id_to_delete = request.form.get('job-id')
        deleted_role = Jobs.query.filter(
            Jobs.job_id == job_id_to_delete).first()
        data = {'job_role': deleted_role.job_role,
                'job_id': deleted_role.job_id}
        db.session.delete(deleted_role)
        db.session.commit()
        delete_rounds_of_job = Jobround.query.filter(Jobround.job_id==job_id_to_delete).all()
        for each_round in delete_rounds_of_job:
            round_to_delete = each_round.round_id
            db.session.query(Jobround).filter(Jobround.round_id==round_to_delete).delete()
            db.session.commit()
            db.session.query(Rounds).filter(Rounds.round_id==round_to_delete).delete()
            db.session.commit()
        return jsonify(data)


def is_equal(interviewers_name_list, interviewers_list):
    "Check both lists are same or not"
    return sorted(interviewers_name_list) == sorted(interviewers_list)


def get_interviewers_name_for_jobupdate(fetched_job_id):
    "Get the interviewers name from table using Jobid"
    # Fetch the interviewer id based on the job id from the Jobinterviewer table
    interviewers_name_list = []
    get_interviewers_id = Jobinterviewer.query.filter(
        Jobinterviewer.job_id == fetched_job_id).all()
    for each_interviewer_id in get_interviewers_id:
        interviewer_id = each_interviewer_id.interviewer_id
        # Fetch the interviewer name by using the parsed interviewer id in interviewers table
        interviewer_name_for_role = db.session.query(Interviewers.interviewer_name).filter(
            Interviewers.interviewer_id == interviewer_id).scalar()
        interviewers_name_list.append(interviewer_name_for_role)

    return interviewers_name_list


def remove_duplicate_interviewers(interviewers_list):
    "Remove the duplicates from the interviewers list"
    new_interviewers_list = []
    for each_interviewers in interviewers_list:
        new_interviewers_list.append(each_interviewers.strip())
    interviewers = list(set(new_interviewers_list))

    return interviewers


def update_job_interviewer_in_database(job_id, job_role, interviewers_list):
    "Update the Job and Interviewer in database based on the condition"
    edit_job = Jobs.query.filter(
        Jobs.job_id == job_id).update({'job_role': job_role})
    db.session.commit()
    # Fetch the combo id of each row which matches with job id
    fetch_combo_id = Jobinterviewer.query.filter(
        Jobinterviewer.job_id == job_id).values(Jobinterviewer.combo_id)
    list_combo_id = []
    for each_id in fetch_combo_id:
        list_combo_id.append(each_id.combo_id)
    # Delete the existing rows of job-id in the Jobinterviewer
    for each_combo_id in list_combo_id:
        delete_updated_job_id = Jobinterviewer.query.filter(
            Jobinterviewer.combo_id == each_combo_id).one()
        db.session.delete(delete_updated_job_id)
        db.session.commit()
    # Fetch the interviewers id from the interviewers table
    # Add new rows in the Jobinterviewer table with updated interviewer id
    for each_interviewer in interviewers_list:
        interviewer_id = db.session.query(Interviewers.interviewer_id).filter(
            Interviewers.interviewer_name == each_interviewer.strip()).scalar()
        job_interviewer_object = Jobinterviewer(
            job_id=job_id, interviewer_id=interviewer_id)
        db.session.add(job_interviewer_object)
        db.session.commit()


@app.route("/job/<job_id>/edit", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    "Editing the already existing job"
    if request.method == 'GET':
        # Fetch the Job role from the job table
        fetched_job_id = job_id
        get_job_role = Jobs.query.filter(
            Jobs.job_id == fetched_job_id).scalar()
        interviewers_name_list = get_interviewers_name_for_jobupdate(
            fetched_job_id)
        # I am repeating this code here to fetch all the interviewers list.
        # I should refactor it
        all_interviewers = Interviewers.query.all()
        interviewers_list = []
        for each_interviewer in all_interviewers:
            interviewers_list.append(each_interviewer.interviewer_name)
        api_response = {'role_name': get_job_role.job_role, 'job_id': fetched_job_id,
                        'interviewers_name': interviewers_name_list, 'interviewers_list': interviewers_list}

        return render_template("edit-jobs.html", result=api_response)

    if request.method == 'POST':
        # Get the job role and Job ID,and name list
        job_role = request.form.get('role')
        job_id = request.form.get('id')
        data = {'job_role': job_role}
        interviewers_list = ast.literal_eval(
            request.form.get('interviewerlist'))
        # Fetch the interviewers list which is already exists for the job
        interviewers_name_list = get_interviewers_name_for_jobupdate(job_id)
        # Remove the duplicate interviewers
        interviewers_list = remove_duplicate_interviewers(interviewers_list)
        #Check the interviewers are there in the database
        all_interviewers_list = Interviewers.query.all()
        actual_interviewers_list = []
        for each_interviewer in all_interviewers_list:
            actual_interviewers_list.append(each_interviewer.interviewer_name)
        #check the non exisiting interviewers are there
        interviewers_list = check_not_existing_interviewers(interviewers_list,actual_interviewers_list)
        #remove None from the list.Filter remos None from the list if it presents
        interviewers_name_list = list(filter(None,interviewers_name_list))
        # Compare the two list which is fetched from UI and Database
        check_interviewer_list = is_equal(
            interviewers_name_list, interviewers_list)
        # Check the job already exists in the database
        check_job_exists = check_jobs_exists(job_role)
        # These are all the four conditions to be tested for editing
        if (check_job_exists != True and check_interviewer_list != True):
            update_job_interviewer_in_database(
                job_id, job_role, interviewers_list)
            return jsonify(data)
        elif (check_job_exists != True and check_interviewer_list == True):
            update_job_interviewer_in_database(
                job_id, job_role, interviewers_list)
            return jsonify(data)
        elif (check_job_exists == True and check_interviewer_list != True):
            update_job_interviewer_in_database(
                job_id, job_role, interviewers_list)
            return jsonify(data)
        else:
            return jsonify(message='The job already exists,Check before you edit the Jobs'), 500


@app.route("/interviewers/add", methods=["GET", "POST"])
@login_required
def add_interviewers():
    data = {}
    "Adding the interviewers"
    if request.method == 'GET':
        return render_template("add-interviewers.html")
    if request.method == 'POST':
        interviewer_name = request.form.get('name')
        interviewer_email = request.form.get('email').lower()
        interviewer_designation = request.form.get('designation')
        # Check the candidate has been already added or not
        check_interviewer_exists = db.session.query(db.exists().where(
            Interviewers.interviewer_email == interviewer_email)).scalar()
        if check_interviewer_exists == False:
            data = {'interviewer_name': interviewer_name}
            interviewer_object = Interviewers(
                interviewer_name=interviewer_name, interviewer_email=interviewer_email, interviewer_designation=interviewer_designation)
            db.session.add(interviewer_object)
            db.session.commit()
            add_edit_interviewers_in_time_slot_table(interviewer_name)
            return jsonify(data=data)
        else:
            return jsonify(error='Interviewer already exists'), 500


def parse_interview_time(interview_time):
    "Parsing the string into time"
    parsed_interview_time = datetime.datetime.strptime(interview_time,'%Y-%m-%dT%H:%M:%S+05:30')
    return parsed_interview_time.strftime('%H') + ':' + parsed_interview_time.strftime('%M')

def convert_to_timezone(date_and_time):
    "convert the time into current timezone"
    # Current time in UTC
    format = "%Y-%m-%d %H:%M:%S %Z%z"
    # Convert to Asia/Kolkata time zone
    now_asia = date_and_time.astimezone(timezone('Asia/Kolkata'))
    now_asia = now_asia.strftime(format)
    return now_asia

@app.route("/<candidate_id>/<job_id>/<url>/welcome")
def show_welcome(candidate_id, job_id, url):
    "Opens a welcome page for candidates"
    interview_data = {}
    data = {'job_id': job_id,'candidate_id':candidate_id,'url':url}
    s = Serializer('WEBSITE_SECRET_KEY')
    now_utc = datetime.datetime.now(timezone('UTC'))
    current_date_and_time = convert_to_timezone(now_utc)
    current_date_and_time = datetime.datetime.strptime(current_date_and_time,"%Y-%m-%d %H:%M:%S IST+0530")

    try:
        #check the url is valid or not
        fetch_candidate_unique_url = Jobcandidate.query.filter(Jobcandidate.candidate_id==candidate_id).values(Jobcandidate.url)
        for unique_url in fetch_candidate_unique_url:
            candidate_unique_url = unique_url.url
        candidate_unique_url = re.sub(r'^.*/','',candidate_unique_url)
        if candidate_unique_url == url:
            #This query fetches the candidate status id
            url = s.loads(url)
            get_candidate_status = db.session.query(Jobcandidate).filter(Jobcandidate.candidate_id==candidate_id).values(Jobcandidate.candidate_status,Jobcandidate.interview_start_time)
            for candidate_status in get_candidate_status:
                candidate_status_id = candidate_status.candidate_status
                interview_start_time = candidate_status.interview_start_time

            #Fetch the candidate status name from candidatestatus table
            candidate_status = db.session.query(Candidatestatus).filter(Candidatestatus.status_id==candidate_status_id).scalar()
            if(candidate_status.status_name == status.CANDIDTATE_STATUS[1]):
                return render_template("welcome.html",result=data)
            elif (candidate_status.status_name == status.CANDIDTATE_STATUS[2] and datetime.datetime.strptime(interview_start_time,"%Y-%m-%dT%H:%M:%S+05:30") > current_date_and_time):
                #Fetch the candidate name and email
                get_candidate_details = db.session.query(Candidates).filter(Candidates.candidate_id==candidate_id).values(Candidates.candidate_email,Candidates.candidate_id,Candidates.candidate_name)

                #Fetch the interview date and time
                get_interview_details = db.session.query(Jobcandidate).filter(Jobcandidate.candidate_id==candidate_id).values(Jobcandidate.interview_end_time,Jobcandidate.interview_start_time,Jobcandidate.interview_date,Jobcandidate.interviewer_email)
                #Parsing candidate details
                for candidate_detail in get_candidate_details:
                    data = {'candidate_name':candidate_detail.candidate_name,'candidate_email':candidate_detail.candidate_email}
                #Parsing the round details
                candidate_round_details = db.session.query(Candidateround.candidate_id==candidate_id,Candidateround.round_status=='Completed').values(Candidateround.round_id)
                for each_round_detail in candidate_round_details:
                    fetched_round_id = each_round_detail.round_id

                round_info_object = Rounds.query.filter(Rounds.round_id==fetched_round_id).values(Rounds.round_id,Rounds.round_description,Rounds.round_name,Rounds.round_requirement,Rounds.round_time)

                for each_round_info in round_info_object:
                    round_info = {'round_name':each_round_info.round_name,'round_requirements':each_round_info.round_requirement,'round_time':each_round_info.round_time,'round_description':each_round_info.round_description}

                #Parsing Interview details
                for interview_detail in get_interview_details:
                    interview_start_time = parse_interview_time(interview_detail.interview_start_time)
                    interview_end_time = parse_interview_time(interview_detail.interview_end_time)
                    interview_data = {'interview_start_time':interview_start_time,'interview_end_time':interview_end_time,'interview_date':interview_detail.interview_date,'interviewer_email':interview_detail.interviewer_email,'round_time': round_info['round_time'],'round_description':round_info['round_description']}
            else:
                return render_template("expiry.html")

        else:
            return render_template("expiry.html")
    except Exception as e:
        print(e)
        return render_template("expiry.html")

    return render_template("welcome.html",result=data,interview_result=interview_data)


@app.route("/<job_id>/<url>/<candidate_id>/valid",methods=['GET','POST'])
def schedule_interview(job_id,url,candidate_id):
    "Validate candidate name and candidate email"
    if request.method == 'POST':
        candidate_unique_code = request.form.get('unique-code')
        candidate_email = request.form.get('candidate-email')
        #url = request.form.get('url')
        candidate_data = Candidates.query.filter(Candidates.candidate_id == candidate_id).values(Candidates.candidate_email,Candidates.candidate_name)
        for each_info in candidate_data:
            candidate_fetch_email = each_info.candidate_email
            candidate_name = each_info.candidate_name
        return_data = {'job_id':job_id,'candidate_id':candidate_id,'url':url,'candidate_name':candidate_name}
        candidate_code = Jobcandidate.query.filter(Jobcandidate.candidate_id==candidate_id,Jobcandidate.job_id==job_id).value(Jobcandidate.unique_code)
        if candidate_fetch_email.lower() != candidate_email.lower():
            err={'error':'EmailError'}
            return jsonify(error=err,result=return_data)
        elif candidate_code.lower() != candidate_unique_code.lower():
            err={'error':'CodeError'}
            return jsonify(error=err,result=return_data)
        elif (candidate_code.lower() == candidate_unique_code.lower() and candidate_fetch_email.lower() == candidate_email.lower()):
            return_data = {
            'candidate_id':candidate_id,
            'candidate_unique_code':candidate_code,
            'candidate_email':candidate_email,
            'job_id':job_id,
            'candidate_name' :candidate_name
            }
            #Fetch the candidate URL from the db and compare the url which is in the browser
            fetch_candidate_unique_url = Jobcandidate.query.filter(Jobcandidate.candidate_id==candidate_id).values(Jobcandidate.url)
            for unique_url in fetch_candidate_unique_url:
                candidate_unique_url = unique_url.url
            candidate_unique_url = re.sub(r'^.*/','',candidate_unique_url)
            if candidate_unique_url == url:
                session['candidate_info'] = return_data
                err={'error':'Success'}
                return jsonify(error=err,result=return_data)
            else:
                err={'error':'OtherError'}
                return_data = {'job_id':job_id,'candidate_id':candidate_id,'url':url}
                return jsonify(error=err,result=return_data)

        else:
            err={'error':'OtherError'}
            return jsonify(error=err,result=return_data)


@app.route('/<job_id>/get-schedule')
def redirect_get_schedule(job_id):
    "Redirect to the get schedule page"
    #Parsing the round details
    fetched_round_id = None
    candidate_round_details = Candidateround.query.filter(Candidateround.candidate_id==session['candidate_info']['candidate_id'],Candidateround.round_status=='Invitation Sent').values(Candidateround.round_id)
    for each_round_detail in candidate_round_details:
        fetched_round_id = each_round_detail.round_id
    if fetched_round_id == None:
        return render_template("expiry.html")
    else:
        round_info_object = Rounds.query.filter(Rounds.round_id==fetched_round_id).values(Rounds.round_id,Rounds.round_description,Rounds.round_name,Rounds.round_requirement,Rounds.round_time)

        for each_round_info in round_info_object:
            round_info = {'round_name':each_round_info.round_name,'round_requirements':each_round_info.round_requirement,'round_time':each_round_info.round_time,'round_description':each_round_info.round_description,'round_id':each_round_info.round_id}


        data = {
        'candidate_id':session['candidate_info']['candidate_id'],
        'candidate_name':session['candidate_info']['candidate_name'],
        'candidate_email':session['candidate_info']['candidate_email'],
        'job_id':session['candidate_info']['job_id'],
        'round_time': round_info['round_time'],
        'round_description':round_info['round_description'],
        'round_id':round_info['round_id']
        }
        return render_template("get-schedule.html",result=data)


@app.route("/candidate/<candidate_id>/job/<job_id>/invite", methods=["GET", "POST"])
@login_required
def send_invite(candidate_id, job_id):
    "Send an invite to schedule an interview"
    if request.method == 'POST':
        candidate_email = request.form.get("candidateemail")
        candidate_id = request.form.get("candidateid")
        candidate_name = request.form.get("candidatename")
        job_id = request.form.get("jobid")
        generated_url = request.form.get("generatedurl")
        expiry_date = request.form.get("expirydate")
        round_description = request.form.get("rounddescription")
        round_id = request.form.get("roundid")
        round_time = request.form.get("roundtime")
        round_name = request.form.get("roundname")
        round_info = {'round_time':round_time,
                        'round_description':round_description,'round_name':round_name}

        logged_email = session['logged_user']
        generated_url = base_url + generated_url +'/welcome'
        try:
            #Generate unique id to schedule an interview
            unique_code = str(uuid.uuid4()).split('-')[0]
            #Update the unique code into the table
            update_unique_code = Jobcandidate.query.filter(Jobcandidate.candidate_id==candidate_id,Jobcandidate.job_id==job_id).update({'unique_code':unique_code})
            msg = Message("Invitation to schedule an Interview with Qxf2 Services!",
                          sender=("Qxf2 Services","test@qxf2.com"), recipients=[candidate_email], cc=[logged_email])
            msg.html = render_template("send_invite.html", candidate_name=candidate_name, round_name=round_name,round_details=round_description, round_username=candidate_name, link=generated_url, unique_code=unique_code,expiry_date=expiry_date)
            mail.send(msg)
            # Fetch the id for the candidate status 'Waiting on Qxf2'
            #Fetch the candidate status from status.py file also. Here we have to do the comparison so fetching from the status file
            candidate_status_id = db.session.query(Candidatestatus).filter(Candidatestatus.status_name==status.CANDIDTATE_STATUS[1]).scalar()

            #Change the candidate status after the invite has been sent
            candidate_status = Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == job_id).update({'candidate_status':candidate_status_id.status_id})
            db.session.commit()

            #Add the candidate round details in candidateround table
            #As of now I am adding round status as completed we can change this to 'Invite sent'
            """candidate_round_detail = Candidateround.query.filter(Candidateround.candidate_id == candidate_id,Candidateround.job_id == job_id).update({'round_id':round_id,'round_status':'Completed'})"""
            candidate_round_detail = Candidateround(candidate_id=candidate_id,job_id=job_id,round_id=round_id,round_status='Invitation Sent')
            db.session.add(candidate_round_detail)
            db.session.commit()

            error = 'Success'

        except Exception as e:
            error = "Failed"
            return(str(e))

        data = {'candidate_name': candidate_name, 'error': error}

    return jsonify(data)


@app.route("/job/status",methods=["GET","POST"])
def job_status():
    "Change the job status based on the selected dropdown"
    #job_status = request.form.get("jobstatus")
    job_id = request.form.get("jobid")
    status = request.form.get("jobstatus")
    #Get the job status for the job id
    job_status_db = Jobs.query.filter(Jobs.job_id == job_id).value(Jobs.job_status)
    if (job_status_db== 'Close'):
        jobs_status = 'Open'
        job_status = Jobs.query.filter(Jobs.job_id == job_id).update({'job_status':jobs_status})
        db.session.commit()
    else:
        jobs_status = 'Close'
        job_status = Jobs.query.filter(Jobs.job_id == job_id).update({'job_status':jobs_status})
        db.session.commit()

    return jsonify({'job_status':jobs_status})