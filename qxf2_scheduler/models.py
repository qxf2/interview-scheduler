from qxf2_scheduler import db
from sqlalchemy import Integer, ForeignKey, String, Column

class Interviewers(db.Model):
    "Adding the interviewer" 
    interviewer_id = db.Column(db.Integer,primary_key=True,nullable=False)   
    interviewer_name = db.Column(db.String(50),nullable=False)
    interviewer_email = db.Column(db.String(50),nullable=False)
    interviewer_designation = db.Column(db.String(40),nullable=False)
    
    def __repr__(self):
        return f"Interviewers('{self.interviewer_name}', '{self.interviewer_email}','{self.interviewer_designation}'')"

class Interviewertimeslots(db.Model):
    "Adding the timing for interviewer"    
    interviewer_id = db.Column(db.Integer,ForeignKey(Interviewers.interviewer_id),nullable=False)
    time_id = db.Column(db.Integer,primary_key=True)
    interviewer_start_time = db.Column(db.String,nullable=False)
    interviewer_end_time = db.Column(db.String,nullable=False)

    def __repr__(self):
        return f"Interviewertimeslots('{self.interviewer_id}', '{self.interviewer_start_time}','{self.interviewer_end_time}','{self.time_id}'')"

