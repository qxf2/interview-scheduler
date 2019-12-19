from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json,ast,sys

from qxf2_scheduler.models import Jobs, Rounds, Jobround


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
                  
        return render_template("rounds.html",result=rounds_list,jobs=job_id)

    if request.method == "POST":        
        round_time = request.form.get('duration')
        round_description = request.form.get('description')
        round_requirements = request.form.get('requirements')
        round_name = request.form.get('roundname')        
        print(round_time,round_description,round_requirements,file=sys.stderr)
        #Check the round has been already added or not
        check_round_exists = db.session.query(db.exists().where(Rounds.round_name==round_name)).scalar()
        if check_round_exists == True:
            msg = "The round is already added for the role"            
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
            msg = "The round has been added"
        

        return jsonify(msg) 

    
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