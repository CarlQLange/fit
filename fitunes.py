#!/usr/local/bin/python3

#fuzzy itunes controller
#intended use:
# $ play "derezzed remix"
#if there is no track titled that, look around for a fuzzy match
#in this case it should play the track titled "Derezzed (Remixed By The Glitch Mob)"

import os, sys, plistlib, time
from _fit import gspeech, recognise

definitions = """
prevaction: {(previous song|previous|prev|last|go back|back|play the last song|play the previous song)},
nextaction: {(next song|next|skip|play the next song|play another song)},
artistaction: {(play songs by|play track by|play music by|play some songs by|i want to listen to)@d1},
playaction: {(play|i want to hear)@d1[by]@d2},
pauseaction: {(pause|stop|shut up for a second)},
currentaction: {(current|whats playing|what song is playing|what song is this|what track is this|whats the name of the current song)}
"""


def main():
	if sys.argv[1] == 'listen':
		action = recognise.parse(gspeech.hearandinterpret(), definitions)
	elif sys.argv[1] == 'serve':
		from _fit.web import server
		server.serve()
		return
	else:
		action = recognise.parse(sys.argv[1], definitions)
	print(action)

	try:
		if (action[0] == 'playaction'):
			st = time.time();

			if(len(action[1]) > 1):
				ar = bestmatch(action[1][1], artistnames)
				tr = bestmatch(action[1][0], tracksbyartist, arg=ar)
				playtrackbyartist(tr, ar)
				print("Playing {0} by {1}".format(tr,ar))
			else:
				tr = bestmatch(action[1][0], tracknames)
				print("Playing %s" % tr)
				playtrack(tr)
			print("Took {0} seconds.".format(round(time.time() - st, 3)))
		elif (action[0] == 'artistaction'):
			st = time.time();
			ar = bestmatch(action[1][0], artistnames)
			print("Playing %s" % ar)
			playartist(ar)
			print("Took {0} seconds.".format(round(time.time() - st, 3)))
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
	except TypeError:
		print("Couldn't understand the input!")

###iTunes Library handling section
lib = plistlib._InternalDict()

def initlib():
	global lib
	if (lib == {}):
		lib = plistlib.readPlist(os.environ['HOME']+"/Music/iTunes/iTunes Music Library.xml") #eww TODO move this somewhere better

def tracknames():
	initlib()
	for track in lib["Tracks"]:
		try:
			lib["Tracks"][track]["Has Video"]
		except KeyError:
			#success! also what am i doing with these exceptions
			yield lib["Tracks"][track]["Name"]

def artistnames():
	initlib()
	artists = set()
	for track in lib["Tracks"]:
		try:
			lib["Tracks"][track]["Has Video"]
		except KeyError:
			if lib["Tracks"][track]["Artist"] not in artists:
				artists.add(lib["Tracks"][track]["Artist"])
				yield lib["Tracks"][track]["Artist"]

def tracksbyartist(exactartistname):
	initlib()
	for track in lib["Tracks"]:
		try:
			lib["Tracks"][track]["Has Video"]
		except KeyError:
			if (lib["Tracks"][track]["Artist"] == exactartistname):
				yield(lib["Tracks"][track]["Name"])

def gettrackbyartist(exactartistname):
	initlib()
	for track in lib["Tracks"]:
		try:
			if (lib["Tracks"][track]["Artist"] == exactartistname):
				return(lib["Tracks"][track]["Name"])
				break
		except KeyError:
			continue

###Fuzzy text section
#TODO: I plan on making this a good bit better. Right now I'm going for fastest-possible solution and this works. Ish.
def bestmatch(inp, matchto, arg=""):
	print(inp)
	lowest = ("", 99999)
	if (arg != ""):
		for trackname in matchto(arg):
			if (recognise.levenshtein(inp, trackname) < lowest[1]):
				lowest = (trackname, recognise.levenshtein(inp, trackname))
	else:
		for trackname in matchto():
					if (recognise.levenshtein(inp, trackname) < lowest[1]):
						lowest = (trackname, recognise.levenshtein(inp, trackname))
	return lowest[0]

###iTunes controller section
def current():
	#print current track
	osascript("""
        tell application "iTunes"
            if not (exists current track) then return "No song playing."
            return (get name of current track) & " by " & (get artist of current track)
        end tell
    """)

def playtrack(exacttrackname):
	#play the track with the **EXACT** track name
	osascript("""
		tell application "iTunes"
			play track "{0}"
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
		end tell
	""".format(exactartistname, exacttrackname))

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

def osascript(str):
	#below is a beautiful solution for this problem thanks to Teddy
	#https://gist.github.com/1532172#gistcomment-71911
	os.system("osascript - <<EOF" + str + "")

main()