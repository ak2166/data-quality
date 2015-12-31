# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Define the blueprint: 'index', set its url prefix: app.url/
ind = Blueprint('index', __name__, url_prefix='/')

# Set the route and accepted methods
@ind.route('index/', methods=['GET'])
def index():
    return render_template("index/index.html")