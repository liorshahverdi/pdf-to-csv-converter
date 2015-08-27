from subprocess import call
from sys import argv
import pandas as pd 

def transform(filename):
	call(["pdftotext", "-layout", filename])
	return filename.split(".")[0]+".txt"

def segment(contents):
	relevant = []
	start = False
	for line in contents:
		if "Vice" in line:
			start = True
		if "Published" in line:
			start = False
		if start:
			relevant.append(line)
	return relevant

def parse(relevant):
	tmp = {}
	tmp1 = {}
	df = pd.DataFrame()
	for line in relevant:
		split_up = line.split(" ")
		split_up = [elem for elem in split_up if elem != '']
		if len(split_up) == 5:
			tmp['last_name'] = split_up[0]
			tmp['first_name'] = split_up[1]
			tmp['party-state'] = split_up[2]
			tmp['suite'] = split_up[3]
			tmp['phone'] = split_up[4]
			df = df.append(tmp, ignore_index=True)
		elif len(split_up) == 10:
			tmp['last_name'] = split_up[0]
			tmp['first_name'] = split_up[1]
			tmp['party-state'] = split_up[2]
			tmp['suite'] = split_up[3]
			tmp['phone'] = split_up[4]
			tmp1['last_name'] = split_up[5]
			tmp1['first_name'] = split_up[6]
			tmp1['party-state'] = split_up[7]
			tmp1['suite'] = split_up[8]
			tmp1['phone'] = split_up[9]
			df = df.append(tmp, ignore_index=True)
			df = df.append(tmp1, ignore_index=True)
	return df

if __name__ == '__main__':
	txt_file = transform(argv[1])
	text = open(txt_file, "r").read().decode("ascii", "ignore")
	contents = text.split('\n')
	relevant = segment(contents)
	df = parse(relevant)
	df.to_csv("results.csv")
	print 'csv file success'