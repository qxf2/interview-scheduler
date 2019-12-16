from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json,ast,sys

from qxf2_scheduler.models import Jobs, Rounds

@app.route("/job/<job_id>/rounds")
def read_round_details(job_id):
    "read round details"
    data = {}
    round_details = db.session.query(Rounds).values(Rounds.round_time,Rounds.round_description,Rounds.round_requirement)
    for each_round in round_details:
        data = {'round_time':each_round.round_time,'round_description':each_round.round_description,'round_requirements':each_round.round_requirement}
    
    return render_template("rounds.html",result=data)