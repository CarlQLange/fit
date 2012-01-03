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
#			threshold = 5
			
#			if (levenshtein(actionw, inp) < threshold):
			if (re.match(actionw, inp, flags=re.I)):
				data = []
				datas = inp
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

#stolen from http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
#need to make this independent of string length!!
def levenshtein(s1, s2):
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
    