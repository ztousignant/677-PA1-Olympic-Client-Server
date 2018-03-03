Zachary Tousignant
Computer Science 677

Testing documentation
Test Cases

Copying and pasting any inputs into the terminal after setup should yield the expected output. If running the clients and server on different machines, then at start each would have to given the proper command line flags for IP Address and Port Number as well:
		-a: host ip address   			default='localhost'
		-p: host port number   		default=8080
		-x: auth_id     				default=(0: client, 123: server)


1) test base GET requests
Setup:
Run server:
python olympic_server.py -x 123

Run client (with matching authorization ID):
python olympic_client.py Ðx 123


Initial GET requests:
GET /getMedalTally/Rome
GET /getMedalTally/Gaul
GET /getScore/Skating
GET /getScore/Skiing
GET /getScore/Curling

Expected output:
{'medals': {'gold': 0, 'silver': 0, 'bronze': 0}}
{'medals': {'gold': 0, 'silver': 0, 'bronze': 0}}
{'Rome': 0, 'Gaul': 0}
{'Rome': 0, 'Gaul': 0}
{'Rome': 0, 'Gaul': 0}


Updating medals and scores:

GET /setScore/Skating/1/1
GET /incrementMedalTally/Rome/gold
GET /incrementMedalTally/Rome/bronze
GET /incrementMedalTally/Rome/silver
GET /getScore/Skating
GET /getMedalTally/Rome

Expected output:
Success
Success
Success
Success
{'Rome': 1, 'Gaul': 1}
{'medals': {'gold': 1, 'silver': 1, 'bronze': 1}}

2) test unauthorized
Setup:
Run server:
python olympic_server.py -x 123

Run client (without matching authorization):
python olympic_client.py Ðx 456


Updating medals and scores:

GET /setScore/Skating/1/1
GET /incrementMedalTally/Rome/gold
GET /incrementMedalTally/Rome/bronze
GET /incrementMedalTally/Rome/silver
GET /getScore/Skating
GET /getMedalTally/Rome

Expected output:
{'error': 'unauthorized access'}
{'error': 'unauthorized access'}
{'error': 'unauthorized access'}
{'error': 'unauthorized access'}
{'Rome': 0, 'Gaul': 0}
{'medals': {'gold': 0, 'silver': 0, 'bronze': 0}}


3) test pull and stop
Setup:
Run server:
python olympic_server.py 

Run client:
python olympic_client.py

Type ÒpullÓ:
Expected output:

Pulling - type "stop" to stop pulling
GET /getMedalTally/Rome
{'medals': {'gold': 0, 'silver': 0, 'bronze': 0}}

GET /getMedalTally/Gaul
{'medals': {'gold': 0, 'silver': 0, 'bronze': 0}}



GET /getMedalTally/Rome
{'medals': {'gold': 0, 'silver': 0, 'bronze': 0}}

GET /getMedalTally/Gaul
{'medals': {'gold': 0, 'silver': 0, 'bronze': 0}}

É

Type ÒstopÓ:
Expected output:

Pulling has been stopped

4) test listen and push
Setup:
Run server:
python olympic_server.py 

Run client:
python olympic_client.py

Type ÒlistenÓ:
Expected output:

register for an event to follow, provide an ID
use the following format: GET /registerClient/<ID>/<eventName>

Register the client with ID of 1 Ð this is client A:
GET /registerClient/1/Curling

Expected output:
success
listening on port: 53472

Use <Ctrl-C> to stop

Now, start another client with authorization, and update the score of ÒCurlingÓ a few times Ð this is client B:

python olympic_client.py -x 123
GET /setScore/Curling/1/2
GET /setScore/Curling/1/2

Expected listening client output:
{'Rome':1,'Gaul':2}
{'Rome':1,'Gaul':3}

Finally, start listening with yet another client  (client C), with a different ID, on the same event, and then update again:

Client C:
python olympic_client.py
listen
GET /registerClient/2/Curling

Client B:
GET /setScore/Curling/2/3

Expected output  for both listening clients (A and B):
{'Rome':2,'Gaul':3}

Overall expected output for server:
127.0.0.1 - - [03/Mar/2018 14:06:28] "GET /registerClient/1/Curling 
HTTP/1.1" 200 Ð

127.0.0.1 - - [03/Mar/2018 14:06:48] "GET /setScore/Curling/1/2/123 HTTP/1.1" 200 -

127.0.0.1 - - [03/Mar/2018 14:06:48] "GET /setScore/Curling/1/3/123 HTTP/1.1" 200 -

127.0.0.1 - - [03/Mar/2018 14:06:39] "GET /registerClient/2/Curling HTTP/1.1" 200 Ð

127.0.0.1 - - [03/Mar/2018 14:06:48] "GET /setScore/Curling/2/3/123 HTTP/1.1" 200 -




