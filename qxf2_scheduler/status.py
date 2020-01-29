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


@app.route("/status/<status_id>/delete",methods=["POST"]) 
def delete_status(status_id):
    "Deletes a candidate"
    if request.method == 'POST':
        status_id_to_delete = request.form.get('statusid')        
        #Delete the status from status table
        status_to_delete = Candidatestatus.query.filter(Candidatestatus.status_id==status_id_to_delete).first()
        data = {'status_name':status_to_delete.status_name,'status_id':status_to_delete.status_id}       
        db.session.delete(status_to_delete)
        db.session.commit() 
                
    return jsonify(data)