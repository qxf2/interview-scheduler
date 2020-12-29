from qxf2_scheduler import app
from flask import render_template, request, url_for, jsonify
from qxf2_scheduler import db
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail
from qxf2_scheduler.models import Login
from qxf2_scheduler.security import encrypt_password

mail = Mail(app)

def check_email_confirmed(email_id):
    "Check email address is confirmed"
    email_confirmed = Login.query.filter(Login.email == email_id).value(Login.email_confirmed)

    return email_confirmed


@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(app.secret_key)
        email = password_reset_serializer.loads(token, salt='scheduler-password-reset', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('login'))
    print(email)

    return render_template('reset_password_with_token.html',email=email)


def send_email(subject, recipients, text_body):
    "Send the email"
    msg = Message(subject, recipients=recipients)
    msg.html = text_body
    mail.send(msg)


def send_password_reset_email(user_email):
    "Send the password reset email"
    password_reset_serializer = URLSafeTimedSerializer(app.secret_key)
    password_reset_url = url_for(
        'reset_with_token',
        token = password_reset_serializer.dumps(user_email, salt='scheduler-password-reset'),
        _external=True)
    html = render_template(
        'email_password_reset.html',
        password_reset_url=password_reset_url)
    send_email('Password Reset Requested', [user_email], html)


@app.route("/reset-password", methods=["GET","POST"])
def reset_password():
    "Reset the password"
    if request.method == 'GET':
        return render_template("reset-password.html")
    if request.method == 'POST':

        email_id = request.form.get("emailid")
        print(email_id)
        email_confirmation = check_email_confirmed(email_id)
        print(email_confirmation)
        if email_confirmation:
            print("email is confirmed",email_id)
            send_password_reset_email(email_id)
            error = "Success"
        else:
            error = "error"
            print("email is not confirmed")
        data = {'email_id':email_id, 'error':error}
        return jsonify(data)


@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if request.method == 'POST':
        user_email = request.form.get("useremail")
        new_password = request.form.get("newpassword")
        print(user_email,new_password)
        Login.query.filter(Login.email == user_email).update({'password':encrypt_password(new_password)})
        db.session.commit()
        error = "Success"
    result = {'error':error}

    return jsonify(result)
