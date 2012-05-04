import os
import urllib.request
import re

def osascript(str):
	os.system("osascript - <<EOF" + str + "")

def current():
	osascript("""
		tell application "Spotify"
			set track_name to name of current track
			set track_artist to artist of current track
			return track_name & " by " & track_artist
		end tell
	""")

def currentartist():
	osascript("""
		tell application "Spotify"
			return artist of current track
		end tell
	""")

def next():
	osascript("""
		tell application "Spotify"
			next track
		end tell
	""")

def prev():
	osascript("""
		tell application "Spotify"
			previous track
		end tell
	""")

def playpause():
	osascript("""
		tell application "Spotify"
			playpause
		end tell
	""")

def play(tr, ar):
	#I kind of doubt I can get this to work
	url = "http://cleanify.net/play/track/" + ar.replace(' ', '-').lower() + "/" + tr.replace(' ', '-').lower()

	t = urllib.request.urlopen(url)
	st = str(t.readlines())
	try:
		f = re.findall(r'(spotify:track:\w+)', st)[0]
		os.system("open {0}".format(f))
	except IndexError:
		print("Couldn't find that track. Try searching in Spotify.")
		print("Due to the way I'm built, I may not find songs that are not well known.")
	#well, I sure showed me