from flask_seeder import Seeder, Faker, generator

class Interviewers(db.Model):
    "Adding the interviewer"
    def __init__(self, interviewer_id=None, interviewer_name=None, interviewer_email=None,interviewer_designation=None):
        self.interviewer_id = interviewer_id
        self.interviewer_name = interviewer_name
        self.interviewer_email = interviewer_email
        self.interviewer_designation = interviewer_designation

    def __str__(self):
        return "interviewer_id=%d, interviewer_name=%s, interviewer_email=%s, interviewer_designation=%s" % (self.interviewer_id, self.interviewer_name, sself.interviewer_email, self.interviewer_designation )

class Demoseeder(Seeder):
    "Creates seeder class"
    def run(self):
        "Create new faker and creates data"
        faker = Faker(cls=Interviewers,
                    init={"interviewer_id":generator.Sequence(),
                          "interviewer_name":generator.Name(),
                          "interviewer_email":generator.Email(),
                          "interviewer_designation":generator.Name()})

        for user in faker.create(5):
            print("Adding user: %s" % user)
            self.db.session.add(user)
