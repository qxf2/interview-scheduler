"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response, session
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json,datetime
import ast
import sys
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from datetime import datetime


from qxf2_scheduler.models import Interviewers, Interviewertimeslots, Jobs, Jobinterviewer, Rounds, Jobround,Candidates,Jobcandidate
DOMAIN = 'qxf2.com'


@app.route("/get-schedule", methods=['GET', 'POST'])
def date_picker():
    "Dummy page to let you see a schedule"
    if request.method == 'GET':
        return render_template('get-schedule.html')
    if request.method == 'POST':
        date = request.form.get('date')
        new_slot = Interviewers.query.join(Interviewertimeslots, Interviewers.interviewer_id == Interviewertimeslots.interviewer_id).values(
            Interviewers.interviewer_email, Interviewertimeslots.interviewer_start_time, Interviewertimeslots.interviewer_end_time)
        interviewer_work_time_slots = []
        for interviewer_email, interviewer_start_time, interviewer_end_time in new_slot:
            interviewer_work_time_slots.append({'interviewer_email': interviewer_email, 'interviewer_start_time': interviewer_start_time,
                                                'interviewer_end_time': interviewer_end_time})
        free_slots = my_scheduler.get_free_slots_for_date(
            date, interviewer_work_time_slots)
        free_slots_in_chunks = my_scheduler.get_free_slots_in_chunks(
            free_slots)
        api_response = {
            'free_slots_in_chunks': free_slots_in_chunks, 'date': date}
        
        return jsonify(api_response)


@app.route("/confirm")
def confirm():
    "Confirming the event message"
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
        schedule_event = my_scheduler.create_event_for_fetched_date_and_time(
            date, email,candidate_email, slot)
        date_object = datetime.strptime(date, '%m/%d/%Y').date()
        date = datetime.strftime(date_object, '%B %d, %Y')
        value = {'schedule_event': schedule_event, 
        'date': date,
        'slot' : slot}
        value = json.dumps(value)
        candidate_status = Jobcandidate.query.filter(Jobcandidate.candidate_id == candidate_id, Jobcandidate.job_id == job_id).update({'candidate_status':'Interview Scheduled','interview_start_time':schedule_event[0]['start']['dateTime'],'interview_end_time':schedule_event[1]['end']['dateTime'],'interview_date':date})
        db.session.commit()        
        return redirect(url_for('confirm', value=value))
    return render_template("get-schedule.html")


@app.route("/")
def index():
    "The index page"
    return "The page is not ready yet!"


@app.route("/interviewers")
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


@app.route("/jobs/")
def jobs_page():
    "Displays the jobs page for the interview"
    display_jobs = Jobs.query.all()
    my_job_list = []
    for each_job in display_jobs:
        my_job_list.append(
            {'job_id': each_job.job_id, 'job_role': each_job.job_role})

    return render_template("list-jobs.html", result=my_job_list)


@app.route("/<job_id>/details/")
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
    db_candidate_list = Candidates.query.join(Jobcandidate,Candidates.candidate_id == Jobcandidate.candidate_id).filter(Jobcandidate.job_id==job_id).values(Candidates.candidate_name)

    for each_interviewer in interviewer_list_for_roles:
        interviewers_list.append(
            {'interviewers_name': each_interviewer.interviewer_name})

    for each_round in db_round_list:
        rounds_list.append(
            {
            'round_name' : each_round.round_name,
            'round_time' : each_round.round_time,
            'round_description' : each_round.round_description,
            'round_requirement' : each_round.round_requirement}
        )

    for each_candidate in db_candidate_list:
        candidates_list.append(
            {'candidate_name': each_candidate.candidate_name})

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


@app.route("/jobs/add", methods=["GET", "POST"])
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
            """for each_interviewers in interviewers:
                new_interviewers_list.append(each_interviewers.strip())
            interviewers=list(set(new_interviewers_list))"""
            job_object = Jobs(job_role=job_role)
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
        data = {'jobrole': job_role, 'interviewers': interviewers}

        return jsonify(data)


@app.route("/jobs/delete", methods=["POST"])
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

@app.route("/<candidateId>/<jobId>/<url>/welcome")
def show_welcome(candidateId, jobId, url):
    "Opens a welcome page for candidates"
    data = {'candidate_id':candidateId,'job_id': jobId,'url':url}

    return render_template("welcome.html", result=data)    

@app.route("/<candidate_id>/<job_id>/<url>/welcome")
def show_welcome(candidate_id, job_id, url):
    "Opens a welcome page for candidates"
    interview_data = {}
    data = {'job_id': job_id}
    s = Serializer('WEBSITE_SECRET_KEY')
    try:
        url = s.loads(url)    
        #Check the candidate status if it's interview scheduled
        get_candidate_status = db.session.query(Jobcandidate).filter(Jobcandidate.candidate_id==candidate_id).values(Jobcandidate.candidate_status)
        for candidate_status in get_candidate_status:
            candidate_status = candidate_status.candidate_status
        if candidate_status == 'Waiting on Candidate':
            return render_template("welcome.html",result=data)

        elif candidate_status == 'Interview Scheduled':
            #Fetch the candidate name and email
            get_candidate_details = db.session.query(Candidates).filter(Candidates.candidate_id==candidate_id).values(Candidates.candidate_email,Candidates.candidate_id,Candidates.candidate_name)

            #Fetch the interview date and time
            get_interview_details = db.session.query(Jobcandidate).filter(Jobcandidate.candidate_id==candidate_id).values(Jobcandidate.interview_end_time,Jobcandidate.interview_start_time,Jobcandidate.interview_date)

            #Parsing candidate details
            for candidate_detail in get_candidate_details:
                data = {'candidate_name':candidate_detail.candidate_name,'candidate_email':candidate_detail.candidate_email}

            #Parsing Interview details
            for interview_detail in get_interview_details:            
                interview_start_time = parse_interview_time(interview_detail.interview_start_time)
                interview_end_time = parse_interview_time(interview_detail.interview_end_time)
                interview_data = {'interview_start_time':interview_start_time,'interview_end_time':interview_end_time,'interview_date':interview_detail.interview_date}
    except:
        return render_template("expiry.html")

    return render_template("welcome.html",result=data,interview_result=interview_data)

    
@app.route("/<jobId>/valid",methods=['GET','POST'])
def schedule_interview(jobId):
    "Validate candidate name and candidate email"
    if request.method == 'POST':
        candidate_name = request.form.get('candidate-name')
        candidate_email = request.form.get('candidate-email')
        candidate_data = Candidates.query.filter(Candidates.candidate_email == candidate_email.lower()).value(Candidates.candidate_name)
        candidate_id = Candidates.query.filter(Candidates.candidate_email == candidate_email.lower()).value(Candidates.candidate_id)
        if candidate_data == None:
            err={'error':'EmailError'}
            return jsonify(error=err), 500

        elif candidate_data.lower() != candidate_name.lower():
            err={'error':'NameError'}
            return jsonify(error=err), 500
        elif candidate_data.lower() == candidate_name.lower():
            data = {
            'candidate_id':candidate_id,
            'candidate_name':candidate_name,
            'candidate_email':candidate_email,
            'job_id':jobId 
            }
            session['candidate_info'] = data
            return redirect(url_for('redirect_get_schedule',jobId=jobId))
        else:
            err={'error':'OtherError'}
            return jsonify(error=err), 500


@app.route('/<jobId>/get-schedule')
def redirect_get_schedule(jobId):
    "Redirect to the get schedule page"
    data = {
    'candidate_id':session['candidate_info']['candidate_id'],
    'candidate_name':session['candidate_info']['candidate_name'],
    'candidate_email':session['candidate_info']['candidate_email'],
    'job_id':session['candidate_info']['job_id']
    }
    return render_template("get-schedule.html",result=data)
