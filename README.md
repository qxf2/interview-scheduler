# interview-scheduler
This repo contains code needed for the Qxf2 interview scheduler application. Please follow the setup instructions to start using the application.

----

### 1. MOTIVATION 


a. Allow Qxf2 to handle a large volume of interview candidates without having to bother about scheduling

b. Make the interaction with Qxf2 different from other companies 

c. Remind candidates at key moments during the process about Qxf2's features

d. Reduce (almost eliminate) exchange of emails between candidate and interviewer

The interview scheduler application should replace the scheduling work Gracy and Smitha did when we hired Rohini. 

### 2. SETUP

__a) Python__

This project uses Python 3.7.4 or higher.


__b)Setup your virtualenv__

1. Install virtualenv

            pip install virtualenv

2. After installing virtualenv open the terminal and go to the directory of your project or the repository exists

3. In the terminal now type the below command


            virtualenv -p <full path to the Python executable> <name of the virtual env>

            E.g.: virtualenv -p /c/Python37/bin/python.exe name of the virtualenv

            E.g.: virtualenv -p /usr/local/bin/python3.7 name of the virtualenv

4. Now it's time to activate your virtualenv. To do that type the below command in the terminal

            (Unix) source name of your virtualenv/bin/activate

            (Windows)source name of your virtualenv/scripts/activate

5. You can see your virtualenv name in the terminal. Once you have finished your work you can do the deactivation by typing the below command in the terminal
      
            deactivate

6. From next time onwards you can don't need to repeat steps 1 to 4.You can directly goto step 4 and work on your project and to stop you can do step 5


__c) Install the required Python modules:__

With your virtualenv activated, run the following command:

            pip install -r requirements.txt


__d) Google calendar setup__

If you are not from Qxf2, please create a token.pickle file using this link: [Google Calendar API: Python quickstart](https://developers.google.com/calendar/quickstart/python)

Place the token.pickle file in the root directory of this project (same directory as this readme).


If you are from Qxf2, please ask a colleague for the token.pickle file


__e) Verify Google calendar setup__

To verify your Google calendar setup, try the following command

            python utils/verify_gcal_setup.py <your_email_id> 

If all went well, you should see 10 upcoming events for the email id you provided.

__f) Start the application__

To start the application, run

      python run.py

The command should be run from the root directory (same as the directory of this readme). If all goes well, when you visit http://localhost:6464 on your browser, you should see the homepage of the application.


__g) Initial db setup__

1] Open the interview-scheduler folder and create another folder named "data"(This folder is Database folder)

2]The above created "data" folder will be empty initially.
      
      For the first time While creating the db run the following command

      "python migrate_db.py db init"
      
Now We have to migrate the required data to this "data" folder. Migrating Database can be done by using the following command
      
      ==>  'python migrate_db.py db  migrate'  (The command should be ran inside the interview-scheduler directory)

3]Once you follow the above step you will see that Database has be created. 

      The created database will be with '.db'extension, i.e (<Filename>.db)

4]So now we should add the required tables by using the following command
      
      ==> 'python migrate_db.py db upgrade'
      
      Whenever we change the structure of table we should again "migrate" and "Upgrade" the db.

5] To check if the tables have been added:
      
open your terminal go to the interview scheduler directory and  Move in to the data folder and follow the commands. 

      ** sqlite3 should be installed in your PC

      .open <filename with extension>

      To check the table names: .table

      To check the structure of table: .schema

6] NOTE: DATA cannot be migrated. You should add your own data to db and proceed.
