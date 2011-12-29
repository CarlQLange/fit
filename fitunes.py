#!/usr/local/bin/python3

#fuzzy itunes controller
#intended use:
# $ play "derezzed remix"
#if there is no track titled that, look around for a fuzzy match
#in this case it should play the track titled "Derezzed (Remixed By The Glitch Mob)"

import os, sys, plistlib, time

def main():
	handleinput()
	#for artist in artistnames():
	#	print(artist)
	

###Input handling section
def handleinput():
	#cache the args
	try:
		cmd = sys.argv[1]
	except IndexError:
		print("Usage: fit [track|current|pause|next|last|prev|play \"song title\"]")
		return

	try:
		inp = sys.argv[2]
	except IndexError:
		inp = ""

	if (((cmd == "track") or (cmd == "current")) and (inp == "")):
		current()
	elif (cmd == "pause"):
		pause()
	elif (cmd == "next"):
		next()
	elif ((cmd == "last") or (cmd == "prev")):
		prev()
	elif (cmd == "artist"):
		st = time.time();
		ar = bestmatch(inp, artistnames)
		print("Playing %s" % ar)
		playartist(ar)
		print("Took %s seconds." % (time.time() - st))
	elif (cmd == "play"):
		st = time.time();
		tr = bestmatch(inp, tracknames)
		print("Playing %s" % tr)
		playtrack(tr)
		print("Took %s seconds." % (time.time() - st))
		#current()

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
			#success!
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
def bestmatch(inp, matchto):
	lowest = ("", 99999)
	for trackname in matchto():
		if (levenshtein(inp, trackname) < lowest[1]):
			lowest = (trackname, levenshtein(inp, trackname))

	return lowest[0]

#stolen from http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
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
			play track "%s"
		end tell
	""" % exacttrackname)

def playartist(exactartistname):
	playtrack(gettrackbyartist(exactartistname))

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