from qxf2_scheduler import db

class Addinterviewer(db.Model):
    "Adding the interviewer" 
    interviewer_id = db.Column(db.Integer(10),primary_key=True,nullable=False)   
    interviewer_name = db.Column(db.String(50),nullable=False)
    interviewer_email = db.Column(db.String(50),nullable=False)
    interviewer_designation = db.Column(db.String(40),nullable=False)
    
    def __repr__(self):
        return f"Addinterviewer('{self.interviewer_name}', '{self.interviewer_email}','{self.interviewer_designation}'')"


class Intervieweravailability(db.model):
    "Adding the interviewer availability"
    person_id = db.Column(db.Integer(10), db.ForeignKey('Addinterviewer.interviewer_id'),nullable=False)
    time_availability = db.Column(db.Integer(10),nullable=False)