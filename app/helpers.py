from pprint import pprint
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

'''
	post_dict = {
		'income': {
			'income_operator': [=,<,>],
			'amount' = int
		},
		'education': {
			'level': [High School, Bachelor's]
			'percentage': int
			'education_operator': [=,<,>],
		},
		'election': {
			'vote_type': [electoral,popular]
			'vote_quantity': int
			'vote_operator': [<,>,=]
			'party': [Republican,Democratic,Green...]
		},
		'hate': {
			hate_operator: [<,>,=]
			hate_quantity: int
		}
	}
'''

def add_inner_join(from_statement, last_table, next_table):
	last_table_name = last_table.split(' ')[0]
	last_table_abbreviation = last_table.split(' ')[1]
	
	next_table_name = next_table.split(' ')[0]
	next_table_abbreviation = next_table.split(' ')[1]
	join_statement = ' inner join {0}'.format(next_table)

	if last_table_abbreviation == 's':
		if next_table_abbreviation == 'a':
			from_statement += ' inner join {0} on {1}.state={2}.name'.format(next_table, next_table_abbreviation, last_table_abbreviation)
		else:
			from_statement += ' inner join {0} on {1}.state={2}.name and {1}.year={2}.year'.format(next_table, next_table_abbreviation, last_table_abbreviation)
	else:
		if next_table_abbreviation == 'a':
			from_statement += ' inner join {0} on {1}.state={2}.state'.format(next_table, next_table_abbreviation, last_table_abbreviation)
		else:
			from_statement += ' inner join {0} on {1}.state={2}.state and {1}.year={2}.year'.format(next_table, next_table_abbreviation, last_table_abbreviation)
		
	return from_statement

def get_states_from_dict(post_dict,year):
	post_dict = sanitize_post(post_dict,year)
	#'select {0}.state from'

	conditions = []
	last_table = None
	select_statement = None
	primary_table = None

	'''
		post_dict['income'] = {
			income_operator: [=,<,>]
			amount = int
		}
	'''
	if post_dict.get('income'):
		#'state s'
		primary_table = 's'
		select_statement = 'select distinct s.name'
		last_table = 'State s'
		from_statement = 'from State s'

		income_criteria = post_dict.get('income')		
		income_operator = income_criteria.get('income_operator') or '='
		amount = income_criteria.get('amount') or queries.get_usa_avg_income(year)
		
		income_condition = 's.avg_income {0} {1}'.format(income_operator, amount)
		conditions.append(income_condition)
		
	'''
		post_dict['election'] = {
			vote_type: [electoral,popular]
			vote_quantity: int
			vote_operator: [<,>,=]
			party = [Republican,Democratic,Green...]
		}
	'''
	if post_dict.get('election'):
		#'CastedVotesFor c'
		if not select_statement:
			primary_table = 'c'
			select_statement = 'select distinct c.state'
			from_statement = 'from CastedVotesFor c'
		else:
			from_statement = add_inner_join(from_statement, last_table, 'CastedVotesFor c')
		last_table = 'CastedVotesFor c'

		election_conditions = []
		election_criteria = post_dict.get('election')
		#where c.vote_type = 'electoral' and c.quantity > 0 and c.party = 'Republican'
		vote_type = election_criteria.get('vote_type')
		if vote_type:
			election_conditions.append('c.vote_type = \"{0}\"'.format(vote_type))
		vote_quantity = election_criteria.get('vote_quantity')
		vote_operator = election_criteria.get('vote_operator') or '='
		if vote_quantity:
			election_conditions.append('c.quantity {0} {1}'.format(vote_operator, vote_quantity))
		party = election_criteria.get('party')
		if party:
			election_conditions.append('c.party = \"{0}\"'.format(party))

		conditions.append(' and '.join(election_conditions))
	
	'''
		post_dict['hate'] = {
			hate_operator: [<,>,=]
			hate_quantity: int
		}
	'''
	if post_dict.get('hate'):
		#'ExistedIn e'
		if not select_statement:
			primary_table = 'e'
			select_statement = 'select distinct e.state'
			from_statement = 'from ExistedIn e'
		else:
			from_statement = add_inner_join(from_statement, last_table, 'ExistedIn e')
		last_table = 'ExistedIn e'

		hate_criteria = post_dict.get('hate')
		hate_operator = hate_criteria.get('hate_operator')
		hate_quantity = hate_criteria.get('hate_quantity') or queries.get_hate_group_average(year)

		'''
			select 
				view.state 
			from 
				(select e1.state, sum(e1.chapters) vchapters from ExistedIn e1 where e1.year = <YEAR> group by e1.state) view 
			where
				view.vchapters <OPERATOR> <QUANTITY> 
		'''
		if primary_table == 's':
			hate_condition = '{0}.name in (select view.vstate from (select e.state vstate, sum(chapters) vchapters from ExistedIn e where year = {1} group by e.state) view where view.vchapters {2} {3})'.format(primary_table, year, hate_operator, hate_quantity)	
		else:
			hate_condition = '{0}.state in (select view.vstate from (select e.state vstate, sum(chapters) vchapters from ExistedIn e where year = {1} group by e.state) view where view.vchapters {2} {3})'.format(primary_table, year, hate_operator, hate_quantity)
		conditions.append(hate_condition)

	'''
		post_dict['education'] = {
			level: [High School, Bachelor's]
			percentage: int
			education_operator = [<,=,>]
		}
	'''
	if post_dict.get('education'):
		if not select_statement:
			select_statement = 'select distinct a.state'
			from_statement = 'from Attained a'
			primary_table = 'a'
		else:
			from_statement = add_inner_join(from_statement, last_table, 'Attained a')
		e_condition = None
		if last_table == 'ExistedIn e':
			e_condition = conditions[-1]
			conditions.remove(e_condition)

		last_table = 'a'

		education_criteria = post_dict.get('education')
		level = education_criteria.get('level')
		education_operator = education_criteria.get('education_operator') or '='
		percentage = education_criteria.get('percentage') or queries.get_us_avg_education(level, year)
		conditions.append('a.education_level = \"{0}\" and a.year = {1} and a.percentage {2} {3}'.format(level, queries.round_year_to_decade(year), education_operator,percentage))
		if e_condition:
			conditions.append(e_condition)

	print last_table, primary_table
	if not (last_table == primary_table and last_table == 'a'):
		conditions.append('{0}.year = {1}'.format(primary_table,year))

	where = ' and '.join(conditions)
	query = '{0} {1} where {2}'.format(select_statement,from_statement,where)
	
	print query
	results = queries.execute_query(query)
	pprint(results)
	return {state: '#ff0' for state in results}

def sanitize_post(post_dict,year):
	clean_data = {}

	if year:
		clean_data['year'] = year
	hate_operator = post_dict.get('hate_operator')
	hate_quantity = post_dict.get('hate_quantity')
	if hate_operator or hate_quantity:
		clean_data['hate'] = {
			'hate_operator': hate_operator,
			'hate_quantity': hate_quantity
		}

	party = post_dict.get('party')
	vote_operator = post_dict.get('vote_operator')
	vote_quantity = post_dict.get('vote_quantity')
	vote_type = post_dict.get('vote_type')
	if party or vote_operator or vote_quantity or vote_type:
		if vote_quantity:
			vote_quantity = int(vote_quantity)
		clean_data['election'] = {
			'party': party,
			'vote_operator': vote_operator,
			'vote_quantity': vote_quantity,
			'vote_type': vote_type
		}

	education_operator = post_dict.get('education_operator')
	level = post_dict.get('level')
	percentage = post_dict.get('percentage')
	if level or percentage or education_operator:
		clean_data['education'] = {
			'level': level,
			'percentage': float(percentage),
			'education_operator': education_operator
		}

	income_operator = post_dict.get('income_operator')
	amount = post_dict.get('amount')
	if amount or income_operator:
		clean_data['income'] = {}
		if amount:
			clean_data['income']['amount'] = int(amount)
		if income_operator:
			clean_data['income']['income_operator'] = income_operator
			
	pprint(clean_data)
	return clean_data

