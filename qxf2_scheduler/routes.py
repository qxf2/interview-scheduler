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
def listinterviewers():
    "List all the interviewer names"
    all_interviewers = Interviewers.query.all()
    my_interviewers_list = []
    for each_interviewer in all_interviewers:
        my_interviewers_list.append({'interviewer_id': each_interviewer.interviewer_id,
                                     'interviewer_name': each_interviewer.interviewer_name})

    return render_template("list-interviewers.html", result=my_interviewers_list)


def parse_interviewer_detail(interviewer_details):
    "Parse the interviewer detail with start and end time"
    time_dict = {}
    time_dict['starttime'] = interviewer_details['interviewers_starttime']
    time_dict['endtime'] = interviewer_details['interviewers_endtime']
    del interviewer_details['interviewers_starttime']
    del interviewer_details['interviewers_endtime']
    interviewer_details['time'] = time_dict

    return interviewer_details


@app.route("/<interviewer_id>/interviewer/")
def read_interviewer_details(interviewer_id):
    "Displays all the interviewer details"
    parsed_interviewer_details = []
    interviewer_details = Interviewers.query.join(Interviewertimeslots, Interviewers.interviewer_id == Interviewertimeslots.interviewer_id).filter(
        Interviewers.interviewer_id == interviewer_id).values(Interviewers.interviewer_name, Interviewers.interviewer_email, Interviewers.interviewer_designation, Interviewers.interviewer_id, Interviewertimeslots.interviewer_start_time, Interviewertimeslots.interviewer_end_time)
    for each_detail in interviewer_details:
        interviewer_detail = {
            'interviewers_id': each_detail.interviewer_id,
            'interviewers_name': each_detail.interviewer_name,
            'interviewers_email': each_detail.interviewer_email,
            'interviewers_designation': each_detail.interviewer_designation,
            'interviewers_starttime': each_detail.interviewer_start_time,
            'interviewers_endtime': each_detail.interviewer_end_time}

        parsed_interviewer_detail = parse_interviewer_detail(
            interviewer_detail)
        if not parsed_interviewer_details:
            parsed_interviewer_details.append(parsed_interviewer_detail)
        else:
            if interviewer_detail['interviewers_name'] in parsed_interviewer_details[0].values():
                parsed_interviewer_details[0]['time'] = [
                    parsed_interviewer_details[0]['time'], parsed_interviewer_detail['time']]

    return render_template("read-interviewers.html", result=parsed_interviewer_details)


@app.route("/<interviewer_id>/interviewer/edit/")
def edit_interviewer(interviewer_id):
    "Edit the interviewers"
    print(interviewer_id, type(interviewer_id), file=sys.stderr)
    interviewer_id = interviewer_id.strip("'")
    print(interviewer_id, file=sys.stderr)
    """edit_interviewer_details = Interviewers.query.filter(Interviewers.interviewer_id == interviewer_id).values(
        Interviewers.interviewer_id, Interviewers.interviewer_name, Interviewers.interviewer_email, Interviewers.interviewer_designation)"""
    edit_interviewer_details = Interviewers.query.join(Interviewertimeslots, Interviewers.interviewer_id == Interviewertimeslots.interviewer_id).values(
        Interviewers.interviewer_id, Interviewers.interviewer_name, Interviewers.interviewer_email, Interviewers.interviewer_designation, Interviewertimeslots.interviewer_start_time, Interviewertimeslots.interviewer_end_time)
    for each_detail in edit_interviewer_details:
        interviewer_detail = {
            'interviewers_id': each_detail.interviewer_id,
            'interviewers_name': each_detail.interviewer_name,
            'interviewers_email': each_detail.interviewer_email,
            'interviewers_designation': each_detail.interviewer_designation,
            'interviewers_starttime': each_detail.interviewer_start_time,
            'interviewers_endtime':each_detail.interviewer_end_time
        }
        print(interviewer_detail, file=sys.stderr)
    return render_template("edit_interviewer.html",result=interviewer_detail)


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
