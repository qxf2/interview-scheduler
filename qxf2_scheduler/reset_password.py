from qxf2_scheduler import app
from flask import render_template, request
from qxf2_scheduler import db

from qxf2_scheduler.models import Login

@app.route("/reset-password", methods=["GET","POST"])
def reset_password():
    "Reset the password"
    if request.method == 'GET':
        return render_template("reset-password.html")
    if request.method == 'POST':
        email_id = request.form.get("emailid")
        print(email_id)
        return email_id