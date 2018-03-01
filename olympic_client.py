#olympic_client.py
#Zachary Tousignant

import httplib
import time
import thread
import argparse

"""
On user input of "stop", thread exits and notifies calling funtions

	params - [] (should always be an empty list)
	returns - void

"""
def wait_for_stop(stop_condition):
	while(True):
		time.sleep(0.5)
		inp = raw_input()
		if inp == "stop":
			stop_condition.append("stop")
			return

"""
creates an HTTP connection with given host:port
Makes request  GET /getMedalTally/<teamName> for Rome and Gaul at specified interval
and prints JSON of medal tallies. Stops when "stop" is input, via wait_for_stop()

	params - host IP addess, host port #, interval at which to send requests
	returns - void (prints message)
"""
def pull_periodically(host, port, interval):

	print 'Pulling - type \"stop\" to stop pulling'
	stop_condition = []
	thread.start_new_thread(wait_for_stop, (stop_condition,)) #starts a thread that waits for user input "stop"
	client = httplib.HTTPConnection(host, port, timeout=5)

	#loops endlessly sending GETs until "stop" is input
	while True: 
		print "GET /getMedalTally/Rome"
		client.request("GET","/getMedalTally/Rome")
		message = client.getresponse().read()
		print message

		print "GET /getMedalTally/Gaul"
		client.request("GET","/getMedalTally/Gaul")
		message = client.getresponse().read()
		print message
		print '\n'
		time.sleep(interval)
		if stop_condition:
			print "Pulling has been stopped"
			return

"""
takes user input and attempts to make a GET request to the server.
For Cacafonix queries, incrementMedalTally and setScore, the clients auth_ID is appended to the GET request
	params - host IP address, host port #, user raw_input string, auth_ID of the client
	returns - void (prints message)
	exceptions - error message if invalid input string
"""
def process_request(host, port, inp, auth):
	a = inp.split()
	error_str = "requests should have format: GET /query/var1/var2/etc"
	if(a and a[0] == "GET"): #make sure input is a GET command
		try:
			client = httplib.HTTPConnection(host, port, timeout=5)
			b = a[1].split("/",2) 
			query = b[1]
			if query == "incrementMedalTally" or query == "setScore": #append auth_id for reserved commands
				a[1] = a[1]+"/"+str(auth)
			client.request(a[0],a[1]) 
			message = client.getresponse().read()
			if message == "":
				print error_str
			print message
		except:
			print error_str
	else:
		print error_str
	return

"""
	runs an indivdual client intended to query olympics_server at the given HOST IP and PORT number
	User can type "pull" to begin periodically requesting the medal tallies of each teamName
	User can type a GET request and it will be processed and sent to the server. 
	NOTE: auth_id is automatically appended and should not be included in user input

	command line parameters:
		-a: host ip address   				default='localhost'
		-p: host port number   				default=8080)
		-i: client-pull request interval    default=5
		-x: client auth_id     				default=0
"""
if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-a',  dest='host', default='localhost')
	parser.add_argument('-p',  dest='port', default= 8080)
	parser.add_argument('-i',  dest='interval', default=5)
	parser.add_argument('-x',  dest='auth_id', default=0)

	args = parser.parse_args()

	HOST = args.host
	PORT = args.port
	interval = args.interval
	auth_id = args.auth_id
	print auth_id
	print '\nStarting client, use <Ctrl-C> to stop'
	print 'Type \"pull\" to check getMedalTally periodically'
	print 'GET requests can be made with the format: GET /query/var1/var2/etc\n'
	while True:
		inp = raw_input()
		if inp == "pull":
			pull_periodically(HOST, PORT, interval)
		else:
			process_request(HOST, PORT, inp, auth_id)
		inp = ""


