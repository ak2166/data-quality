# Import flask dependencies
from flask import Flask, Blueprint, request, render_template, session, flash, g, redirect, url_for

# Import the secure_filename 
from werkzeug import secure_filename

# Import our upload form
from app.csv_analysis.forms import UploadForm
import os

# Import Data Processing Libraries
import pandas
import numpy as np

# Import Seaborn for vis
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
import StringIO, base64

# Define the blueprint: 'login', set its url prefix: app.url/login
upload = Blueprint('upload', __name__, url_prefix='/')

# We will only allow text or csv files to be uploaded
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Set the route and accepted methods
@upload.route('upload/', methods=['GET', 'POST'])
def upload_file():

	form = UploadForm(request.form)
	if request.method == 'POST' and 'uploaded_csv' in request.files:
		file = request.files['uploaded_csv']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(os.getcwd()+'/app/uploads/', filename))
			session['delimiter'] = form.delimiter.data
			session['filename'] = filename
			return redirect(url_for('upload.data_analysis'))
	return render_template('upload_templates/upload_file.html', form = form)

@upload.route('analysis/', methods=['GET', 'POST'])
def data_analysis():

	filepath = os.path.join(os.getcwd()+'/app/uploads/', session['filename'])
	print session['delimiter']
	if unicode(session['delimiter']) != '' :
		sep = unicode(session['delimiter'])
	else:
		sep = ','

	# Now build dataframe
	df = pandas.read_csv(filepath, sep = sep, na_values='unknown')
	row_count = len(df.index)

	# Populate the field object list 
	field_list = []
	for i in range(0, len(df.columns)):

		# Field Object 
		field = {}

		field['name'] = str(df.columns[i])
		field['num_records'] = df.iloc[:,i].count()
		field['num_unique'] = len(df.iloc[:,i].unique())
		field['max_length'] = df.iloc[:,i].map(lambda x: len(str(x))).max()
		field['dtype'] = df.iloc[:, i].dtype
		field['plot_url'] = ''
		field['uniqueness'] = field['num_unique']/field['num_records']
		field['percentage_nna'] = format(float(field['num_records'])/len(df.iloc[:, i])*100.0, '.2F')
		if field['num_unique'] < 30 and field['num_unique'] > 0:
			field['value_count'] = df.iloc[:, i].value_counts()
			img = StringIO.StringIO()
			plot = sns.countplot(df.iloc[:, i], palette='Blues_d')
			locs, labels = plt.xticks()
			if field['num_unique'] > 15:
				plot.set_xticklabels(labels, rotation=45)
			elif field['num_unique'] > 4:
				plot.set_xticklabels(labels, rotation=15)
			else:
				plot.set_xticklabels(labels, rotation=0)
			fig = plot.get_figure()
			fig.savefig(img, format='png')
			img.seek(0)
			field['plot_url'] = base64.b64encode(img.getvalue())
		field_list.append(field)

	#Finally delete the file
	os.remove(filepath)
	return render_template('upload_templates/display_stats.html', field_list = field_list, row_count = row_count)