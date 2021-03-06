# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

#Import simple salesforce
from simple_salesforce import Salesforce

# Import module forms
from app.sfdc_login.forms import LoginForm, SelectForm

# Define the blueprint: 'login', set its url prefix: app.url/login
login = Blueprint('login', __name__, url_prefix='/auth')
sf = None
# Set the route and accepted methods
@login.route('/signin/', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
	form = LoginForm(request.form)
	# Verify the sign in form
	if form.validate_on_submit():
		session['un'] = form.email.data
		session['pw'] = form.password.data
		session['tk'] = form.token.data
		return redirect(url_for('login.display'))
	return render_template("auth/signin.html", form=form)

@login.route('/displayobjects/', methods=['GET', 'POST'])
def display():

	sf = Salesforce(username=session['un'], password=session['pw'], security_token=session['tk'])
	object_dict = {}
	object_list = []
	form = SelectForm(request.form)
	form.selected_objects.choices = []
	for index, x in enumerate(sf.describe()['sobjects']):
			field_list = []
			if (x['name'] in ['Account', 'Contact', 'Asset', 'Campaign', 'Case', 'CaseComment', 'Contract', 'Idea', 'Lead', 'Opportunity', 'Quote', 'Task', 'Event']) or x['name'].endswith('__c'):
				#for field in getattr(sf, x['name']).describe()['fields']:
				#	field_list.append(unicode([x['name']][0]))
				form.selected_objects.choices.append((index, unicode([x['name']][0])))
				#object_dict[x['name'][0]] = field_list
	if request.method == 'POST':
		print request.form.getlist('checkbox_list')
	return render_template("auth/select_objects.html", form = form,)