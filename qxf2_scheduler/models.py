from qxf2_scheduler import db
import datetime
from sqlalchemy import Integer, ForeignKey, String, Column,CheckConstraint,DateTime
from sqlalchemy.sql import table, column
from flask_seeder import Seeder, Faker, generator


class Interviewers(db.Model):
    "Adding the interviewer"
    interviewer_id = db.Column(db.Integer,primary_key=True)
    interviewer_name = db.Column(db.String(50),nullable=False)
    interviewer_email = db.Column(db.String(50),nullable=False)
    interviewer_designation = db.Column(db.String(40),nullable=False)
    db.CheckConstraint(interviewer_name > 5)

    def __repr__(self):
        return f"Interviewers('{self.interviewer_name}', '{self.interviewer_email}','{self.interviewer_designation}')"


class Interviewertimeslots(db.Model):
    "Adding the timing for interviewer"
    time_id = db.Column(db.Integer,primary_key=True)
    interviewer_id = db.Column(db.Integer,db.ForeignKey(Interviewers.interviewer_id),nullable=False)
    interviewer_start_time = db.Column(db.String,nullable=False)
    interviewer_end_time = db.Column(db.String,nullable=False)

    def __repr__(self):
        return f"Interviewertimeslots('{self.interviewer_id}', '{self.interviewer_start_time}','{self.interviewer_end_time}','{self.time_id}')"


class Jobs(db.Model):
    "Adding the Job page"
    job_id = db.Column(db.Integer,primary_key=True,nullable=False)
    job_role = db.Column(db.String,nullable=False)
    job_status = db.Column(db.String)

    def __repr__(self):
        return f"Jobs('{self.job_id}','{self.job_role}')"


class Jobinterviewer(db.Model):
    "Combine Job id and Interviewer ID"
    combo_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    job_id = db.Column(db.Integer,ForeignKey(Jobs.job_id))
    interviewer_id = db.Column(db.Integer,ForeignKey(Interviewers.interviewer_id))

    def __repr__(self):
        return f"Jobinterviewer('{self.job_id}','{self.interviewer_id}')"


class Candidates(db.Model):
    "Adding the candidates"
    candidate_id = db.Column(db.Integer,primary_key=True,nullable=False)
    candidate_name = db.Column(db.String,nullable=False)
    candidate_email = db.Column(db.String,nullable=False)
    date_applied = db.Column(DateTime, default=datetime.datetime.utcnow)
    job_applied = db.Column(db.String,nullable=False)
    comments = db.Column(db.String)
    last_updated_date = db.Column(db.String)

    def __repr__(self):
        return f"Candidates('{self.candidate_name}','{self.candidate_email}')"


class Rounds(db.Model):
    "Adding the rounds"
    round_id = db.Column(db.Integer,primary_key=True)
    round_name = db.Column(db.String,nullable=False)
    round_time = db.Column(db.String,nullable=False)
    round_description = db.Column(db.String,nullable=False)
    round_requirement = db.Column(db.String,nullable=False)


    def __repr__(self):
        return f"Rounds('{self.round_time}','{self.round_description}','{self.round_requirement}','{self.round_name}','{self.added_interviewers}')"


class Roundinterviewers(db.Model):
    "Adding interviewers for rounds"
    combo_id = db.Column(db.Integer,primary_key=True)
    round_id = db.Column(db.Integer,ForeignKey(Rounds.round_id))
    interviewers_id = db.Column(db.Integer,ForeignKey(Interviewers.interviewer_id))
    job_id = db.Column(db.Integer,ForeignKey(Jobs.job_id))

    def __repr__(self):
        return f"Roundinterviewers('{self.round_id}','{self.interviewers_id}')"


class Jobcandidate(db.Model):
    "Combine Job id and Candidate ID"
    combo_id = db.Column(db.Integer,primary_key=True)
    candidate_id = db.Column(db.Integer,ForeignKey(Candidates.candidate_id))
    job_id = db.Column(db.Integer,ForeignKey(Jobs.job_id))
    url = db.Column(db.String)
    unique_code = db.Column(db.String)
    interview_start_time = db.Column(db.String)
    interview_end_time = db.Column(db.String)
    interview_date = db.Column(db.String)
    interviewer_email = db.Column(db.String)
    candidate_status = db.Column(db.String)

    def __repr__(self):
        return f"Jobcandidate('{self.candidate_id}','{self.job_id}','{self.url}','{self.candidate_status}','{self.interview_start_time}','{self.unique_code}')"


class Jobround(db.Model):
    "Combine Job id and Round id"
    combo_id = db.Column(db.Integer,primary_key=True)
    job_id = db.Column(db.Integer,ForeignKey(Jobs.job_id))
    round_id = db.Column(db.Integer,ForeignKey(Rounds.round_id))

    def __repr__(self):
        return f"Jobround('{self.job_id}','{self.round_id}')"


class Candidateround(db.Model):
    "Combine candidate id and round id"
    combo_id = db.Column(db.Integer,primary_key=True)
    job_id = db.Column(db.Integer,ForeignKey(Jobs.job_id))
    candidate_id = db.Column(db.Integer,ForeignKey(Candidates.candidate_id))
    round_id = db.Column(db.Integer,ForeignKey(Rounds.round_id))
    round_status = db.Column(db.String)
    candidate_feedback = db.Column(db.String)
    thumbs_value = db.Column(db.String)

class Candidatestatus(db.Model):
    "Save the status list"
    status_id = db.Column(db.Integer,primary_key=True)
    status_name = db.Column(db.String)


class Updatetable(db.Model):
    "Store the last updated date of Jobcandidate"
    table_id = db.Column(db.Integer,primary_key=True)
    last_updated_date = db.Column(db.Integer)


class Candidateinterviewer(db.Model):
    "Combine candidate id ,interviewer id and round id,job id"
    combo_id = db.Column(db.Integer,primary_key=True)
    job_id = db.Column(db.Integer,ForeignKey(Jobs.job_id))
    candidate_id = db.Column(db.Integer,ForeignKey(Candidates.candidate_id))
    interviewer_id = db.Column(db.Integer,ForeignKey(Interviewers.interviewer_id))

    def __repr__(self):
        return f"Candidateinterviewer('{self.job_id}','{self.candidate_id}','{self.interviewer_id}')"


class Interviewcount(db.Model):
    "Keep the number of interview count for interviewers"
    id = db.Column(db.Integer, primary_key=True)
    interviewer_id = db.Column(db.Integer,ForeignKey(Interviewers.interviewer_id))
    interview_count = db.Column(db.Integer)

    def __repr__(self):
        return f"Interviewcount('{self.interviewer_id}','{self.interview_count}')"
