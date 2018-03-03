## Running olympic_server.py

Open a terminal and execute:
```
python olympic_server.py
```

There are optional command line flags as follows:

		-a: host ip address  			default='localhost'

		-p: host port number   			default=8080

		-x: cacafonix auth_id     		default=123

Stop running the server with Ctrl-C.


## Running olympic_client.py

Open a terminal and execute:
```
python olympic_client.py
```

There are optional command line flags as follows:

		-a: host ip address   				      default='localhost'
		
		-p: host port number   				      default=8080
		
		-i: client-pull request interval		      default=5
		
		-x: client auth_id     				      default=0
    
### client-pull:
The following GET requests may be issued by any client:
```
GET /getMedalTally/<TeamName>
GET /getScore/<EventName>
```
If a client (Cacaphonix) is given the authorization ID that matches the server's,the following requests may also be issued:
```
GET /incrementMedalTally/<TeamName>/<Medal>
GET /setScore/<EventName>/<int:rome_score>/<int:gaul_score>
```
Notes: 
Make sure to include the introductory '/' 
'Rome' and 'Gaul' are the possible TeamNames, and are case sensitive
'bronze', 'silver', and 'gold' are the Medals, and are case sensitive
'Curling', 'Skiing', and 'Skating' are the EventNames, and are case sensitive

To begin pulling the medal tallies from the server periodically, type "pull":
```
pull
```
At the interval set with the command "-i", this will repeatedly make the following requests:
```
GET /getMedalTally/Rome
GET /getMedalTally/Gaul
```
Other requests cannot be entered while pulling.
To stop and return to manually entering requests, type "stop":
```
stop
```

### server-push:
To register for updates for an event, begin running the client, then type "listen":
```
listen
```
At this point, select an ID for this client to be remembered as and the event about which the client will receive updates.
Use the following request:
```
GET /registerClient/<int:ID>/<EventName>
```
Now the client will listen for updates, which will automatically be sent by the server to any registered clients.
Use Ctrl-C to stop.

