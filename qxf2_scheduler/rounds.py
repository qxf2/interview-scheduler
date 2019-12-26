from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json,ast,sys

from qxf2_scheduler.models import Jobs, Rounds, Jobround

def check_round_name_exists(round_name):
    "Check the round name already in the database"
    fetch_existing_round_name = Rounds.query.all()
    round_name_list = []
    #Fetch the round names
    for each_round_name in fetch_existing_round_name:           
        round_name_list.append(each_round_name.round_name.lower())
    
    #Compare the job with database job list
    if round_name.lower() in round_name_list:
        check_round_name_exists = True
    else:
        check_round_name_exists = False

    return check_round_name_exists   



@app.route("/job/<job_id>/rounds",methods=["GET","POST"])
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
def add_rounds(job_id):
    "add rounds"
    if request.method == "POST": 
        data = {}       
        round_time = request.form.get('roundTime')
        round_description = request.form.get('roundDescription')
        round_requirements = request.form.get('roundRequirements')
        round_name = request.form.get('roundName')        
        print(round_time,round_description,round_requirements,file=sys.stderr)
        #Check the round has been already added or not
        data={'round_name':round_name,'job_id':job_id}
        check_round_exists = check_round_name_exists(round_name)
        if check_round_exists == True:
            error = 'Failed'
        else:            
            add_round_object = Rounds(round_name=round_name,round_time=round_time,round_description=round_description,round_requirement=round_requirements)
            db.session.add(add_round_object)
            db.session.commit()
            #getting the unique round id for new rounds
            round_id = Rounds.query.filter(Rounds.round_name==round_name).value(Rounds.round_id)            
            #storing the round id and job id in roundjob table
            add_job_round_object = Jobround(round_id=round_id,job_id=job_id)
            db.session.add(add_job_round_object)
            db.session.commit()
            error = 'Success'
        api_response = {'data':data,'error':error}

        return jsonify(api_response) 

    return render_template("add-rounds.html",job_id=job_id)



    
@app.route("/rounds/<round_id>/jobs/<job_id>/delete")
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
    

