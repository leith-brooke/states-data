import queries

def get_valid_years():

	return queries.get_distinct_years()

def get_usa_data_for_year(year):
	data = {}
	for state in queries.get_states():
		data[state] = get_state_data_for_year(state, year)
	return data

def get_state_data_for_year(state,year):
	education = queries.get_education_levels_for_state_year(state,year)

	income = queries.get_avg_income_by_state_in_year(state,year)
	if len(income) > 0:
		income = income[0] 

	election_results = queries.get_full_election_results_by_state_in_year(state,year)
	if election_results:
		for k, v in election_results.iteritems():
			if isinstance(v, tuple):
				if v[1] == None:
					v = v[0]

	hate_groups = queries.get_hate_group_data_by_state_in_year(state,year)
	

	data = {}
	if education:
		data['education'] = education
	if income:
		data['income'] = income
	if election_results:
		data['election_results'] = election_results
	if hate_groups:
		data['hate_groups'] = hate_groups
	data['state'] = state
	return data

def get_state_election_color(state,year):
	red = '#E91D0E'
	blue = '#290EE9'
	winning_party = queries.get_winning_party(state,year)
	if winning_party == 'Democratic':
		return blue
	if winning_party == 'Republican':
		return red
	return '#FFF'

def get_election_colors(year):
	if not year % 4 == 0:
		return {}
	else:
		return { state: get_state_election_color(state,year) for state in queries.get_states() }

def get_state_income_color(state,year,avg):
	red = '#E91D0E'
	black = '#000'
	if queries.get_state_income(state,year) < avg:
		return red
	else:
		return black

def get_income_colors(year):
	national_avg = queries.get_usa_avg_income(year)
	data = { state: get_state_income_color(state,year,national_avg) for state in queries.get_states() }	
	data['avg'] = round(national_avg,2)
	return data

def get_state_hate_color(state,year,avg):
	hate_groups_in_state = queries.get_total_hate_groups_in_state_year(state, year)
	national_avg = queries.get_hate_group_average(year)
	if hate_groups_in_state < national_avg:
		return '#E6E6FA'
	else:
		return '#B22222'

def get_hate_colors(year):
	if year >= 2000 and year < 2016:
		national_avg = queries.get_hate_group_average(year)
		data = { state: get_state_hate_color(state,year,national_avg) for state in queries.get_states() }
		data['avg'] = round(national_avg,2)
		return data
	else:
		return None

def get_education_colors(level,year):

	national_avg = queries.get_us_avg_education(level,year)
	colors = {}
	for state in queries.get_states():
		state_avg = queries.get_state_avg_education(level,state,year)
		if state_avg > national_avg:
			colors[state] = '#008000'
		else:
			colors[state] = '#DC143C'
	colors['avg'] = round(national_avg,2)
	return colors

def get_colors(criteria, year):
	print criteria, year
	if criteria == 'election':
		return get_election_colors(int(year))
	elif criteria == 'income':
		return get_income_colors(int(year))
	elif criteria == 'hate':
		return get_hate_colors(int(year))
	elif criteria == 'bachelors':
		return get_education_colors("Bachelor's",int(year))
	elif criteria == 'hs':
		return get_education_colors("High School",int(year))
