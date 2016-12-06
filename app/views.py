from flask import render_template, jsonify, request, redirect
from app import app
from helpers import get_state_data_for_year, get_usa_data_for_year, get_valid_years, get_colors, get_states_from_dict

@app.route('/')
@app.route('/index')
def index():
	years = get_valid_years()
	years.remove(2016)
	print years
	return render_template('index.html',years=get_valid_years())

@app.route('/query/<year>', methods=['POST', 'GET'])
def get_states_fulfilling_query(year):
	print request.method
	
	data = get_states_from_dict(request.form, year)
	return jsonify(**data)

@app.route('/year/<year>/state/<state>')
def get_state_by_year(state,year):
	data = get_state_data_for_year(state,int(year))
	return jsonify(**data)

@app.route('/year/<year>')
def get_usa_by_year(year):
	data = get_usa_data_for_year(int(year))
	return jsonify(**data)

@app.route('/colors/<criteria>/<year>')
def get_map_colors(criteria,year):
	data = get_colors(criteria,year)
	return jsonify(**data)
