from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib
import os
 
class posthandler(SimpleHTTPRequestHandler):
	def do_POST(self):
		length = int(self.headers['Content-Length'])
		post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
		print(post_data)
		os.system("fit play %s" % post_data["inp"])
		self.send_response(301)

httpd = HTTPServer(('127.0.0.1', 8000), posthandler)
httpd.serve_forever()