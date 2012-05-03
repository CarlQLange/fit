import plistlib, os

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
		on isrunning()
			tell application "System Events" to (name of processes) contains "iTunes"
		end isrunning

		if isrunning()
			tell application "iTunes"
				return (get artist of current track)
			end tell
		else
			return "No song playing."
		end if
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

def last():
	#play the previous track
	osascript("""
		tell application "iTunes"
			previous track
		end tell
	""")

def play(tr, ar):
	ar = bestmatch(ar, artistnames)
	tr = bestmatch(tr, tracksbyartist, arg=ar)

	print("Playing " + tr + " by " + ar)

	osascript("""
		tell application "iTunes"
			set mySongs to every track of library playlist 1 whose artist is "{0}" and name is "{1}"
			repeat with song in mySongs
				play song
			end repeat
			set song repeat of current playlist to off
		end tell
	""".format(ar, tr))

def osascript(str):
	os.system("osascript - <<EOF" + str + "")

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


def bestmatch(inp, matchto, arg=""):
	lowest = ("", 999999)
	if (arg != ""):
		for trackname in matchto(arg):
			if (recognise.match(inp, trackname) < lowest[1]):
				lowest = (trackname, recognise.match(inp, trackname))
	else:
		for trackname in matchto():
			if (recognise.match(inp, trackname) < lowest[1]):
				lowest = (trackname, recognise.match(inp, trackname))
	return lowest[0]