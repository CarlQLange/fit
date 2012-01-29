from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib
import os

class posthandler(SimpleHTTPRequestHandler):
	def do_POST(self):
		length = int(self.headers['Content-Length'])
		post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
		print(post_data)
		os.system('fit "%s"' % post_data["inp"][0]) #FIXME this is bad bad bad
		self.send_response(200)

def serve():
	print("Serving on port 5171.")
	print("Go to 127.0.0.1:5171/_fit/web in your browser!")
	httpd = HTTPServer(('127.0.0.1', 5171), posthandler)
	httpd.serve_forever()