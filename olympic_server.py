#olympic_server.py
#Zachary Tousignant

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

import httplib
import threading
import time
import argparse

#Shared resources - a dict for medals and and a dict for events, with a Lock() for accessing each
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
clients_lock = threading.Lock()
registered_clients = {
	'Curling':{
	},
	'Skiing':{
	},
	'Skating':{
	}

}

"""
Handler.doGET passes a query and parameters to this function. There are 5 possible queries:

getMedalTally: returns the bronze/silver/gold medal tally of Rome or Gaul
	params - teamName
	returns - JSON formated: {'medals': {'gold': <int>, 'silver': <int>, 'bronze': <int>}}
	exceptions - error message if KeyException or incorrect number of parameters

incrementMedalTally: increments the tally for the given medal of Rome or Gaul. Requires authorization.
	params - teamName, medal, authorization
	returns - success message
	exceptions - error message if unauthorize access, KeyException, or incorrect number of parameters

getScore: returns the score between Rome and Gaul for a specific event
	params - eventName
	returns - JSON formated: {'<string:event>': {'Rome': <int>, 'Gaul': <int>}}
	exceptions - error message if KeyException or incorrect number of parameters

setScore: sets the score for a particular event. Requires authorization.
	params - eventName, rome_score, gaul_score, authorization
	returns - success message (IF registered clients, sends updated score)
	exceptions - error message if unauthorize access, KeyException, or incorrect number of parameters, incorrect parameter type

registerClient: registers a client at with a given port and ip address to recieve updates whenever the score of an event is updated
	params - clientID, eventName (port # and IP address are pulled from client's GET request)
	returns - success message
	exceptions - error message if KeyException, incorrect parameter type, or clientID already in use

Team names and event names are case sensitive.
Threadsafe for accessing shared resources.
"""
def processQuery(self, query, params):
	if query == "getMedalTally":
		#params[0] == teamName
		#error checking for key indeces
		if len(params) != 1: 
			return {"error": "incorrect number of parameters for \"getMedalTally\""}

		ret = []
		medals_lock.acquire() #critical section - access medals dict
		try:
			ret.append(medals[params[0]]) 
		except KeyError:
			ret.append({"error": "key not found"})
		medals_lock.release()
		return ret[0]

	elif query == "incrementMedalTally":
		#params[0] == teamName, params[1] == medal, params[2] == authorization
		#error checking for key indeces
		if len(params) != 3: 
			return {"error": "incorrect number of parameters for \"incrementMedalTally\""}

		#check authorization
		if params[2] == str(auth_id):
			ret = []
			medals_lock.acquire() #critical section - increment medals dict
			try:
				medals[params[0]]['medals'][params[1]] = medals[params[0]]['medals'][params[1]]+1
				ret.append('success')
			except KeyError:
				ret.append({"error": "key not found"})
			medals_lock.release()
			return ret[0]
		else:
			return {"error": "unauthorized access"}

	elif query == "getScore":
		#params[0] == eventName
		#error checking for key indeces
		if len(params) != 1: 
			return {"error": "incorrect number of parameters for \"getScore\""}

		ret = []
		events_lock.acquire() #critical section - access events dict
		try:
			ret.append(events[params[0]])
		except KeyError:
			ret.append({"error": "key not found"})
		events_lock.release()
		return ret[0]

	elif query == "setScore":
		#params[0] == eventName, params[1] == rome_score, params[2] == gaul_score, params[3] == authorization
		#error checking for key indeces
		if len(params) != 4: 
			return {"error": "incorrect number of parameters for \"setScore\""}

		#check authorization
		if params[3] == str(auth_id):
			ret = []
			update = []
			events_lock.acquire() #critical section - modify events dict
			try:
				events[params[0]]['Rome'] = int(params[1])
				events[params[0]]['Gaul'] = int(params[2])
				update.append(events[params[0]])
				ret.append('success')
			except KeyError:
				ret.append({"error": "key not found"})
			except:
				ret.append({"error": "make sure keys are of correct type"})
			events_lock.release()
			if ret[0] == 'success': #for setScore, if there are clients registered to recieve updates for an event, we send an update
				clients_lock.acquire() #critical section - push to any registered clients
				if len(registered_clients[params[0]]) > 0:
					for c in registered_clients[params[0]]:
						conn = httplib.HTTPConnection(registered_clients[params[0]][c]['ip'], registered_clients[params[0]][c]['port'], timeout=5)
						msg = str(update[0])
						conn.request("GET", msg)
						conn.close()
				clients_lock.release()
			return ret[0]
		else:
			return {"error": "unauthorized access"}
	elif query == "registerClient":
		#params[0] == clientid, params[1] == eventName
		#error checking for key indeces
		if len(params) != 2: 
			return {"error": "incorrect number of parameters for \"registerClient\""}
		ret = []
		clients_lock.acquire() #critical section - register new client
		try:
			if params[0] not in registered_clients[params[1]]: #make sure no other client with this ID has been registered for this event
				ip = self.client_address[0]
				pt = self.client_address[1]
				registered_clients[params[1]][params[0]] = {"ip": ip, "port":pt} #store client port and IP
				s = "success," + str(ip) + "," + str(pt)
				ret.append(s)
			else:
				ret.append({"error": "client with this key already registered for this event"})	
		except KeyError:
				ret.append({"error": "key not found"})
		clients_lock.release()
		return ret[0]

	else:
		return {"error": "query not found"}

"""
Receives GET requests from clients, tokenizing and passing query/parameters to processQuery().
Sends a response to the client. 
"""
class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
		self.send_response(200)
		self.end_headers()
		#split path into query and paramaters, then process
		a = self.path.split("/",2) 
		query = a[1]
		params = a[2].split("/")
		message = processQuery(self, query, params)
		self.wfile.write(message)
		self.wfile.write('\n')
		return

"""
Uses a thread per request model. For each request, a thread is generated to handle that request.
Uses ThreadingMixIn and BaseHTTPServer
"""
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass

"""
	starts the server at the given HOST IP and PORT number

	command line parameters:
		-a: host ip address   				default='localhost'
		-p: host port number   				default=8080)
		-x: cacafonix auth_id     			default=123
"""
if __name__ == '__main__':
	#command line arguements
	parser = argparse.ArgumentParser()
	parser.add_argument('-a',  dest='host', default='localhost')
	parser.add_argument('-p',  dest='port', default= 8080)
	parser.add_argument('-x',  dest='auth_id', default=123)

	args = parser.parse_args()
	
	HOST = args.host
	PORT = args.port
	auth_id = args.auth_id

	server = ThreadedHTTPServer((HOST, PORT), Handler)
	print 'Starting server, use <Ctrl-C> to stop'
	server.serve_forever()





