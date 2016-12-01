import queries

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
	return data