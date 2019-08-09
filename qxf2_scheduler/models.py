from qxf2_scheduler import db
from sqlalchemy import Integer, ForeignKey, String, Column

class Addinterviewer(db.Model):
    "Adding the interviewer" 
    interviewer_id = db.Column(db.Integer,primary_key=True,nullable=False)   
    interviewer_name = db.Column(db.String(50),nullable=False)
    interviewer_email = db.Column(db.String(50),nullable=False)
    interviewer_designation = db.Column(db.String(40),nullable=False)
    
    def __repr__(self):
        return f"Addinterviewer('{self.interviewer_name}', '{self.interviewer_email}','{self.interviewer_designation}'')"

class Intervieweravailability(db.Model):
    "Adding the timing for interviewer" 
    time_availability = db.Column(db.String(20),nullable=False)
    person_id = db.Column(db.Integer,primary_key=True,nullable=False)
    interviewer_id = db.Column(db.Integer,ForeignKey(Addinterviewer.interviewer_id))