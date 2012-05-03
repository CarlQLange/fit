#!/usr/local/bin/python3

#fuzzy itunes controller
#intended use:
# $ fit "play derezzed remix"
#if there is no track titled that, look around for a fuzzy match
#in this case it should play the track titled "Derezzed (Remixed By The Glitch Mob)"

import os, sys, plistlib, time
from _fit import gspeech, recognise, plugins

enabledplugins = ["iTunes"]

def main():
	'''
	if sys.argv[1] == 'listen':
		action = recognise.parse(gspeech.hearandinterpret(), definitions)
	elif sys.argv[1] == 'serve':
		from _fit.web import server
		server.serve()
		return
	else:
	'''
		#there's an issue here somewhere with single-quotes
		#eg:
		#  $ fit "play we don't eat by adventure club"
		# Playing Teach Me How To Jerk by Adventure Club
		#  $ fit "play we dont eat by adventure club"
		# Playing We Don't Eat by Adventure Club

	for i in plugins.__all__:
		__import__("_fit.plugins." + i + ".actions")
		#sys.modules["_fit.plugins."+i+".actions"].current()
		desc = sys.modules["_fit.plugins."+i].__descriptions__
		#FIXME: This won't work with multiple plugins
		act = ""
		scr = 99999999
		args = []
		for k in desc.keys():
			t = recognise.parse(sys.argv[1], desc[k])
			if t[1] < scr:
				act = k
				scr = t[1]
				args = t[2]


		(getattr(sys.modules["_fit.plugins."+i+".actions"], act))(*args)

main()
