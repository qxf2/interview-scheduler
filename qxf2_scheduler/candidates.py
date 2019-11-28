from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
from qxf2_scheduler import db
import json

from qxf2_scheduler.models import Candidates
DOMAIN = 'qxf2.com'

@app.route("/candidates",methods=["GET"])
def read_candidates():
    "Read the candidates"      
    display_candidates = Candidates.query.all()
    my_candidates_list = []
    for each_candidate in display_candidates:
        my_candidates_list.append({'candidate_id':each_candidate.candidate_id,'candidate_name':each_candidate.candidate_name,'candidate_email':each_candidate.candidate_email})
        
    return render_template("read-candidates.html",result=my_candidates_list)


@app.route("/candidate/delete",methods=["POST"]) 
def delete_candidate():
    "Deletes a candidate"
    if request.method== 'POST':
        candidate_id_to_delete = request.form.get('candidateId')
        candidate_to_delete = Candidates.query.filter(Candidates.candidate_id==candidate_id_to_delete).first()
        data = {'candidate_name':candidate_to_delete.candidate_name,'candidate_id':candidate_to_delete.candidate_id}       
        db.session.delete(candidate_to_delete)
        db.session.commit()        
        
    return jsonify(data)


