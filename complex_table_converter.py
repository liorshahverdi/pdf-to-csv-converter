from subprocess import call
from sys import argv
import pandas as pd 

#table on page 3 of 20 in world_population.pdf

def transform(filename):
	call(["pdftotext", "-layout", filename])
	return filename.split(".")[0]+".txt"

def segment(contents):
	relevant = []
	start = False
	for line in contents:
		if "7,238,184,000" in line:
			start = True
		if "2014 Population Reference Bureau" in line:
			start = False
		if start:
			relevant.append(line)
	return relevant

def parse(relevant):
	table = {}
	table['population'] = {}
	table['births'] = {}
	table['births']['year'] = {}
	to_births_year = False
	table['births']['day'] = {}
	to_births_day = False
	table['births']['minute'] = {}
	to_births_minute = False
	table['deaths'] = {}
	table['deaths']['year'] = {}
	to_deaths_year = False
	table['deaths']['day'] = {}
	to_deaths_day = False
	table['deaths']['minute'] = {}
	to_deaths_minute = False
	table['natural'] = {}
	table['natural']['year'] = {}
	to_natural_year = False
	table['natural']['day'] = {}
	to_natural_day = False
	table['natural']['minute'] = {}
	to_natural_minute = False
	df = pd.DataFrame()
	for line in relevant:
		split_up = line.split(" ")
		#print split_up
		split_up = [elem for elem in split_up if elem != '']
		if 'Population' in split_up:
			table['population']['world'] = split_up[1]
			table['population']['mdc'] = split_up[2]
			table['population']['ldc'] = split_up[3]
			to_births_year = True
			continue
		if to_births_year:
			to_births_year = False
			table['births']['year']['world'] = split_up[1]
			table['births']['year']['mdc'] = split_up[2]
			table['births']['year']['ldc'] = split_up[3]
			to_births_day = True
			continue
		if to_births_day:
			to_births_day = False
			table['births']['day']['world'] = split_up[3]
			table['births']['day']['mdc'] = split_up[4]
			table['births']['day']['ldc'] = split_up[5]
			to_births_minute = True
			continue
		if to_births_minute:
			to_births_minute = False
			table['births']['minute']['world'] = split_up[1]
			table['births']['minute']['mdc'] = split_up[2]
			table['births']['minute']['ldc'] = split_up[3]
			to_deaths_year = True
			continue
		if to_deaths_year:
			to_deaths_year = False
			table['deaths']['year']['world'] = split_up[1]
			table['deaths']['year']['mdc'] = split_up[2]
			table['deaths']['year']['ldc'] = split_up[3]
			to_deaths_day = True
			continue
		if to_deaths_day:
			to_deaths_day = False
			table['deaths']['day']['world'] = split_up[3]
			table['deaths']['day']['mdc'] = split_up[4]
			table['deaths']['day']['ldc'] = split_up[5]
			to_deaths_minute = True
			continue
		if to_deaths_minute:
			to_deaths_minute = False
			table['deaths']['minute']['world'] = split_up[1]
			table['deaths']['minute']['mdc'] = split_up[2]
			table['deaths']['minute']['ldc'] = split_up[3]
			to_natural_year = True
			continue
		if to_natural_year:
			to_natural_year = False
			table['natural']['year']['world'] = split_up[1]
			table['natural']['year']['mdc'] = split_up[2]
			table['natural']['year']['ldc'] = split_up[3]
			to_natural_day = True
			continue
		if to_natural_day:
			to_natural_day = False
			table['natural']['day']['world'] = split_up[3]
			table['natural']['day']['mdc'] = split_up[4]
			table['natural']['day']['ldc'] = split_up[5]
			to_natural_minute = True
			continue
		if to_natural_minute:
			to_natural_minute = False
			table['natural']['minute']['world'] = split_up[1]
			table['natural']['minute']['mdc'] = split_up[2]
			table['natural']['minute']['ldc'] = split_up[3]
			continue
	df = df.append(table, ignore_index = True)
	#print table
	return df

if __name__ == '__main__':
	txt_file = transform(argv[1])
	text = open(txt_file, "r").read().decode("ascii", "ignore")
	contents = text.split('\n')
	relevant = segment(contents)
	df = parse(relevant)
	df.to_csv("world_population.csv")
	print 'csv file success'