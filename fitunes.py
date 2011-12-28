#!/usr/local/bin/python3

#fuzzy itunes controller
#intended use:
# $ play "derezzed remix"
#if there is no track titled that, look around for a fuzzy match
#in this case it should play the track titled "Derezzed (Remixed By The Glitch Mob)"

import os, sys, plistlib, time

def main():
	handleinput()


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
	elif (cmd == "play"):
		st = time.time();
		tr = bestmatch(inp)
		print("Playing %s" % tr)
		playtrack(tr)
		print("Took %s seconds." % (time.time() - st))
		#current()

###iTunes Library handling section
#it's a plist so let's make it a dict
def tracknames():
	lib = plistlib.readPlist(os.environ['HOME']+"/Music/iTunes/iTunes Music Library.xml") #eww TODO move this somewhere better
	for track in lib["Tracks"]:
		yield lib["Tracks"][track]["Name"]

###Fuzzy text section
#TODO: I plan on making this a good bit better. Right now I'm going for fastest-possible solution and this works. Ish.
def bestmatch(inp):
	lowest = ("", 99999)
	for trackname in tracknames():
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
            if not (exists current track) then return ""
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
	os.system("osascript -e '" + str + "'")

main()