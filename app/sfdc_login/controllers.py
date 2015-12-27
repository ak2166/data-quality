# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

#Import simple salesforce
from simple_salesforce import Salesforce

# Import module forms
from app.sfdc_login.forms import LoginForm

# Define the blueprint: 'login', set its url prefix: app.url/login
login = Blueprint('login', __name__, url_prefix='/auth')

# Set the route and accepted methods
@login.route('/signin/', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        sf = Salesforce(username=form.email.data, password=form.password.data, security_token=form.token.data)
        print sf.query('SELECT Id FROM Account')

    return render_template("auth/signin.html", form=form)
