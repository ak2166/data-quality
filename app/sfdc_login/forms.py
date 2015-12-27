# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class LoginForm(Form):
    email = TextField('Salesforce Username', [Email(),
            	Required(message='Please enter your SFDC Username')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])
    token = TextField('Salesforce Security Token')
