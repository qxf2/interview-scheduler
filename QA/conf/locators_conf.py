#Common locator file for all locators

############################################
#Selectors we can use
#ID
#NAME
#css selector
#CLASS_NAME
#LINK_TEXT
#PARTIAL_LINK_TEXT
#XPATH
###########################################

#Locators for the login object
username_field = "xpath,//input[@id = 'username']"
password_field = "xpath,//input[@id='userpassword']"
login_button = "xpath,//*[@id='loginButton']"
signup_button = "xpath,//*[@id='signupButton']"
user_name_field = "xpath,//input[contains(@name,'uname')]"
email_field = "xpath,//input[contains(@id,'email')]"
password_field = "xpath,//input[contains(@id,'password')]"
confirm_password_field = "xpath,//input[contains(@id,'confirmPassword')]"
submit_button = "xpath,//button[contains(@id,'addSubmit')]"
logout_button = "xpath,//input[contains(@value,'log out')]"

#Locators for the index object
interviewers_page = "xpath,//a[contains(.,'List the interviewers')]"
jobs_page = "xpath,//a[contains(.,'List the jobs')]"
candidates_page = "xpath,//a[contains(.,'List the candidates')]"

#Heading for index page
heading = "xpath,//h2[contains(.,'Why Interview Scheduler Application?')]"

#Locators for Candidates Page
search_option = "xpath,//input[contains(@type,'search')]"
add_candidates_button = "xpath,//input[@id='add']"
delete_candidate = "xpath,//button[contains(@data-candidateid,'')]"
edit_candidate_button = "xpath,//button[@id='edit']"
name_candidates = "xpath,//input[@id='fname']"
email_candidates = "xpath,//input[@id='email']"
job_applied = "xpath,//select[contains(@id,'select1')]"
job_applied_select = "xpath,//option[@value='%s']"
comment_candidates = "xpath,//textarea[@id='comments']"
submit_candidates_button = "xpath,//button[@id='addSubmit']"
delete_candidates_button = "xpath,//button[contains(@data-candidatename,'Nayara')]"
remove_candidates_button = "xpath,//button[@id='remove-button']"
select_candidate_button = "xpath,//a[contains(.,'Nayara')]"
thumbs_up_button = "xpath,//input[@value='Thumbs up']"
thumbs_down_button = "xpath,//input[@value='Thumbs down']"
select_round_level_scroll = "xpath,//select[@id='select1']"
send_email_button = "xpath,//button[contains(.,'Send Email')]"
select_url = "xpath,//label[@class='col-md-8'][contains(.,'http://localhost:6464/')]"
select_unique_code = "xpath,//input[contains(@id,'candidate-name')]"
select_candidate_email = "xpath,//input[contains(@id,'candidate-email')]"
go_for_schedule = "xpath,//input[contains(@id,'submit')]"
date_picker = "xpath,//input[contains(@id,'datepicker')]"
date_on_calendar = "xpath,//a[contains(text(),%s)]"
confirm_interview_date = "xpath,//input[contains(@id,'submit')]"
select_free_slot = "xpath,/html/body/div[1]/div[1]/input"
select_free_slot = "xpath,(//input[@class='btn'])[1]"
schedule_my_interview = "xpath,//input[@value='Schedule my interview']"
calendar_link = "xpath,//a[contains(@target,'blank')]"
google_meet_link = "xpath,//a[contains(.,'Join with Google Meet')]"
email_on_link = "xpath,//input[@type='email']"
next_button = "xpath,//div[@class='VfPpkd-RLmnJb']"
next_button_after_password = "xpath,//*[@id='passwordNext']"
password_link = "xpath,//input[@type='password']"
edit_candidate_page_save_button = "xpath,//button[@class= 'btn btn-info']"

#Locators for Interviewers Page
add_interviewers_button = "xpath,//input[contains(@onclick,'addinterviewer()')]"
interviewers_name = "xpath,//input[contains(@id,'fname')]"
interviewers_email = "xpath,//input[@id='email']"
interviewers_designation = "xpath,//input[contains(@id,'designation')]"
interviewers_starttime = "xpath,//input[contains(@id,'starttime0')]"
interviewers_starttime_drop = "xpath,//a[text()='%s']"
interviewers_endtime = "xpath,//input[contains(@id,'endtime0')] "
interviewers_endtime_drop = "xpath,//a[text()='%s']"
add_time_button = "xpath,//input[contains(@value,'Add time')]"
save_interviewers_button = "xpath,//input[@id='submit']"
cancel_interviewers_button = "xpath,//button[@id='clear']"
close_interviewers_button = "xpath,//button[@id='close']"
delete_interviewers_button = "xpath,//a[text()='nilaya']/parent::td/following-sibling::td/button[@data-toggle='modal']"
remove_interviewers_button = "xpath,//button[contains(@id,'remove-button')]"

#Locators for Jobs Page
add_jobs_button = "xpath,//input[contains(@onclick,'addJob()')]"
job_role = "xpath,//input[contains(@id,'role')]"
job_interviewers = "xpath,//input[contains(@id,'interviewers')]"
submit_job_button = "xpath,//button[contains(@id,'submit')]"
delete_job_button = "xpath,//a[text()='Junior QA']/parent::td/following-sibling::td/button[@data-jobrole='Junior QA']"
remove_job_button = "xpath,//button[@id='remove-button']"

#Locators for Rounds
specific_round_add = "xpath,//a[text()='Junior QA']/parent::td/following-sibling::td/button[text()='Rounds']"
add_rounds_button = "xpath,//input[@value='Add Rounds']"
round_name = "xpath,//input[@id='rname']"
round_duration = "xpath,//select[@name='Duration']"
round_duration_select = "xpath,//option[@value='%s']"
round_description = "xpath,//textarea[@name='rdesc']"
round_requirements = "xpath,//input[@name='rreq']"
add_button = "xpath,//button[@id='addRound']"
cancel_rounds_button = "xpath,//button[@id='cancelRound']"
