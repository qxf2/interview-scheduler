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


def check_status_exists(status_name):
    "Check the status already exists in the database"
    fetch_existing_status_name = Candidatestatus.query.all()
    status_list = []
    # Fetch the status name
    for each_status in fetch_existing_status_name:
        status_list.append(each_status.status_name.lower())

    # Compare the job with database job list
    if status_name.lower() in status_list:
        check_status_exists = True
    else:
        check_status_exists = False

    return check_status_exists



@app.route("/status/add",methods=["GET","POST"])
def add_status():
    "Add a status through UI"
    if request.method == 'GET':
        return render_template("add-status.html")
    if request.method == 'POST':
        data ={}
        status_name = request.form.get("statusname")
        data = {'status_name':status_name}
        status_exists = check_status_exists(status_name)
        if status_exists == True:
            error = "Failed"            
        else:
            add_status_object = Candidatestatus(status_name=status_name)
            db.session.add(add_status_object)
            db.session.commit()
            error = "Success"

        api_response = {'data':data,'error':error}

        return jsonify(api_response)


@app.route("/status/<status_id>/edit",methods=["GET","POST"])
def edit_status(status_id):
    "Edit the status through UI"
    if request.method == "GET":
        data = {}
        get_edit_status_details = Candidatestatus.query.filter(Candidatestatus.status_id==status_id).first()
        data = {'status_name':get_edit_status_details.status_name,'status_id':get_edit_status_details.status_id}
        return render_template("edit-status.html",result=data)
    
    if request.method == "POST":
        edit_status_name = request.form.get('statusname')
        check_edited_status_exists = check_status_exists(edit_status_name)
        if check_edited_status_exists == True:
            error ="Failed"
        else:
            edit_status_object = Candidatestatus.query.filter(Candidatestatus.status_id==status_id).update({"status_name":edit_status_name})
            db.session.commit()
            data = {'status_name':edit_status_name,'status_id':status_id}
            error = "Success"
        api_response = {'data':data,'error':error}
        return (jsonify(api_response))
