from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json,ast,sys,os,datetime
from flask_login import login_required

from qxf2_scheduler.models import Jobs, Roundinterviewers, Rounds, Jobround, Interviewers, Roundinterviewers


def fetch_interviewers_for_rounds(round_id,job_id):
    "Fetch interviewers id for the rounds"
    # Fetch the interviewers id for the round
    interviewers_lst_for_rounds = []
    db_interviewer_list_for_rounds = Roundinterviewers.query.filter(Roundinterviewers.job_id == job_id, Roundinterviewers.round_id == round_id).values(Roundinterviewers.interviewers_id)
    for each_interviewer in db_interviewer_list_for_rounds:
        interviewers_lst_for_rounds.append(each_interviewer.interviewers_id)

    return interviewers_lst_for_rounds


def fetch_interviewers_names_for_rounds(round_interviewers_id):
    "Fetch interviewers names from id list"
    #Fetch the interviewers name from the interviewers id
    interviewers_name_list = []
    for each_interviewer_id in round_interviewers_id:
        interviewer_name = Interviewers.query.filter(Interviewers.interviewer_id == each_interviewer_id).value(Interviewers.interviewer_name)
        interviewers_name_list.append(interviewer_name)

    return interviewers_name_list


@app.route("/job/<job_id>/rounds",methods=["GET","POST"])
@login_required
def read_round_details(job_id):
    "read round details"
    if request.method == 'GET':
        rounds_list = []
        db_round_list = db.session.query(Jobround, Rounds).filter(Jobround.job_id == job_id, Rounds.round_id == Jobround.round_id).group_by(Rounds.round_id).values(
        Rounds.round_id,Rounds.round_name,Rounds.round_time,Rounds.round_description,Rounds.round_requirement)

        for each_round in db_round_list:
            round_interviewers_id_list =  fetch_interviewers_for_rounds(each_round.round_id,job_id)
            round_interviewers_names_list =  fetch_interviewers_names_for_rounds(round_interviewers_id_list)
            rounds_list.append(
            {
            'round_id':each_round.round_id,
            'round_name':each_round.round_name,
            'round_time' : each_round.round_time,
            'round_description' : each_round.round_description,
            'round_requirement' : each_round.round_requirement,
            'round_interviewers':round_interviewers_names_list})

    return render_template("rounds.html",result=rounds_list,job_id=job_id)


def fetch_all_interviewers():
    "Fetch all interviewers"
    my_interviewers_list = []
    display_interviewers = Interviewers.query.all()
    for each_interviewer in display_interviewers:
        my_interviewers_list.append({'interviewer_id':each_interviewer.interviewer_id,'interviewer_name':each_interviewer.interviewer_name})

    return my_interviewers_list

@app.route("/jobs/<job_id>/round/add",methods=["GET","POST"])
@login_required
def add_rounds_details(job_id):
    "add rounds details"
    if request.method == "GET":
        #Fetch all the interviewers for adding rounds
        interviewers_list = []
        interviewers_list = fetch_all_interviewers()

    if request.method == "POST":
        data = {}
        round_time = request.form.get('roundTime')
        round_description = request.form.get('roundDescription')
        round_requirements = request.form.get('roundRequirements')
        round_name = request.form.get('roundName')
        added_interviewers = request.form.getlist('addedInterviewers[]')
        data={'round_name':round_name,'job_id':job_id}
        #Adding the round details into the database
        add_round_object = Rounds(round_name=round_name,round_time=round_time,round_description=round_description,round_requirement=round_requirements)
        db.session.add(add_round_object)
        db.session.flush()
        round_id = add_round_object.round_id
        db.session.commit()
        #Adding the round id and interviewers id to the roundinterviewers table
        for each_added_interviewers in added_interviewers:
            add_round_interviewers_object = Roundinterviewers(round_id=round_id,interviewers_id=each_added_interviewers,job_id=job_id)
            db.session.add(add_round_interviewers_object)
            db.session.commit()
        #Adding the round and job id to the jobround table
        add_job_round_object = Jobround(round_id=round_id,job_id=job_id)
        db.session.add(add_job_round_object)
        db.session.commit()
        api_response = {'data':data}

        return jsonify(api_response)

    return render_template("add-rounds.html",job_id=job_id,interviewers=interviewers_list)


@app.route("/rounds/<round_id>/jobs/<job_id>/delete")
@login_required
def delete_round_details(round_id,job_id):
    "delete round details"
    delete_round = Rounds.query.filter(Rounds.round_id == round_id).first()
    db.session.delete(delete_round)
    db.session.commit()
    delete_job_round = Jobround.query.filter(Jobround.job_id == job_id,Jobround.round_id == round_id).first()
    db.session.delete(delete_job_round)
    db.session.commit()

    return jsonify(data="Deleted")


def remove_interviewers_in_common(new_interviewers_list,round_interviewers_id_list):
    "remove interviewers in common"
    for each_interviewers in new_interviewers_list:
        if each_interviewers in round_interviewers_id_list:
            new_interviewers_list.remove(each_interviewers)
            round_interviewers_id_list.remove(each_interviewers)

    return new_interviewers_list, round_interviewers_id_list


def deleting_old_interviewers(round_interviewers_id_list,round_id,job_id):
    "Delete the interviewers which is not there in the new edit"
    for each_remove_interviewers in round_interviewers_id_list:
        remove_interviewer_object = Roundinterviewers.query.filter(Roundinterviewers.interviewers_id==each_remove_interviewers,Roundinterviewers.round_id==round_id,Roundinterviewers.job_id==job_id).first()
        db.session.delete(remove_interviewer_object)
        db.session.commit()

def adding_new_interviewers(new_interviewers_list,round_id,job_id):
    "Adding the new interviewers for the round"
    for each_add_interviewers in new_interviewers_list:
        add_new_interviewer_object = Roundinterviewers(round_id=round_id,job_id=job_id,interviewers_id=each_add_interviewers)
        db.session.add(add_new_interviewer_object)
        db.session.commit()


def check_round_interviewers(round_id,job_id,new_interviewers_list,round_interviewers_id_list):
    "check the interviewers for round"
    if round_interviewers_id_list == new_interviewers_list:
            pass
    else:
        new_interviewers_list,round_interviewers_id_list=remove_interviewers_in_common(new_interviewers_list,round_interviewers_id_list)

    #deleting the old interviewers
    deleting_old_interviewers(round_interviewers_id_list,round_id,job_id)

    #Adding the new interviewers
    adding_new_interviewers(new_interviewers_list,round_id,job_id)


@app.route("/rounds/<round_id>/jobs/<job_id>/edit",methods=["GET","POST"])
@login_required
def edit_round_details(round_id,job_id):
    "Edit the round details"
    if request.method == "GET":
        rounds_list = []
        db_round_list = db.session.query(Rounds).filter(Rounds.round_id == round_id).values(Rounds.round_id,Rounds.round_name,Rounds.round_time,Rounds.round_description,Rounds.round_requirement)
        # Fetch interviewers name list for rounds
        round_interviewers_id_list = fetch_interviewers_for_rounds(round_id,job_id)
        round_interviewers_name_list = fetch_interviewers_names_for_rounds(round_interviewers_id_list)
        # Fetch all interviewers
        interviewers_list = fetch_all_interviewers()

        for each_round in db_round_list:
            rounds_list.append(
            {
            'round_id':each_round.round_id,
            'round_name':each_round.round_name,
            'round_time' : each_round.round_time,
            'round_description' : each_round.round_description,
            'round_requirement' : each_round.round_requirement}
        )
        return render_template("edit-rounds.html",result=rounds_list,job_id=job_id,interviewers_name_list=round_interviewers_name_list,interviewers_list=interviewers_list)

    if request.method=="POST":
        data = {}
        round_time = request.form.get('roundTime')
        round_description = request.form.get('roundDescription')
        round_requirements = request.form.get('roundRequirements')
        round_name = request.form.get('roundName')
        new_interviewers_list = request.form.getlist('editedinterviewers[]')
        data = {'round_name':round_name}
        #Fetch the existing interviewers for the rounds
        round_interviewers_id_list = fetch_interviewers_for_rounds(round_id,job_id)
        #Check tow lists are identical
        check_round_interviewers(round_id,job_id,new_interviewers_list,round_interviewers_id_list)

        edit_round_object = Rounds.query.filter(Rounds.round_id==round_id).update({'round_name':round_name,'round_time':round_time,'round_description':round_description,'round_requirement':round_requirements})
        db.session.commit()
        api_response = {'data':data}
        return (jsonify(api_response))


@app.route("/roundname/get-description",methods=["GET","POST"])
@login_required
def get_round_description():
    "Get the round description"
    round_details = ast.literal_eval(request.form.get("round_name"))
    data={'round_id':round_details[0],'round_name':round_details[1]}
    round_description = db.session.query(Rounds).filter(Rounds.round_id==data['round_id']).scalar()
    round_descriptions = {'round_description':round_description.round_description,'round_id':round_details[0],'round_name':round_details[1],'round_time':round_description.round_time}
    return jsonify(round_descriptions)