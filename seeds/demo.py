from flask_seeder import Seeder, Faker, generator
from qxf2_scheduler import db
import datetime
from sqlalchemy import DateTime
from qxf2_scheduler.security import encrypt_password

class Jobs(db.Model):
    "Adding the Job page"
    def __init__(self,job_id=None,job_role=None,job_status=None):
        self.job_id = job_id
        self.job_role = job_role
        self.job_status = job_status

    def __str__(self):
        return "job_id=%d, job_role=%s, job_status=%s" % (self.job_id, self.job_role,
        self.job_status)


class Candidates(db.Model):
    "Adding the candidates"
    def __init__(self,candidate_id=None, candidate_name=None, candidate_email=None,job_applied=None,comments=None):
        self.candidate_id = candidate_id
        self.candidate_name = candidate_name
        self.candidate_email = candidate_email
        self.job_applied = job_applied
        self.comments = comments

    def __str__(self):
        return "candidate_id=%d, candidate_name=%s, candidate_email=%s, date_applied=%d, job_applied=%s, comments=%s" %(self.candidate_id, self.candidate_name, self.candidate_email, self.job_applied, self.comments)


class Jobcandidate(db.Model):
    "Combine Job id and Candidate ID"
    def __init__(self, combo_id=None, candidate_id=None, job_id=None, url=None, unique_code=None, interview_start_time=None, interview_end_time=None, interview_date=None, interviewer_email=None, candidate_status=None):
        self.combo_id = combo_id
        self.candidate_id = candidate_id
        self.job_id = job_id
        self.url = url
        self.unique_code = unique_code
        self.interview_start_time = interview_start_time
        self.interview_end_time = interview_end_time
        self.interview_date = interview_date
        self.interviewer_email = interviewer_email
        self.candidate_status = candidate_status

    def __str__(self):
        return "combo_id=%d, candidate_id=%d, job_id=%d, url=%s, unique_code=%s, interview_start_time=%s, interview_end_time=%s, interview_date=%s, interviewer_email=%s, candidate_status=%d"%(self.combo_id, self.candidate_id, self.job_id, self.url, self.unique_code, self.interview_start_time, self.interview_end_time, self.interview_date, self.interviewer_email, self.candidate_status)


class Login(db.Model):
    "Creates username and password"
    def __init__(self, id=None, username=None, password=None, email=None, email_confirmation_sent_on=None, email_confirmed=None, email_confirmed_on=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = email_confirmed
        self.email_confirmed_on = email_confirmed_on

    def __str__(self):
        return "id=%d, username=%s, password=%s, email=%s, email_confirmation_sent_on=%s, email_confirmed=%s, email_confirmed_on=%s"%(self.id, self.username, self.password, self.email, self.email_confirmation_sent_on, self.email_confirmed, self.email_confirmed_on)


class DemoSeeder(Seeder):
    "Creates seeder class"
    def run(self):
        "Create new faker and creates data"
        #Adding user to login
        print("Hi how are you")
        self.login = Login(id=3,username='nilaya', password=encrypt_password("qwerty"), email="nilaya@qxf2.com",email_confirmed=1)
        print(f'Login object{self.login}{type(self.login)}')
        self.db.session.add(self.login)
        self.db.session.commit()

        #Adding jobs
        self.job = Jobs(job_role='Junior QA',job_status='Open')
        self.db.session.add(self.job)
        self.db.session.commit()

        #Adding candidates
        self.add_candidate = Candidates(candidate_name="test_seeder_candidate", candidate_email="annupriyan27+220220212@gmail.com", job_applied="Junior QA", comments="Hi I am the comment. You can add,edit or delete me. Thankyou.")
        self.db.session.add(self.add_candidate)
        self.db.session.commit()

        #Adding candidate status
        self.job_candidate= Jobcandidate(candidate_id=self.add_candidate.candidate_id, job_id=self.job.job_id, url='', candidate_status= 1)
        self.db.session.add(self.job_candidate)
        self.db.session.commit()
