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
