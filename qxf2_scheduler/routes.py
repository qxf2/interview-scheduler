"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json
import sys

from qxf2_scheduler.models import Interviewers, Interviewertimeslots, Jobs, Jobinterviewer
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
        email = request.form.get('emails')
        date = request.form.get('date')
        schedule_event = my_scheduler.create_event_for_fetched_date_and_time(
            date, email, slot)
        value = {'schedule_event': schedule_event, 'date': date}
        value = json.dumps(value)

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
    parsed_interviewer_details = []
    for each_detail in interviewer_details:
        interviewer_detail = {
            'interviewer_id':each_detail.interviewer_id,
            'interviewers_name': each_detail.interviewer_name,
            'interviewers_email': each_detail.interviewer_email,
            'interviewers_designation': each_detail.interviewer_designation,
            'interviewers_starttime': each_detail.interviewer_start_time,
            'interviewers_endtime': each_detail.interviewer_end_time}

        parsed_interviewer_detail = form_interviewer_timeslot(
            time_slot=interviewer_detail)
        if len(parsed_interviewer_details) == 0:
            parsed_interviewer_details.append(parsed_interviewer_detail)
        else:
            if interviewer_detail['interviewers_name'] in parsed_interviewer_details[0].values():
                parsed_interviewer_details[0]['time'] = [
                    parsed_interviewer_details[0]['time'], parsed_interviewer_detail['time']]

    return parsed_interviewer_details


@app.route("/<interviewer_id>/interviewer/")
def read_interviewer_details(interviewer_id):
    "Displays all the interviewer details"
    # Fetching the Interviewer detail by joining the Interviewertimeslots tables and Interviewer tables
    interviewer_details = Interviewers.query.join(Interviewertimeslots, Interviewers.interviewer_id == Interviewertimeslots.interviewer_id).filter(
        Interviewers.interviewer_id == interviewer_id).values(Interviewers.interviewer_id,Interviewers.interviewer_name, Interviewers.interviewer_email, Interviewers.interviewer_designation, Interviewers.interviewer_id, Interviewertimeslots.interviewer_start_time, Interviewertimeslots.interviewer_end_time)

    parsed_interviewer_details = form_interviewer_details(interviewer_details)

    return render_template("read-interviewers.html", result=parsed_interviewer_details)


@app.route("/<interviewer_id>/interviewer/edit/", methods=['GET', 'POST'])
def edit_interviewer(interviewer_id):
    "Edit the interviewers"
    # This query fetch the interviewer details by joining the time slots table and interviewers table.
    edit_interviewer_details = Interviewers.query.join(Interviewertimeslots, Interviewers.interviewer_id == Interviewertimeslots.interviewer_id).values(
        Interviewers.interviewer_id, Interviewers.interviewer_name, Interviewers.interviewer_email, Interviewers.interviewer_designation, Interviewertimeslots.interviewer_start_time, Interviewertimeslots.interviewer_end_time)

    parsed_interviewer_details = form_interviewer_details(
        edit_interviewer_details)

    if request.method == "POST":
        interviewer_name = request.form.get('name')
        data = {'interviewer_name': interviewer_name}
        print("ia interviewer is", interviewer_name, file=sys.stderr)
        edit_interviewers = Interviewers.query.filter(Interviewers.interviewer_id == interviewer_id).update({'interviewer_name': request.form.get(
            'name'), 'interviewer_email': request.form.get('email'), 'interviewer_designation': request.form.get('designation')})
        db.session.commit()

        # Adding the time slots in the interviewerstimeslots table
        interviewer_time_slots = eval(request.form.get('timeObject'))
        interviewer_start_time = interviewer_time_slots['starttime']
        interviewer_end_time = interviewer_time_slots['endtime']

        # Updating the table based on the time id of the interviewertimeslots table
        # Fetching the time ids of interviewer
        total_rows_of_interviewer_in_time_table = Interviewertimeslots.query.filter(
            Interviewertimeslots.interviewer_id == interviewer_id).values(Interviewertimeslots.time_id)

        # Updating the timeslots
        i = 0
        for each_time_id in total_rows_of_interviewer_in_time_table:
            edited_time_slots = Interviewertimeslots.query.filter(Interviewertimeslots.time_id == each_time_id.time_id).update(
                {'interviewer_start_time': interviewer_start_time[i], 'interviewer_end_time': interviewer_end_time[i]})
            i = i + 1
        db.session.commit()

        return jsonify(data)

    return render_template("edit-interviewer.html", result=parsed_interviewer_details)


@app.route("/<interviewer_id>/interviewer/delete", methods=["POST"])
def delete_interviewer(interviewer_id):
    "Deletes a job"
    if request.method == 'POST':
        #interviewer_to_delete = request.form.get('interviewer-id')
        deleted_user = Interviewers.query.filter(
            Interviewers.interviewer_id == interviewer_id).first()
        data = {'interviewer_name': deleted_user.interviewer_name,
                'interviewer_id': deleted_user.interviewer_id}
        db.session.delete(deleted_user)
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


@app.route("/<job_id>/interviewers/")
def interviewers_for_roles(job_id):
    "Display the interviewers based on the job id"
    interviewers_list = []
    interviewer_list_for_roles = Interviewers.query.join(Jobinterviewer, Interviewers.interviewer_id == Jobinterviewer.interviewer_id).filter(
        Jobinterviewer.job_id == job_id).values(Interviewers.interviewer_name)

    for each_interviewer in interviewer_list_for_roles:
        interviewers_list.append(
            {'interviewers_name': each_interviewer.interviewer_name})

    return render_template("role-for-interviewers.html", result=interviewers_list)


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


@app.route("/interviewers/add", methods=["GET", "POST"])
def add_interviewers():
    "Adding the interviewers"
    data = {}
    if request.method == 'GET':
        return render_template("add-interviewers.html")
    if request.method == 'POST':
        try:
            # Adding the name,email,deignation through UI
            interviewer_name = request.form.get('name')
            data = {'interviewer_name': interviewer_name}
            add_interviewers = Interviewers(interviewer_name=request.form.get('name'), interviewer_email=request.form.get(
                'email'), interviewer_designation=request.form.get('designation'))
            db.session.add(add_interviewers)

            # Filtering the interviewer id from the table to use it for interviewertimeslots table
            added_interviewer_id = Interviewers.query.filter(
                Interviewers.interviewer_name == interviewer_name).first()

            # Adding the time slots in the interviewerstimeslots table
            interviewer_time_slots = eval(request.form.get('timeObject'))
            interviewer_start_time = interviewer_time_slots['starttime']
            interviewer_end_time = interviewer_time_slots['endtime']
            len_of_slots = len(interviewer_start_time)
            for i in range(len_of_slots):
                add_time_slots = Interviewertimeslots(interviewer_id=added_interviewer_id.interviewer_id,
                                                      interviewer_start_time=interviewer_start_time[i], interviewer_end_time=interviewer_end_time[i])
                db.session.add(add_time_slots)

        except Exception as e:
            print(e)

        db.session.commit()

        return jsonify(data)
