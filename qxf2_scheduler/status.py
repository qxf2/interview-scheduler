from flask import render_template, url_for, flash, redirect, jsonify, request, Response,session
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
import qxf2_scheduler.candidate_status as status
from qxf2_scheduler import db
import json
import string
import random,sys

from qxf2_scheduler.models import Candidatestatus

@app.route("/status",methods=["GET","POST"])
def read_status():
    "Display the statuses from the database"
    read_status = db.session.query(Candidatestatus).all()
    my_status_list = []
    for each_status in read_status:
        my_status_list.append({'status_id':each_status.status_id,'status_name':each_status.status_name})
    
    return render_template("read-status.html",result=my_status_list)