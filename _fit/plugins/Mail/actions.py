import os

def osascript(str):
	os.system("osascript - <<EOF" + str + "")

def mailpersonwithsubject(person, subject):
	osascript("""
		tell application "Mail"
			set theMessage to make new outgoing message with properties {{visible:true, subject:"{1}", content:""}}
			tell theMessage
				make new to recipient at end of to recipients with properties {{name:"{0}"}}
			end tell
		end tell
		tell application "Mail"
			activate
		end tell 
	""".format(person, subject))