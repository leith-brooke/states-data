from flask import render_template, jsonify
from app import app
from helpers import get_state_data_for_year, get_usa_data_for_year
# from helpers import STATES

@app.route('/')
@app.route('/index')
def index():	
	return render_template('index.html',data=get_usa_by_year(2016))

@app.route('/year/<year>/state/<state>')
def get_state_by_year(state,year):
	data = get_state_data_for_year(state,int(year))
	return jsonify(**data)

@app.route('/year/<year>')
def get_usa_by_year(year):
	data = get_usa_data_for_year(int(year))
	return jsonify(**data)