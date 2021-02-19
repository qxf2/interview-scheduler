from flask_seeder import Seeder, Faker, generator
from qxf2_scheduler import db


class Interviewers(db.Model):
    "Adding the interviewer"
    def __init__(self, interviewer_id=None, interviewer_name=None, interviewer_email=None,interviewer_designation=None):
        self.interviewer_id = interviewer_id
        self.interviewer_name = interviewer_name
        self.interviewer_email = interviewer_email
        self.interviewer_designation = interviewer_designation

    def __str__(self):
        return "interviewer_id=%d, interviewer_name=%s, interviewer_email=%s, interviewer_designation=%s" % (self.interviewer_id, self.interviewer_name, self.interviewer_email, self.interviewer_designation )


class Interviewertimeslots(db.Model):
    "Adding the timing for interviewer"
    def __init__(self,time_id=None,interviewer_id=None,interviewer_start_time=None,interviewer_end_time=None):
        self.time_id = time_id
        self.interviewer_id = interviewer_id
        self.interviewer_start_time = interviewer_start_time
        self.interviewer_end_time = interviewer_end_time

    def __str__(self):
        return "time_id=%d, interviewer_id=%d, interviewer_start_time=%s, interviewer_end_time=%s" % (self.time_id, self.interviewer_id, self.interviewer_start_time, self.interviewer_end_time)

class Jobs(db.Model):
    "Adding the Job page"
    def __init__(self,job_id=None,job_role=None,job_status=None):
        self.job_id = job_id
        self.job_role = job_role
        self.job_status = job_status

    def __str__(self):
        return "job_id=%d, job_role=%s, job_status=%s" % (self.job_id, self.job_role,
        self.job_status)


class Jobinterviewer(db.Model):
    "Combine Job id and Interviewer ID"
    def __init__(self,combo_id=None,job_id=None,interviewer_id=None):

        self.combo_id = combo_id
        self.job_id = job_id
        self.interviewer_id = interviewer_id

    def __str__(self):
        return "combo_id=%d, job_id=%s, interviewer_id=%s" % (self.combo_id, self.job_id, self.interviewer_id)


class DemoSeeder(Seeder):
    "Creates seeder class"
    def run(self):
        "Create new faker and creates data"
        names_list = ['mak','avinash']
        email_list = ['mak@qxf2.com','avinash@qxf2.com']
        start_time = ["10:00","12:00"]
        end_time = ["21:00","23:00"]
        for i,names in enumerate(names_list):
            self.user= Interviewers(interviewer_name=names,interviewer_email=email_list[i],interviewer_designation="Manager")
            self.db.session.add(self.user)
            self.db.session.commit()
            print(f'adding:{self.user}')
            #Adding time slots for interviewers
            time_slot = Interviewertimeslots(interviewer_id=self.user.interviewer_id,interviewer_start_time=start_time[i],interviewer_end_time=end_time[i])
            self.db.session.add(time_slot)
            self.db.session.commit()
        print(self.user)

        #Adding jobs
        self.job = Jobs(job_role='Junior QA',job_status='Open')
        self.db.session.add(self.job)
        self.db.session.commit()

        self.job_interviewer = Jobinterviewer(job_id=self.job.job_id,interviewer_id=self.user.interviewer_id)
        self.db.session.add(self.job_interviewer)
        self.db.session.commit()

