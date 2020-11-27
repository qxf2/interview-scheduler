"""
1. Fetch the username and password and id from the login table
2. Take the password and call the encrypt_password method
3. Update the password in the table
"""
from qxf2_scheduler.security import encrypt_password
from qxf2_scheduler.models import Login
from qxf2_scheduler import db

#Fetch the users from the login table
all_users = Login.query.all()
print(all_users)

for each_user in all_users:
    print(each_user.id)
    encrypted_password = encrypt_password(each_user.password)
    Login.query.filter(Login.id == each_user.id).update({'password':encrypted_password})
    db.session.commit()