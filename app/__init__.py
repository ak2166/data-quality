# Import flask and template operators
from flask import Flask, render_template


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (sfdc_login)
from app.sfdc_login.controllers import login
from app.index_mod.controllers import ind
from app.csv_analysis.controllers import upload

# Register blueprint(s)
app.register_blueprint(ind)
app.register_blueprint(login)
app.register_blueprint(upload)
# app.register_blueprint(xyz_module)
# ..
