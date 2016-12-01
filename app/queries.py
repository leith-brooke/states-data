from app import db_engine
db = db_engine.connect()

'''
ExistedIn(
	hate_group varchar(32) references HateGroup(name),
	chapters int,
	state varchar(2) references State(name), 
	year int
);
'''
def get_total_hate_groups_in_state_year(state,year):
	return [
		result[0] for result in db.execute(
				'select sum(chapters) from ExistedIn where state = \"{0}\" and year = {1}'.format(state,year)
				).fetchall()
		]

def get_hate_group_data_by_state_in_year(state,year):
	state_data = {}
	for hate_group in get_hate_groups():
		chapters = get_hate_group_occurences_by_state_in_year(hate_group, state, year)
		if isinstance(chapters, list) and len(chapters) == 1:
			chapters = chapters[0]
		if len(chapters) == 1:
			chapters = chapters[0]
		if chapters and isinstance(chapters,int):
			state_data[hate_group] = chapters
	return state_data

def get_hate_group_occurences_by_state_in_year(hate_group,state,year):
	return db.execute(
		'select chapters from ExistedIn where hate_group = \"{0}\" and state = \"{1}\" and year = {2}'.format(hate_group,state,year)
		).fetchall()



def get_hate_group_average(year):
	total = 0
	for state in states:
		total += get_total_hate_groups_in_state_year(state, year)
	return total/len(states)

'''
Attained(
	state varchar(2) references State(name),
	education_level varchar(12) references Education(level), 
	percentage float, 
	year int
);
'''
def get_education_levels_for_state_year(state,year):
	if year % 10 >=5:
		year += 10 - year % 10
	elif year % 10 < 5:
		year -= year % 10
	if year > 2010:
		year = 2010
	elif year < 1990:
		return None

	data = {}
	for level in get_education_levels():
		query_result = db.execute('select percentage from Attained where state = \"{0}\" and year = {1} and education_level = \"{2}\"'.format(state,year,level)).fetchall()
		if isinstance(query_result, list) and len(query_result) == 1:
			query_data = query_result[0]
			if isinstance(query_data, list):
				data[level] = query_data[0]

	return data

'''
CastedVotesFor(
	year int,
	state varchar(2) references State(name),
	vote_type varchar(9) references Vote(type),
	party varchar(13) references PoliticalParty(name),
	quantity int
);
'''
def get_votes_of_type_for_party_by_state_in_year(vote_type,party,state,year):
	return [
		result[0] for result in db.execute(
			'select quantity from CastedVotesFor where vote_type = \"{0}\" and party = \"{1}\" and state = \"{2}\" and year = {3}'.format(
				vote_type,
				party,
				state,
				year
				)
			).fetchall()
	]

def get_full_election_results_by_state_in_year(state,year):
	if not year % 4 == 0:
		return None
	election_data = {}
	for party in get_political_parties_in_election_year(year):
		election_data[party] = {}
		for vote_type in get_vote_types():
			vote_count = get_votes_of_type_for_party_by_state_in_year(vote_type,party,state,year)
			if vote_count:
				election_data[party][vote_type] = vote_count
	return election_data

'''
State(
	name varchar(2),
	year int,
	avg_income float
);
'''
def get_states():
	return [
		result[0] for result in db.execute(
			'select distinct name from State'
		).fetchall()
	]		

def get_avg_income_by_state_in_year(state,year):
	return [
		result[0] for result in db.execute(
			'select avg_income from State where name = \"{0}\" and year = {1}'.format(state,year)
			).fetchall()
	]

'''
HateGroup(

	type varchar(32)
);
'''
def get_hate_groups():
	return [
		result[0] for result in db.execute(
			'select distinct type from HateGroup'
		).fetchall()
	]	

'''
Education(

	level varchar(12)
);
'''
def get_education_levels():
	return [
		result[0] for result in db.execute(
			'select distinct level from Education'
		).fetchall()
	]

'''
PoliticalParty(

	name varchar(13)
);
'''
def get_political_parties_in_election_year(year):
	return [
		result[0] for result in db.execute(
			'select name from PoliticalParty where name in (select distinct party from CastedVotesFor where year = {0})'.format(year)
		).fetchall()
	]

'''
Vote(

	type varchar(9)
);
'''
def get_vote_types():
	return [
		result[0] for result in db.execute(
			'select distinct type from Vote'
		).fetchall()	
	]

