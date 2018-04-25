from flask import Flask , render_template, flash, redirect, url_for, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from datetime import datetime, date, timedelta
import os
from functools import wraps
from forms import InputForm
import pandas as pd
import pickle  
import numpy as np



# Create constants for dirs
training_dir = 'city_training/'
test_dir = 'city_testing/'

# Create constants for filenames
city_attrib_file = 'city_attributes.csv'
humidity_file = 'humidity.csv'
pressure_file = 'pressure.csv'
temperature_file = 'temperature.csv'
weather_description_file = 'converted.csv'
wind_direction_file = 'wind_direction.csv'
wind_speed_file = 'wind_speed.csv'

models_folder = 'model_pickles/'

training_date_range = ('2013-10-2', '2016-12-31')
test_date_range = ('2017-1-1', '2017-11-30')
# List of all independent variable files we are pulling data from
attrib_files = [humidity_file, pressure_file, temperature_file, weather_description_file, wind_direction_file, wind_speed_file]
# List of all independent variables (not files)
attribs = []
for attrib_file in attrib_files:
    attribs.append(attrib_file[:-4])


# Create lists of 12 cities
cities = list(pd.read_csv(humidity_file, sep=',').columns.values)
cities.remove('datetime')

attrib_dfs = []
for file in attrib_files:
    attrib_dfs.append(pd.read_csv(file, sep=','))




def get_avg(dataframe, city, date):
    strdate = date.strftime("%Y-%m-%d")
    daily = dataframe[['datetime', city]].copy() #create dataframe of just datetimes and that city 
    day = daily[daily['datetime'].str.contains(strdate)]   #filter above dataframe for a specific day
    valGood = day.dropna()
    vals = list(valGood[city])     #create list of all temps for that day
    return np.mean(vals)


# Get today's attribute (avg'ed) based on city and csv_file
# Args:
    # city_name = name of city you want the data of
    # date = the current date in datetime, from which you want 1 year ago and the past 3 days
    # csv_file = the attribute you want to get
# Returns:
    # the avg of the attribute for the given day and city
def get_today_attrib(city_name, date, attrib_df):
    return get_avg(attrib_df, city_name, date)


# Parse datetime from Y-m-d strings
def get_datetime(date):
    return datetime.strptime(date, '%Y-%m-%d')
 
def get_df_test_file(city):
    return pd.read_csv(test_dir + city + '_test.csv')

# Predict all attributes given a date (as string) and city,
# Returns: (prediction, true values)
def predict_all_attrib(city, date):
    
    city_folder = models_folder + city + '/'
    
    all_model_files = os.listdir(city_folder)
    all_models = []
    for model_file in all_model_files:
        filename = city_folder + model_file
        all_models.append( ( pickle.load(open(filename, 'rb')) , model_file.rstrip('.pkl') ) )
        
    
    test_df = get_df_test_file(city)
    
    # Get what row we want from the test file
    date = get_datetime(date)
    delta = date - get_datetime(test_date_range[0])
    row_index_from_date = delta.days
    
    test_X = test_df.loc[row_index_from_date][:-6].values.reshape(1, -1)
    
    predicted_attribs = {}
    true_attribs = {}
    
    

    for model, attrib in all_models:        
        predicted_attrib = model.predict(test_X)
        predicted_attribs[attrib] = round(float(predicted_attrib), 3)

        # Index into the global attrib array
        attrib_index = attribs.index(attrib)
        
        true_attrib = get_today_attrib(city, date, attrib_dfs[attrib_index])
        true_attribs[attrib] = round(true_attrib, 3)

        
    return [predicted_attribs, true_attribs]



app = Flask(__name__)


def validate_date(date_text):
    try:
        date = datetime.strptime(date_text, '%Y-%m-%d')
        if date.year != 2017:
        	return 0
        if date.month > 11:
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
			city = request.form['city']
			date = request.form['date']
			file = 'images/' + city + '.jpg'
			results = predict_all_attrib(city, date)
			print(results[0])


			return render_template('submission.html', city = request.form['city'], date = request.form['date'], city_image = file, results = results)
		else:
			return render_template('errorindex.html',  form=form)	
	return render_template('index.html', form=form)



@app.route('/submission')
def submission():
	return render_template('submission.html')


if __name__ == '__main__':
    app.secret_key = 'secret12345'
    app.run(debug = True)