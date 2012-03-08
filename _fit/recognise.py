#recognise.py

#and today's award for worst use of regex goes to...

import re

def parse(inp, definitions):
	getactions = re.compile(r'([^\n].*[^,])')
	getactionname = re.compile(r'(^[^:]+)')
	getactionwordsr = re.compile(r'\(([^}]+)\)')
	splitmultipler = re.compile(r'([^|]+)')
	#getdatadefr = re.compile(r'@(\w*)')
	getseperatorsr = re.compile(r'\[([^}]+)\]')

	actions = getactions.findall(definitions)

	for action in actions:
		actionwordsstr = getactionwordsr.findall(action)[0]
		actionwords = splitmultipler.findall(actionwordsstr)
		#print(actionwords)
		if getseperatorsr.search(action):
			seperatorsstr = getseperatorsr.findall(action)[0]
			seperators = splitmultipler.findall(seperatorsstr)
			
		for actionw in actionwords:
			threshold = 5

			if (levenshtein(actionw, inp[0:8]) < threshold):
			#if (re.match(actionw, inp, flags=re.I)):
				data = []
				datas = inp.replace(actionw, "")
				#print(datas)
				if getseperatorsr.search(action):
					for seperator in seperators:
						data = datas.split(seperator)
				else:
					data.append(datas)
				#print(data)
				return(getactionname.findall(action)[0], data)
				#threshold+=1
		"""
		for actionw in actionwords:
			lowestaction = ("", 9999)
			if match(inp, actionw) < lowestaction[1]:
				lowestaction = (actionw, match(inp, actionw))
	print(lowestaction)
	"""



#stolen from http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
def levenshtein(s1, s2, normalise=False):
	if len(s1) < len(s2):
		return levenshtein(s2, s1)
	if not s1:
		return len(s2)

	previous_row = range(len(s2) + 1)
	for i, c1 in enumerate(s1):
		current_row = [i + 1]
		for j, c2 in enumerate(s2):
			insertions = previous_row[j + 1] + 1
			deletions = current_row[j] + 1
			substitutions = previous_row[j] + (c1 != c2)
			current_row.append(min(insertions, deletions, substitutions))
		previous_row = current_row

	return previous_row[-1]
	

def match(s1, s2):
	score = 0
	for gr in _grams(s1):
		if _makeStr(gr) in s2.lower():
			score -= 1
	return score

#ugly, messy, shit, but it works?
def _grams(s, n=3):
	tr = [[]]
	i = 1
	j = 0
	for ch in s:
		if ch != ' ':
			if i % n == 0 and i != 0 and i != len(s)-1:
				tr.append([])
				tr[j].append(ch)
				j += 1
			else:
				tr[j].append(ch)
			i += 1

	return tr

def _makeStr(ls):
	ret = ""
	for c in ls:
		ret += c
	return ret