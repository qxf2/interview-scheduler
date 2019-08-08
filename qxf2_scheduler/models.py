from qxf2_scheduler import db

class Addinterviewer(db.Model):
    "Adding the interviewer"    
    interviewer_name = db.column(db.string(10),nullable=False)
    interviewer_email = db.column(db.string(30),nullable=False)
    interviewer_designation = db.column(db.string(10),nullable=False)
    
    def __repr__(self):
        return f"Addinterviewer('{self.interviewer_name}', '{self.interviewer_email}','{self.interviewer_designation}'')"