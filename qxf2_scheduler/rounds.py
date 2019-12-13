from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json,ast,sys

from qxf2_scheduler.models import Jobs, Rounds

@app.route("/job/<job_id>/rounds",methods=["GET","POST"])
def read_round_details(job_id):
    "read round details"
    if request.method == 'GET':
        round_details = db.session.query(Rounds).values(Rounds.round_time,Rounds.round_description,Rounds.round_requirement)
        for each_round in round_details:
            data = {'job_id':job_id,'round_time':each_round.round_time,'round_description':each_round.round_description,'round_requirements':each_round.round_requirement}
        print("data",data)
    
        return render_template("rounds.html",result=data)

    if request.method == "POST":
        print("I am coming here",file=sys.stderr)
        round_time = request.form.get('duration')
        round_description = request.form.get('round_description')
        round_requirements = request.form.get('round_requirements')
        add_round_object = Rounds({'round_time':round_time,'round_description':round_description,'round_requirement':round_requirements})
        db.session.add(add_round_object)
        db.session.commit()

