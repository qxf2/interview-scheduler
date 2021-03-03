"""
This class models the form on the Selenium tutorial page
The form consists of some input fields, a dropdown, a checkbox and a button
"""
import sys
import os
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from .Base_Page import Base_Page
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Form_Object:
    "Page object for the Form"

    #locators
    username_field = locators.username_field
    password_field = locators.password_field
    user_name_field = locators.user_name_field
    email_field = locators.email_field
    password_field = locators.password_field
    confirm_password_field = locators.confirm_password_field
    login_button = locators.login_button
    signup_button = locators.signup_button
    submit_button = locators.submit_button
    logout_button = locators.logout_button
    redirect_title = "redirect"

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_user(self, username):
        "Set the name on the form"
        result_flag = self.set_text(self.username_field, username)
        self.conditional_write(result_flag,
                               positive='Set the name to: %s'%username,
                               negative='Failed to set the name in the form',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_password(self, password):
        "Set the email on the form"
        result_flag = self.set_text(self.password_field, password)
        self.conditional_write(result_flag,
                               positive='Set the password to: %s'%password,
                               negative='Failed to set the password in the form',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_login(self):
        "Click on 'Login' button"
        result_flag = self.click_element(self.login_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the "Login" button',
                               negative='Failed to click on "Login" button',
                               level='debug')
        result_flag = self.alert_accept()

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def alert_accept(self):
        "Click on 'Ok' alert"
        result_flag = self.alert_window()
        return result_flag
        self.conditional_write(result_flag,
                               positive='Clicked on the OK',
                               negative='Failed to click on OK',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def login_page(self, username, password):
        "Login Wrapper method"
        result_flag = self.set_user(username)
        result_flag &= self.set_password(password)
        result_flag &= self.click_login()

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def signup(self):
        "Click on 'Signup' button"
        result_flag = self.click_element(self.signup_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the "Signup" button',
                               negative='Failed to click on "Signup" button',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_username(self, username):
        "Set the user name on the registration form"
        result_flag = self.set_text(self.user_name_field, username)
        self.conditional_write(result_flag,
                               positive='Set the name to: %s'% username,
                               negative='Failed to set the name in the form',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_email(self, email):
        "Set the user name on the registration form"
        result_flag = self.set_text(self.email_field, email)
        self.conditional_write(result_flag,
                               positive='Set the email to: %s'% email,
                               negative='Failed to set the email in the form',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_password(self, password):
        "Set the password on the registration form"
        result_flag = self.set_text(self.password_field, password)
        self.conditional_write(result_flag,
                               positive='Set the password to: %s'% password,
                               negative='Failed to set the password in the form',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def confirm_password(self, password):
        "Set the confirm password on the registration form"
        result_flag = self.set_text(self.confirm_password_field, password)
        self.conditional_write(result_flag,
                               positive='Set the confirm password to: %s'% password,
                               negative='Failed to set the confirm password in the form',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit(self):
        "Click on 'Submit' button"
        result_flag = self.click_element(self.submit_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the "Submit" button',
                               negative='Failed to click on "Submit" button',
                               level='debug')

        result_flag = self.alert_accept()

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def accept_terms(self):
        "Accept the terms and conditions"
        result_flag = self.select_checkbox(self.tac_checkbox)
        self.conditional_write(result_flag,
                               positive='Accepted the terms and conditions',
                               negative='Failed to accept the terms and conditions',
                               level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def check_redirect(self):
        "Check if we have been redirected to the redirect page"
        result_flag = False
        if self.redirect_title in self.driver.title:
            result_flag = True
            self.switch_page("redirect")

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit_signup_form(self, username, email, password):
        "Submit the form"
        result_flag = self.set_username(username)
        result_flag &= self.set_email(email)
        result_flag &= self.enter_password(password)
        result_flag &= self.confirm_password(password)
        result_flag &= self.submit()

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def logout_page(self):
        "Click on 'Logout' button"
        result_flag = self.click_element(self.logout_button)
        self.conditional_write(result_flag,
                               positive='Clicked on the "Logout" button',
                               negative='Failed to click on "Logout" button',
                               level='debug')

        return result_flag
