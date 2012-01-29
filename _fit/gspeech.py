#!/usr/local/bin/python3

import urllib.request,urllib.parse,urllib.error
import socket
import json
import subprocess

def interpret(filestr):
	with open(filestr, 'rb') as file:
		audio = file.read()
		try:
			#audio = urllib.parse.urlencode(audio)
			url = urllib.request.Request("https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-IE", audio)
			url.add_header("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")
			url.add_header("Content-Type", "audio/x-flac; rate=16000")
			resp = urllib.request.urlopen(url).read().decode("utf8", 'ignore')
			#print(resp)
			return json.loads(resp)["hypotheses"][0]["utterance"]

		except urllib.error.HTTPError as e:
			print(e.read().decode("utf8", 'ignore'))
		except urllib.error.URLError:
			print("URLError")
		except socket.error:
			print("socket.error")
		except socket.timeout:
			print("socket.timeout")

def hear():
	print("Start talking!")
	subprocess.call("rec -q -V1 -r 16000 -c 1 out.flac silence 0 1 0:00:03 2%", shell=True)
	print("Heard you.")
	return("out.flac")

def hearandinterpret():
	r = interpret(hear())
	print("I think you said {0}".format(r))
	return r