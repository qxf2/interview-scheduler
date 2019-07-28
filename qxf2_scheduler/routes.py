"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app
import qxf2_scheduler.qxf2_scheduler as my_scheduler
DOMAIN = 'qxf2.com'

@app.route("/get-schedule", methods=['GET', 'POST'])
def date_picker():
    "Dummy page to let you see a schedule"
    if request.method == 'GET':
        return render_template('get-schedule.html')
    if request.method == 'POST':
        email = request.form.get('email')
        date = request.form.get('date')
        if '@' + DOMAIN == email[-9:]:
            free_slots = my_scheduler.get_free_slots_for_date(email, date)
            api_response = {'free_slots': free_slots, 'email': email, 'date': date}
        else:
            api_response = {'error':'This application will only work for emails ending in @{domain}'.format(domain=DOMAIN)}
        return jsonify(api_response)


@app.route("/")
def index():
    "The index page"
    return "The page is not ready yet!"
