#!/usr/local/bin/python3

import os, sys, plistlib, time
from _fit import gspeech, recognise, plugins

enabledplugins = ["Mail"]

def main():
	if len(sys.argv) == 1:
		print("I need to be told something to do.")
		print("For example, try")
		print("  fit \"what song is playing?\"")
		return
	if sys.argv[1] == 'listen':
		action = recognise.parse(gspeech.hearandinterpret(), definitions)
	elif sys.argv[1] == 'serve':
		from _fit.web import server
		server.serve()
		return

	for i in plugins.__all__:
		if i not in enabledplugins:
			continue
		__import__("_fit.plugins." + i + ".actions")
		
		desc = sys.modules["_fit.plugins."+i].__descriptions__
		#FIXME: This might not work well with multiple plugins
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
