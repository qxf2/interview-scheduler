from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json,ast,sys,os,datetime
from qxf2_scheduler.authentication_required import Authentication_Required
from qxf2_scheduler.models import Jobs, Rounds, Jobround, Interviewers


@app.route("/job/<job_id>/rounds",methods=["GET","POST"])
@Authentication_Required.requires_auth
def read_round_details(job_id):
    "read round details"
    if request.method == 'GET':
        rounds_list = []
        db_round_list = db.session.query(Jobround, Rounds).filter(Jobround.job_id == job_id, Rounds.round_id == Jobround.round_id).group_by(Rounds.round_id).values(
        Rounds.round_id,Rounds.round_name,Rounds.round_time,Rounds.round_description,Rounds.round_requirement)
        for each_round in db_round_list:
            rounds_list.append(
            {
            'round_id':each_round.round_id,
            'round_name':each_round.round_name,
            'round_time' : each_round.round_time,
            'round_description' : each_round.round_description,
            'round_requirement' : each_round.round_requirement}
        )

        return render_template("rounds.html",result=rounds_list,job_id=job_id)


@app.route("/jobs/<job_id>/round/add",methods=["GET","POST"])
@Authentication_Required.requires_auth
def add_rounds_details(job_id):
    "add rounds details"
    if request.method == "POST":
        data = {}
        round_time = request.form.get('roundTime')
        round_description = request.form.get('roundDescription')
        round_requirements = request.form.get('roundRequirements')
        round_name = request.form.get('roundName')
        added_interviewers = request.form.getlist('addedInterviewers[]')
        data={'round_name':round_name,'job_id':job_id}
        print(added_interviewers)
        #Adding the round details into the database
        add_round_object = Rounds(round_name=round_name,round_time=round_time,round_description=round_description,round_requirement=round_requirements)
        db.session.add(add_round_object)
        db.session.flush()
        round_id = add_round_object.round_id
        db.session.commit()
        #Adding the round and job id to the jobround table
        add_job_round_object = Jobround(round_id=round_id,job_id=job_id)
        db.session.add(add_job_round_object)
        db.session.commit()
        api_response = {'data':data}

        return jsonify(api_response)

    return render_template("add-rounds.html",job_id=job_id)


@app.route("/rounds/<round_id>/jobs/<job_id>/delete")
@Authentication_Required.requires_auth
def delete_round_details(round_id,job_id):
    "delete round details"
    delete_round = Rounds.query.filter(Rounds.round_id == round_id).first()
    db.session.delete(delete_round)
    db.session.commit()
    delete_job_round = Jobround.query.filter(Jobround.job_id == job_id,Jobround.round_id == round_id).first()
    db.session.delete(delete_job_round)
    db.session.commit()

    return jsonify(data="Deleted")


@app.route("/rounds/<round_id>/jobs/<job_id>/edit",methods=["GET","POST"])
@Authentication_Required.requires_auth
def edit_round_details(round_id,job_id):
    "Edit the round details"
    if request.method == "GET":
        rounds_list = []
        db_round_list = db.session.query(Rounds).filter(Rounds.round_id == round_id).values(
        Rounds.round_id,Rounds.round_name,Rounds.round_time,Rounds.round_description,Rounds.round_requirement)
        for each_round in db_round_list:
            rounds_list.append(
            {
            'round_id':each_round.round_id,
            'round_name':each_round.round_name,
            'round_time' : each_round.round_time,
            'round_description' : each_round.round_description,
            'round_requirement' : each_round.round_requirement}
        )
        return render_template("edit-rounds.html",result=rounds_list,job_id=job_id)

    if request.method=="POST":
        data = {}
        round_time = request.form.get('roundTime')
        round_description = request.form.get('roundDescription')
        round_requirements = request.form.get('roundRequirements')
        round_name = request.form.get('roundName')
        data = {'round_name':round_name}
        edit_round_object = Rounds.query.filter(Rounds.round_id==round_id).update({'round_name':round_name,'round_time':round_time,'round_description':round_description,'round_requirement':round_requirements})
        db.session.commit()
        api_response = {'data':data}
        return (jsonify(api_response))


@app.route("/roundname/get-description",methods=["GET","POST"])
@Authentication_Required.requires_auth
def get_round_description():
    "Get the round description"
    round_details = ast.literal_eval(request.form.get("round_name"))
    data={'round_id':round_details[0],'round_name':round_details[1]}
    round_description = db.session.query(Rounds).filter(Rounds.round_id==data['round_id']).scalar()
    round_descriptions = {'round_description':round_description.round_description,'round_id':round_details[0],'round_name':round_details[1],'round_time':round_description.round_time}
    return jsonify(round_descriptions)