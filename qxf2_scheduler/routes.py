"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler

@app.route("/get-schedule", methods=['GET', 'POST'])
def date_picker():
    "Dummy page to let you see a schedule"
    if request.method == 'GET':
        return render_template('get-schedule.html')
    if request.method == 'POST':
        email = request.form.get('email')
        date = request.form.get('date')
        free_slots = my_scheduler.get_free_slots_for_date(email, date)
        api_response = {"free_slots": free_slots, "email": email, "date": date}
        return jsonify(api_response)


@app.route("/")
def index():
    "The index page"
    return "The page is not ready yet!"
