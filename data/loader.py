import xlrd
import os
from pprint import pprint

def get_hate_group_names():
	wkbook = xlrd.open_workbook('done/hate-groups.xlsx')
	names = []
	for sheet in wkbook.sheets():
		for row in sheet.get_rows():
			if row[3].value not in names:
				names.append(row[3].value)
	print names

def prepare_hate_groups():
    wkbook = xlrd.open_workbook('done/hate-groups.xlsx')
    hate_groups = {}
    for sheet in wkbook.sheets():
    	year = sheet.name
    	hate_groups[year] = {}
    	for row in sheet.get_rows():
    		state = row[2].value
    		if not hate_groups[year].get(state):
    			hate_groups[year][state] = {}

    		hate_type = row[3].value
    		if not hate_groups[year][state].get(hate_type):
    			hate_groups[year][state][hate_type] = 0

    		hate_groups[year][state][hate_type] = hate_groups[year][state][hate_type] + 1

    with open('{0}.csv'.format(year), 'a') as f:			
    	for year, state_data in hate_groups.iteritems():
    		for state, groups_dict in state_data.iteritems():
    			for group_name, count in hate_groups[year][state].iteritems():
    				f.write('{0},{1},{2},{3}\n'.format(group_name,count,state,year))

def prepare_education():
	sheet = xlrd.open_workbook('education-all.xlsx').sheet_by_index(0)
	education_levels = {'1990':{},'2000':{},'2010':{}}
	for row in sheet.get_rows():
		
		state = row[0].value
		education_levels['1990'][state] = {}
		education_levels['1990'][state]['population'] = row[1].value
		education_levels['1990'][state]['high_school'] = row[2].value
		education_levels['1990'][state]['bachelors'] = row[4].value

		education_levels['2000'][state] = {}
		education_levels['2000'][state]['population'] = row[6].value
		education_levels['2000'][state]['high_school'] = row[7].value
		education_levels['2000'][state]['bachelors'] = row[9].value

		education_levels['2010'][state] = {}
		education_levels['2010'][state]['high_school'] = row[11].value
		education_levels['2010'][state]['bachelors'] = row[12].value

	with open('education_attained.csv', 'a') as f:			
		for year,state_info in education_levels.iteritems():
			for state,level_info in state_info.iteritems():
				for level,percentage in level_info.iteritems():
					f.write('{0},{1},{2},{3}\n'.format(year, state, level, percentage))
    					# print year, state, level, percentage

def prepare_income():
	sheet = xlrd.open_workbook('income-view.xlsx').sheet_by_index(1)
	income_by_state = {}

	for row in sheet.get_rows():
		state = row[0].value
		if not income_by_state.get(state):
			income_by_state[state] = {
				'2015': row[1].value,
				'2014': row[3].value,
				'2013(39)': row[5].value,
				'2013(38)': row[7].value,
				'2012': row[9].value,
				'2011': row[11].value,
				'2010': row[13].value,
				'2009': row[15].value,
				'2008': row[17].value,
				'2007': row[19].value,
				'2006': row[21].value,
				'2005': row[23].value,
				'2004': row[25].value,
				'2003': row[27].value,
				'2002': row[29].value,
				'2001': row[31].value,
				'2000': row[33].value,
				'1999': row[35].value,
				'1998': row[37].value,
				'1997': row[39].value,
				'1996': row[41].value,
				'1995': row[43].value,
				'1994': row[45].value,
				'1993': row[47].value,
				'1992': row[49].value,
				'1991': row[51].value,
				'1990': row[53].value,
			}
	
	with open('state-income.csv', 'a') as f:
		for state,year_data in income_by_state.iteritems():
			for year,income in year_data.iteritems():
				f.write('{0},{1},{2}\n'.format(state, year, income))

def prepare_election_data():
	years = [1988,1992,1996,2000,2004,2008,2012,2016]
	for year in years:
		sheet = xlrd.open_workbook('elections/election-{0}.xlsx'.format(year)).sheet_by_index(0)
		if year == 1988:
			dem_index = 5
			rep_index = 2
			lib_index = 8

		if year == 1992:
			dem_index = 2
			rep_index = 5
			lib_index = 11

		if year == 1996:
			dem_index = 2
			rep_index = 5
			lib_index = 14

		if year == 2000:
			dem_index = 5
			rep_index = 2
			lib_index = 14

		if year == 2004:
			dem_index = 5
			rep_index = 2
			lib_index = 11

		if year == 2008:
			dem_index = 2
			rep_index = 5
			lib_index = 11

		if year == 2012:
			dem_index = 2
			rep_index = 5
			lib_index = 8

		if year == 2016:
			dem_index = 2
			rep_index = 5
			lib_index = 8

		voting_by_state = {}
		for row in sheet.get_rows():
			state = row[0].value
			for value in row:
				if value.value == '\u2013':
					value.value = None
			if not voting_by_state.get(state):
				voting_by_state[state] = {
					'available_electoral_votes' : row[1].value,
					'popular_votes_democrat' : row[dem_index].value,
					'electoral_votes_democrat' : row[dem_index + 2].value,
					'popular_votes_republican' : row[rep_index].value,
					'electoral_votes_republican' : row[rep_index + 2].value,
					'popular_votes_libertarian' : row[lib_index].value,
					'electoral_votes_libertarian' : row[lib_index + 2].value,
				}
			if year == 1988:
				voting_by_state[state]['popular_votes_new_alliance'] = row[11].value
				voting_by_state[state]['electoral_votes_new_alliance'] = row[13].value
			if year == 1992 or year == 1996 or year == 2004:
				voting_by_state[state]['popular_votes_reform'] = row[8].value
				voting_by_state[state]['electoral_votes_reform'] = row[10].value
			if year == 1996 or year == 2012 or year == 2016:
				voting_by_state[state]['popular_votes_green'] = row[11].value
				voting_by_state[state]['electoral_votes_green'] = row[13].value
			if year == 2000:
				voting_by_state[state]['popular_votes_green'] = row[8].value
				voting_by_state[state]['electoral_votes_green'] = row[10].value
				voting_by_state[state]['popular_votes_reform'] = row[11].value
				voting_by_state[state]['electoral_votes_reform'] = row[13].value
				voting_by_state[state]['popular_votes_constitution'] = row[17].value
				voting_by_state[state]['electoral_votes_constitution'] = row[19].value
				voting_by_state[state]['popular_votes_natural_law'] = row[20].value
				voting_by_state[state]['electoral_votes_natural_law'] = row[22].value
			if year == 2004 or year == 2008:
				voting_by_state[state]['popular_votes_constitution'] = row[14].value
				voting_by_state[state]['electoral_votes_constitution'] = row[16].value
				voting_by_state[state]['popular_votes_green'] = row[17].value
				voting_by_state[state]['electoral_votes_green'] = row[19].value
			if year == 2008:
				voting_by_state[state]['popular_votes_independent'] = row[8].value
				voting_by_state[state]['electoral_votes_independent'] = row[10].value

		with open('states-voting.csv', 'a') as f:
			for state, state_votes in voting_by_state.iteritems():
				for vote_type, votes in state_votes.iteritems():
					if isinstance(votes,float):
						f.write('{0},{1},{2},{3}\n'.format(year, state, vote_type, votes))
