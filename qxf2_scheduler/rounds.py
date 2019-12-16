from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json,ast,sys

from qxf2_scheduler.models import Jobs, Rounds, Jobround

@app.route("/job/<job_id>/rounds")
def read_round_details(job_id):
    "read round details"
    round_details = []
    round_details_obj = db.session.query(Jobs,Rounds,Jobround).filter(Jobs.job_id==job_id,Jobround.job_id==job_id,Rounds.round_id==Jobround.round_id).values(Rounds.round_id,Rounds.round_time,Rounds.round_description,Rounds.round_requirement)
    for each_round in round_details_obj:
        data = {'job_id':job_id,'round_id':each_round.round_id,'round_time':each_round.round_time,'round_description':each_round.round_description,'round_requirement':each_round.round_requirement}
        round_details.append(data)

    return render_template("rounds.html",result=round_details)


@app.route("/rounds/<job_id>/<round_id>/delete")
def delete_round_details(job_id,round_id):
    "delete round details"
    delete_round = Rounds.query.filter(Rounds.round_id == round_id).first()
    db.session.delete(delete_round)
    db.session.commit()
    delete_job_round = Jobround.query.filter(Jobround.job_id == job_id,Jobround.round_id == round_id).first()
    db.session.delete(delete_job_round)
    db.session.commit()

    return jsonify(data="Deleted")