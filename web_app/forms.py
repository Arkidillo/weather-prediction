from wtforms import Form, SelectField, SubmitField, validators, ValidationError, DateField
from wtforms_components import DateTimeField, DateRange
from datetime import datetime


cities = [('Vancouver', 'Vancouver'), ('Portland', 'Portland'), ('San Francisco', 'San Francisco'), 
('Seattle', 'Seattle'), ('Los Angeles', 'Los Angeles'), ('San Diego', 'San Diego'), 
('Las Vegas', 'Las Vegas'), ('Phoenix', 'Phoenix'), ('Albuquerque', 'Albuquerque'), 
('Denver', 'Denver'), ('San Antonio', 'San Antonio'), ('Dallas', 'Dallas'), ('Houston', 'Houston'), 
('Kansas City', 'Kansas City'), ('Minneapolis', 'Minneapolis'), ('Saint Louis', 'Saint Louis'), 
('Chicago', 'Chicago'), ('Nashville', 'Nashville'), ('Indianapolis', 'Indianapolis'), ('Atlanta', 'Atlanta'),
 ('Detroit', 'Detroit'), ('Jacksonville', 'Jacksonville'), ('Charlotte', 'Charlotte'), ('Miami', 'Miami'), 
 ('Pittsburgh', 'Pittsburgh'), ('Toronto', 'Toronto'), ('Philadelphia', 'Philadelphia'), 
('New York', 'New York'), ('Montreal', 'Montreal'), ('Boston', 'Boston'), ('Beersheba', 'Beersheba'), 
('Tel Aviv District', 'Tel Aviv District'), ('Eilat', 'Eilat'), ('Haifa', 'Haifa'), 
('Nahariyya', 'Nahariyya'), ('Jerusalem', 'Jerusalem')]

'''mytest = [('Vancouver', 'Vancouver'), ('Portland', 'Portland'), ('San Francisco', 'San Francisco')]

mytest2 = [(0, 'Vancouver'), (1, 'Portland'), (2, 'San Francisco')]

print(type(mytest[0][0]))
print(type(mytest[0][1]))'''




class InputForm(Form):
    city = SelectField(label='City', coerce=str, choices=cities)
    date = DateField(label='Date (Y-m-d)', format='%Y-%m-%d' , validators=[DateRange(min=datetime(2017, 1, 1),max=datetime(2017, 11, 30))])
    submit = SubmitField('Submit')