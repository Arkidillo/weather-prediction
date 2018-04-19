from flask import Flask , render_template, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps

app = Flask(__name__)


@app.route('/')
def home():
	return 'WEATHER_APP'

if __name__ == '__main__':
    app.secret_key = 'secret12345'
    app.run(debug = True)