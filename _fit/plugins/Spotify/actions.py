import os

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