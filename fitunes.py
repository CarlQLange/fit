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
		for k in desc.keys():
			t = recognise.parse(sys.argv[1], desc[k])
			if t[1] < scr:
				act = k
				scr = t[1]

		(getattr(sys.modules["_fit.plugins."+i+".actions"], act))()

	"""
	try:
		if (action[0] == 'playaction'):
			#st = time.time();

			if(len(action[1]) > 1):
				ar = bestmatch(action[1][1], artistnames)
				tr = bestmatch(action[1][0], tracksbyartist, arg=ar)
				playtrackbyartist(tr, ar)
				print("Playing {0} by {1}".format(tr, ar))
			else:
				tr = bestmatch(action[1][0], tracknames)
				print("Playing {0}".format(tr))
				playtrack(tr)
			#print("Took {0} seconds.".format(round(time.time() - st, 3)))
		elif (action[0] == 'artistaction'):
			#st = time.time();
			ar = bestmatch(action[1][0], artistnames)
			print("Playing %s" % ar)
			playartist(ar)
			#print("Took {0} seconds.".format(round(time.time() - st, 3)))
		elif (action[0] == 'pauseaction'):
			print("Paused")
			pause()
		elif (action[0] == 'prevaction'):
			print("Previous song")
			prev()
		elif (action[0] == 'nextaction'):
			print("Next song")
			next()
		elif (action[0] == 'currentaction'):
			current()
		elif (action[0] == 'listaction'):
			listsongsbyartist(action[1][0])
		elif (action[0] == 'repeataction'):
			repeat()
		elif (action[0] == 'stoprepeataction'):
			stoprepeat()
	except TypeError:
		print("Couldn't understand the input! (TypeError)")
	"""

###Fuzzy text section
#TODO: I plan on making this a good bit better. Right now I'm going for fastest-possible solution and this works. Ish.
#need to move this elsewhere
def bestmatch(inp, matchto, arg=""):
	#print(inp)
	lowest = ("", 99999)
	if (arg != ""):
		for trackname in matchto(arg):
			if (recognise.match(inp, trackname) < lowest[1]):
				lowest = (trackname, recognise.match(inp, trackname))
				#print(lowest)
	else:
		for trackname in matchto():
			if (recognise.match(inp, trackname) < lowest[1]):
				lowest = (trackname, recognise.match(inp, trackname))
	return lowest[0]

'''
###iTunes controller section
def current():
	#print current track
	osascript("""
		on isrunning()
			tell application "System Events" to (name of processes) contains "iTunes"
		end isrunning

		if isrunning()
			tell application "iTunes"
				if not (exists current track) then return "No song playing."
				return (get name of current track) & " by " & (get artist of current track)
			end tell
		else
			return "No song playing."
		end if
	""")

def currentartist():
	osascript("""
		tell application "iTunes"
			return (get artist of current track)
		end tell
	""")

def playtrack(exacttrackname):
	#play the track with the **EXACT** track name
	osascript("""
		tell application "iTunes"
			play track "{0}"
			set song repeat of current playlist to off
		end tell
	""".format(exacttrackname))

def playartist(exactartistname):
	playtrack(gettrackbyartist(exactartistname))

def playtrackbyartist(exacttrackname, exactartistname):
	osascript("""
		tell application "iTunes"
			set mySongs to every track of library playlist 1 whose artist is "{0}" and name is "{1}"
			repeat with song in mySongs
				play song
			end repeat
			set song repeat of current playlist to off
		end tell
	""".format(exactartistname, exacttrackname))

def listsongsbyartist(exactartistname):
	osascript("""
		tell application "iTunes"
			set mySongs to every track of library playlist 1 whose artist is "Draper" -- and name is "{1}"
			repeat with song in mySongs
				log(get name of song)
			end repeat
		end tell
	""")

def pause():
	#pause or unpause the current track
	osascript("""
		tell application "iTunes"
			playpause
		end tell
	""")

def next():
	#play the next track
	osascript("""
		tell application "iTunes"
			next track
		end tell
	""")

def prev():
	#play the previous track
	osascript("""
		tell application "iTunes"
			previous track
		end tell
	""")

def repeat():
	osascript("""
		tell application "iTunes"
			set song repeat of current playlist to one
		end tell
	""")

def stoprepeat():
	osascript("""
		tell application "iTunes"
			set song repeat of current playlist to off
		end tell
	""")

def osascript(str):
	#below is a beautiful solution for this problem thanks to Teddy
	#https://gist.github.com/1532172#gistcomment-71911
	os.system("osascript - <<EOF" + str + "")
'''

main()
