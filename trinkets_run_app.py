#--------------------------------
# app config
#--------------------------------
from flask import Flask, request, render_template
import trinkets #this is temp data
#print(trinkets.data)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'katyb3e1smyfav0re3'


#--------------------------------
# restful api operations
#--------------------------------	
from flask_restful import Resource, Api
from random import randint

api = Api(app)

class alltrinkets(Resource):
	def get(self):
			query = trinkets.data
			print(query)
			return query

# get the full list of trinket data
api.add_resource(alltrinkets, '/trinkets')


class trinket(Resource):
	def get(self, trinket):
			query = trinkets.data[ int( trinket ) ]
			return query

# get specific trinkets by their ids
api.add_resource(trinket, '/trinkets/<trinket>')

#--------------------------------
# logic for web forms
#--------------------------------
#this can become part of the below class
def genRandTrinkList(how_many):
	from random import sample

	trinket_name_list = []

	trinket_count = sample(range(0, 7), how_many) #this range needs to read the current min & max ids from the db...
	
	for t in trinket_count:
		#note the dependancy on the trinket api class
		trinket_name_list.extend( [ trinket.get(0,t)["trinket"] ] ) #add the returned trinket name to the list

	return trinket_name_list


from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

class genRandTrinkForm(FlaskForm):
	radio = RadioField(
		'pick how many trinkets',
		validators = [DataRequired()],
		choices=[(0, 'zero'),(1,'one'),(2,'two'),(3,'three'),(4,'four')],
		coerce=int #this returns the radio value as an integer. Flask wtf defaults to returning a string
	)
	submit = SubmitField('get you some trinkets!')

#--------------------------------
# routes for web app
#--------------------------------
# home page
@app.route('/', methods=['get','post'])
@app.route('/index', methods=['get','post'])
def index():
	form = genRandTrinkForm()
	if form.validate_on_submit():
		print(form.validate_on_submit())
		ReturnedTrinkets = genRandTrinkList(form.radio.data)
		return render_template('index.html', form=form, ReturnedTrinkets=ReturnedTrinkets)
	else:
		print(form.validate_on_submit())
		ReturnedTrinkets = ['']
	return render_template('index.html', form=form, ReturnedTrinkets=ReturnedTrinkets)
	
''' #out of commission until i can figure out to write json to an html table
# https://pypi.org/project/json2html/ ???
# trinkets in a table
@app.route('/trinkets/table')
def trinkettable():
	return render_template('trinket_table.html',trinkets=trinkets.data,field=0)
'''

#--------------------------------
# Run the app
#--------------------------------
if __name__ == '__main__':
	app.run(
		port='5002'
		,debug=True
		#,host='0.0.0.0' #run on public ip other local devices can access (see in ipconfig) 
	)

#make a ruby sinatra equivalent when it's done!
# ctrl + shift + ] 