#olympic_server.py
#Zachary Tousignant

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

from restart import status
from restart.api import RESTArt
from restart.resource import Resource
from restart.exceptions import NotFound
from restart.utils import make_location_header

import threading
import time

api = RESTArt()

medals_lock = threading.Lock()
medals = {
	'Rome': {
		'medals': {
			'bronze': 0, 
			'silver': 0, 
			'gold': 0
		}
	},
	'Gaul': {
		'medals': {
			'bronze': 0, 
			'silver': 0, 
			'gold': 0
		}
	}
}

events_lock = threading.Lock()
events = {
	'Curling':{
		'Rome': 0,
		'Gaul': 0
	},
	'Skiing':{
		'Rome': 0,
		'Gaul': 0
	},
	'Skating':{
		'Rome': 0,
		'Gaul': 0
	}
}

@api.register(pk='<string:team>')
class getMedalTally(Resource):
	name = 'getMedalTally'

	def read(self, request, team):
		ret = []
		medals_lock.acquire()
		try:
			ret.append(medals[team])
		except KeyError:
			ret.append({"error": "key not found"})
		medals_lock.release()
		return ret[0]


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message = self.path #call RESTart api?
        self.wfile.write(message)
        self.wfile.write('\n')
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass


if __name__ == '__main__':
	HOST = 'localhost'
	PORT = 8080
	server = ThreadedHTTPServer((HOST, PORT), Handler)
	print 'Starting server, use <Ctrl-C> to stop'
	server.serve_forever()





