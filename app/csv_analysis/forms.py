# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, BooleanField

# Define the login form (WTForms)
class UploadForm(Form):
    
    delimiter = TextField('Fields Delimited By')
    data_row = TextField('Data Begins on Row')
    contains_header = BooleanField('Has header row')
