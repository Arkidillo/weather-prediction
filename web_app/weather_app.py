from flask import Flask , render_template, flash, redirect, url_for, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField


from functools import wraps
from forms import InputForm


app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
	form = InputForm()
	#if request.method == 'POST' and form.validate():
	if request.method == 'POST' and form.validate():
		print(request.form['city'])
		print(request.form['date'])
		return render_template('index.html', form=form)
	
	return render_template('index.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'secret12345'
    app.run(debug = True)