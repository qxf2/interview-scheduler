#Common locator file for all locators
#Locators are ordered alphabetically

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

#Locators for interview-Scheduler application

#Locators for Interview-scheduler for Add interviewer:

add_button = "xpath,//input[contains(@id,'add')]"

interviewer_name = "xpath,//input[contains(@id,'fname')]"

interviewer_email = "xpath,//input[contains(@id,'email')]"

interviewer_designation = "xpath,//input[contains(@id,'designation')]"

starttime = "xpath,//input[contains(@id,'starttime0')]"

set_starttime = "xpath,//a[contains(text(),'00:30')]"

endtime = "xpath,//input[contains(@id,'endtime0')]"

set_endtime = "xpath,//a[contains(text(),'07:30')]"

submit = "xpath,//input[contains(@id,'submit')]"

#Locators for Interview-scheduler for delete interviewer:

url = "http://3.219.215.68/interviewers"

find_table = "xpath,//div[@class='container col-md-offset-1']"

find_rows = "xpath,//td//a[contains(@href,'interviewer')]"

delete_button = "xpath,(//td//button[contains(@text,Delete)])[%d]"#'(//button[text()="Delete"])[1]'

confirmation_Pop_up = "xpath,//button[@id='remove-button']"

close_pop_up = "xpath,//button[@id='close-button']"

interviewer_name = "xpath,//th[contains(text(),'Interviewer Name')]"

column_header = "xpath,//div[@class='container col-md-offset-1']//thead/descendant::th"

tab_rows = "xpath,//div[@class='container col-md-offset-1']//tbody/descendant::tr"

relative_xpath = "xpath,//div[@class='container col-md-offset-1']//tbody/descendant::tr[%d]/descendant::td"

