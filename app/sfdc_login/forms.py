# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form, widgets

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, SelectMultipleField, widgets # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# Define the login form (WTForms)
class LoginForm(Form):
    email = TextField('Salesforce Username', [Email(),
            	Required(message='Please enter your SFDC Username')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])
    token = TextField('Salesforce Security Token')


# Define the list of objects we will use to create
class SelectForm(Form):
	selected_objects = MultiCheckboxField("SelectedObjects", coerce=int)
