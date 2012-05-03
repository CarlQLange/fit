#recognise.py

import re

def parse(inp, definitions):
	#inp is a str, definitions is an list of str
	score = 99999999
	best = ""
	args = []
	for defn in definitions:
		if ('$' in defn):
			#we need to deal with arguments now
			s = re.sub(r"\\\$(\w+)", r"(.*)", re.escape(defn))
			try:
				args = re.findall(s, inp)[0]
			except IndexError:
				pass

			#now match the rest of the desc (aside from the args)
			inpwithoutargs = inp
			defnwithoutargs = defn
			for a in args:
				inpwithoutargs = inpwithoutargs.replace(' ' + a, '')
				defnwithoutargs = defnwithoutargs.replace(' ' + a, '')

			cs = match(inpwithoutargs, defnwithoutargs)
			if cs-1 < score: #FIXME hack crap here
				score = cs-1
				best = defn

		else:
			cs = match(inp, defn)
			if cs < score:
				score = cs
				best = defn

	return [best,score, args]

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
	for gr in _grams(s1, n=3):
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
