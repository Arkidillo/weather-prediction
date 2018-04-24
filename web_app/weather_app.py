from flask import Flask , render_template, flash, redirect, url_for, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from datetime import datetime, date, timedelta

from functools import wraps
from forms import InputForm


app = Flask(__name__)

def validate_date(date_text):
    try:
        date = datetime.strptime(date_text, '%Y-%m-%d')
        if date.year != 2017:
        	return 0 
    except ValueError:
        return 0	

@app.route('/', methods=['GET', 'POST'])
def index():
	form = InputForm()

	#if request.method == 'POST' and form.validate():
	if request.method == 'POST':
		if validate_date(request.form['date']) != 0:
		#datetime_object = datetime.strptime(request.form['date'], '%Y-%m-%d')
			print(request.form['city'])
			print(request.form['date'])
			return 'THIS IS A TEST'
		else:
			return render_template('errorindex.html',  form=form)	
	return render_template('index.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'secret12345'
    app.run(debug = True)