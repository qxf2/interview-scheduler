"""
This file contains all the endpoints exposed by the interview scheduler application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response
from qxf2_scheduler import app

@app.route("/get-schedule")
def date_picker():
    "Dummy page to let you see a schedule"
    return render_template('get-schedule.html')

@app.route("/")
def index():
    "The index page"
    return "This page is not ready yet!"